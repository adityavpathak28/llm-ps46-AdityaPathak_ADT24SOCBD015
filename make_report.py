from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

body = ParagraphStyle("b", fontName="Times-Roman", fontSize=12, leading=15.5, spaceAfter=4)
h = ParagraphStyle("h", fontName="Times-Bold", fontSize=12, leading=14, spaceBefore=5, spaceAfter=2,
                   textColor=colors.HexColor("#1F3864"))
title = ParagraphStyle("t", fontName="Times-Bold", fontSize=16, leading=19, alignment=1, spaceAfter=4)
item = ParagraphStyle("i", parent=body, leftIndent=16, firstLineIndent=-12, spaceAfter=1)
small = ParagraphStyle("s", parent=body, fontName="Times-Italic", fontSize=12, alignment=1)

S = []
S.append(Paragraph("To-Do List from Text (LLM Mini Project)", title))
hdr = [["PS Number: 46", "Roll No: 46"],
       ["Name: Aditya Pathak", "Class: [YOUR CLASS]"],
       ["GitHub: [PASTE YOUR REPO LINK HERE]", ""]]
t = Table(hdr, colWidths=[8.5*cm, 8.5*cm])
t.setStyle(TableStyle([("FONT", (0,0), (-1,-1), "Times-Roman", 12), ("BOX", (0,0), (-1,-1), 0.7, colors.black),
    ("SPAN", (0,2), (1,2)), ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2)]))
S += [t]

def sec(name, text): S.extend([Paragraph(name, h), Paragraph(text, body)])

sec("1. Problem Statement",
 "People write quick, messy notes full of tasks, dates and urgency hints, and important items get missed. "
 "This project converts free-text notes into a clean, prioritised to-do list with deadlines. It helps students "
 "and working people organise their day without retyping anything.")
sec("2. Tools &amp; Model",
 "Python 3.10, Streamlit (UI), requests, pandas and python-dotenv. The LLM is Llama 3.3 70B accessed through the "
 "Groq API (Gemini and Ollama are also supported in the code). No model training was done.")

S.append(Paragraph("3. Procedure", h))
steps = [
 "Created a virtual environment, installed the libraries and got a free Groq API key stored in a .env file.",
 "Tried the prompt in the Groq playground on five sample notes until the output was consistent.",
 "Wrote <i>todo_core.py</i>: build prompt, call the LLM, parse the JSON reply, sort tasks by priority and deadline.",
 "Built <i>app.py</i> in Streamlit: notes box, sidebar settings, a checkbox per task, progress bar and CSV download.",
 "Wrote four pytest tests (parsing, sorting, prompt content, retry) and tested on five different note samples.",
 "Pushed the code to a public GitHub repository with a README, requirements.txt and .gitignore (hides .env).",
]
for i, s in enumerate(steps, 1):
    S.append(Paragraph(f"{i}. {s}", item))

S.append(Paragraph("4. Prompt Used", h))
S.append(Paragraph(
 "<i>\"Today's date is {date} ({weekday}). Read the messy notes and extract every actionable task. Return ONLY a "
 "JSON array with keys task (short imperative), priority (High/Medium/Low) and deadline (YYYY-MM-DD, resolving words "
 "like tomorrow or Friday, else 'Not specified'). Do not invent tasks; merge duplicates.\"</i> "
 "<b>Improvement:</b> my first prompt had no date, so \"Friday\" and \"tomorrow\" gave wrong deadlines. Adding "
 "today's date and weekday fixed this.", body))

res_tbl = Table([[Paragraph("<b>[INSERT SCREENSHOT HERE]</b><br/>Input: sample_notes.txt notes<br/>"
   "Output: prioritised task list with checkboxes", small)]], colWidths=[17*cm], rowHeights=[6.5*cm])
res_tbl.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 0.7, colors.grey), ("VALIGN", (0,0), (-1,-1), "MIDDLE")]))
S.append(Paragraph("5. Results", h))
S.append(Paragraph("For the input \"finish DBMS assignment by friday, super important ... call dad tomorrow evening ... "
 "clean laptop someday\", the app produced the DBMS assignment as High with a resolved date, calling dad as "
 "Medium/High due tomorrow, and cleaning files as Low with no deadline. All were sorted correctly.", body))
S.append(res_tbl)

sec("6. Challenges",
 "(a) The model sometimes wrapped JSON in markdown fences or added extra text, which broke json.loads; I fixed this "
 "by stripping fences, extracting the text between [ and ], and retrying once with a stricter instruction. "
 "(b) Some priorities came back in odd forms, so invalid values default to Medium. "
 "(c) pytest could not find my module, solved by adding a conftest.py file. "
 "(d) Free API rate limits were handled by showing a clear error message.")
sec("7. Conclusion",
 "The tool reliably turns messy notes into an ordered to-do list. It can still guess wrongly when a deadline is "
 "vague (for example \"next week\"). Future improvement: export tasks to Google Calendar and add reminders.")

doc = SimpleDocTemplate("Report.pdf", pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm,
                        title="PS46 To-Do List from Text", author="Aditya Pathak")
doc.build(S)
from pypdf import PdfReader
print("pages:", len(PdfReader("Report.pdf").pages))
