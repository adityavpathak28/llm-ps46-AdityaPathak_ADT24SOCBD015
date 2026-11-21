# PS46 – To-Do List from Text  (draft: rewrite in your own words, 2 pages, export to PDF)
Header: Name / Roll No 46 / Class / GitHub link
**Problem statement:** Notes are messy and tasks get missed. The tool converts free text into a prioritised to-do list with deadlines. Helps students and professionals.
**Tools & model:** Python, Streamlit, requests, pandas; Llama 3.3 70B via Groq (or Gemini 2.5 Flash / Ollama).
**Procedure:** 1) Got a free API key. 2) Tested the prompt in the playground on 5 notes. 3) Wrote todo_core.py (prompt → LLM → JSON parse → sort). 4) Built Streamlit UI with checkboxes, progress bar, CSV download. 5) Wrote pytest tests. 6) Tested on 5 inputs, pushed to GitHub.
**Prompt used:** (paste from PROMPT_TEMPLATE in todo_core.py). Improvement: added today's date + weekday so "Friday"/"tomorrow" resolve correctly; added "return ONLY JSON" after fenced output broke parsing.
**Results:** screenshot of sample_notes.txt input and the output list.
**Challenges:** model wrapped JSON in markdown fences (fixed by stripping + retry); invalid priority values (defaulted to Medium); API rate limits.
**Conclusion:** Works well on clear notes; ambiguous deadlines can be wrong. Future: calendar export, reminders.
