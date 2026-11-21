# PS46 – To-Do List from Text

**Problem:** People write messy notes. This app converts free-text notes into a prioritised to-do list (task, priority, deadline) using an LLM.

## Features
- Paste notes → LLM returns tasks as JSON (`task`, `priority`, `deadline`)
- Relative dates ("friday", "tomorrow") resolved against today's date
- Tasks sorted by priority, then deadline; a `st.checkbox` per task + progress bar
- CSV download; works with Groq, Gemini (free keys) or local Ollama
- Robust JSON parsing with one automatic retry

## Run
```bash
pip install -r requirements.txt
cp .env.example .env        # add GROQ_API_KEY or GEMINI_API_KEY
streamlit run app.py
```
Run tests: `pytest -q`

## Structure
`app.py` (UI) · `todo_core.py` (prompt, LLM call, parsing) · `tests/` · `samples/sample_notes.txt`

## Screenshots
Add 1–2 screenshots here after running the app.
