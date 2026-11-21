"""PS46 - To-Do List from Text (Streamlit UI)."""
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from todo_core import extract_tasks, get_api_key

load_dotenv()
st.set_page_config(page_title="To-Do List from Text", page_icon="✅", layout="centered")
st.title("✅ To-Do List from Text")
st.caption("Paste messy notes → get a prioritised to-do list with deadlines.")

SAMPLE = open("samples/sample_notes.txt", encoding="utf-8").read()
ICON = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("LLM provider", ["Groq", "Gemini", "Ollama"])
    key = ""
    if provider != "Ollama":
        key = st.text_input("API key (optional if set in .env)", type="password")
        key = key or get_api_key(provider.lower())
    model = st.text_input("Model (optional)", placeholder="leave blank for default")
    if st.button("Load sample notes"):
        st.session_state["notes"] = SAMPLE

notes = st.text_area("Your notes", key="notes", height=220,
                     placeholder="e.g. submit DBMS assignment by friday, buy gift for mom's bday on 25th...")

if st.button("Generate to-do list", type="primary"):
    if not notes.strip():
        st.warning("Please paste some notes first.")
    elif provider != "Ollama" and not key:
        st.error("Add an API key in the sidebar or in your .env file.")
    else:
        with st.spinner("Extracting tasks..."):
            try:
                st.session_state["tasks"] = extract_tasks(notes, provider.lower(), key, model)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

tasks = st.session_state.get("tasks")
if tasks:
    st.subheader("Your tasks")
    done = 0
    for i, t in enumerate(tasks):
        c = st.checkbox(f"{ICON[t['priority']]} **{t['task']}**  —  {t['priority']} · due {t['deadline']}",
                        key=f"task_{i}")
        done += c
    st.progress(done / len(tasks), text=f"{done}/{len(tasks)} completed")
    df = pd.DataFrame(tasks)
    st.download_button("Download as CSV", df.to_csv(index=False), "todo.csv", "text/csv")
