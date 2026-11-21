"""Core logic for PS46: To-Do List from Text.
Turns messy free-text notes into a prioritised to-do list using an LLM.
Providers: Groq, Gemini, Ollama (all callable through plain HTTP)."""
import json
import os
import re
from datetime import date

import requests

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

PROMPT_TEMPLATE = """You are a task-extraction assistant.
Today's date is {today} ({weekday}).

Read the messy notes below and extract every actionable task.
Return ONLY a JSON array (no explanation, no markdown fences). Each item must have exactly these keys:
  "task":     short imperative sentence (max 12 words)
  "priority": one of "High", "Medium", "Low"
  "deadline": date as YYYY-MM-DD if a deadline is stated or implied
              (resolve words like "tomorrow", "Friday", "next week" using today's date),
              otherwise the string "Not specified"

Rules:
- Priority is High if urgent, due within 2 days, or marked important; Low if optional/"someday".
- Do not invent tasks that are not in the notes.
- Merge duplicate tasks.

NOTES:
\"\"\"
{notes}
\"\"\"
"""


def build_prompt(notes: str, today: date | None = None) -> str:
    today = today or date.today()
    return PROMPT_TEMPLATE.format(
        today=today.isoformat(), weekday=today.strftime("%A"), notes=notes.strip()
    )


# ---------- LLM calls ----------
def call_llm(prompt: str, provider: str, api_key: str = "", model: str = "") -> str:
    provider = provider.lower()
    if provider == "groq":
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model or "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            },
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    if provider == "gemini":
        m = model or "gemini-2.5-flash"
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
            headers={"x-goog-api-key": api_key},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2},
            },
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    if provider == "ollama":
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model or "llama3.2", "prompt": prompt, "stream": False,
                  "options": {"temperature": 0.2}},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["response"]
    raise ValueError(f"Unknown provider: {provider}")


# ---------- Parsing ----------
def parse_tasks(raw: str) -> list[dict]:
    """Extract a clean list of task dicts from the LLM's raw text."""
    text = re.sub(r"```(?:json)?", "", raw).strip()
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON list found in the model output.")
    data = json.loads(text[start : end + 1])
    tasks = []
    for item in data:
        if not isinstance(item, dict) or not str(item.get("task", "")).strip():
            continue
        pr = str(item.get("priority", "Medium")).strip().capitalize()
        if pr not in PRIORITY_ORDER:
            pr = "Medium"
        dl = str(item.get("deadline", "Not specified")).strip() or "Not specified"
        tasks.append({"task": str(item["task"]).strip(), "priority": pr, "deadline": dl})
    return sort_tasks(tasks)


def sort_tasks(tasks: list[dict]) -> list[dict]:
    """Sort by priority (High first), then by deadline (dated before undated)."""
    def key(t):
        dl = t["deadline"]
        dated = bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", dl))
        return (PRIORITY_ORDER[t["priority"]], 0 if dated else 1, dl if dated else "")
    return sorted(tasks, key=key)


def extract_tasks(notes: str, provider: str, api_key: str = "", model: str = "") -> list[dict]:
    """Full pipeline: notes -> prompt -> LLM -> parsed, sorted tasks (one retry on bad JSON)."""
    prompt = build_prompt(notes)
    last_err = None
    for _ in range(2):
        raw = call_llm(prompt, provider, api_key, model)
        try:
            return parse_tasks(raw)
        except (ValueError, json.JSONDecodeError) as e:
            last_err = e
            prompt += "\n\nYour previous reply was not valid JSON. Return ONLY the JSON array."
    raise ValueError(f"Could not parse model output: {last_err}")


def get_api_key(provider: str) -> str:
    return os.getenv({"groq": "GROQ_API_KEY", "gemini": "GEMINI_API_KEY"}.get(provider, ""), "")
