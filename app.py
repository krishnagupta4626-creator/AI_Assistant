import os
import time
from dotenv import load_dotenv
from pypdf import PdfReader
import docx
from google import genai
from google.genai import types
from google.genai.errors import ServerError

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# In-memory storage for attendance records
ATTENDANCE_LOG = []


# ==========================================
# 1. FILE PARSING (PDF, DOCX, TXT)
# ==========================================
def extract_document_text(file_path: str) -> str:
    """Reads and extracts text from .pdf, .docx, or .txt files."""
    if not os.path.exists(file_path):
        return f"[File Error: '{file_path}' does not exist.]"

    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".pdf":
            reader = PdfReader(file_path)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        elif ext == ".docx":
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return f"[Unsupported format '{ext}'. Only .pdf, .docx, and .txt are supported.]"
    except Exception as e:
        return f"[Error parsing file: {e}]"


# ==========================================
# 2. ASSIGNMENT TOOLS
# ==========================================
def calculator_tool(attended_classes: float, total_classes: float) -> str:
    """Calculates attendance percentage. Use this whenever the user asks for attendance percentage or math calculations."""
    print("\n" + "=" * 55)
    print(">> TOOL USED IN OPERATION: [calculator_tool]")
    print(f">> ARGUMENTS: attended_classes={attended_classes}, total_classes={total_classes}")
    print("=" * 55 + "\n")

    if total_classes <= 0:
        return "Total classes must be greater than zero."
    percentage = (attended_classes / total_classes) * 100
    return f"Calculated: {attended_classes:.0f}/{total_classes:.0f} attended = {percentage:.2f}%"


def attendance_tool(student_id: str, date: str, subject: str, status: str) -> str:
    """Marks attendance for a student on a specific date and subject. Status must be 'Present' or 'Absent'."""
    print("\n" + "=" * 55)
    print(">> TOOL USED IN OPERATION: [attendance_tool]")
    print(f">> ARGUMENTS: student_id={student_id}, date={date}, subject={subject}, status={status}")
    print("=" * 55 + "\n")

    record = {
        "student_id": student_id,
        "date": date,
        "subject": subject,
        "status": status.capitalize()
    }
    ATTENDANCE_LOG.append(record)
    return f"Attendance recorded: {student_id} is marked '{status.capitalize()}' for {subject} on {date}."


def timetable_analysis_tool(query: str, timetable_content: str) -> str:
    """Analyzes class schedules, timings, and timetable documents provided by the student."""
    print("\n" + "=" * 55)
    print(">> TOOL USED IN OPERATION: [timetable_analysis_tool]")
    print(f">> ARGUMENTS: query={query}")
    print("=" * 55 + "\n")

    if not timetable_content or timetable_content.startswith("["):
        return "No valid timetable document content was provided."
    return f"Timetable Context:\n{timetable_content}\nUser Question: {query}"


SYSTEM_PROMPT = """
You are a College AI Assistant.
Rules:
1. When asked about attendance percentage or math, you MUST call 'calculator_tool'.
2. When asked to mark attendance for a student/day, you MUST call 'attendance_tool'.
3. When asked about schedules or classes from an attached document, you MUST call 'timetable_analysis_tool'.
Always confirm the result clearly to the user.
"""


# ==========================================
# 3. ASSISTANT CONTROLLER (With Auto-Retry)
# ==========================================
def ask_assistant(user_message: str, file_path: str = None):
    doc_context = ""
    if file_path:
        doc_context = extract_document_text(file_path)
        print(f"\n[System] Ingested document: {file_path}")

    full_prompt = user_message
    if doc_context:
        full_prompt += f"\n\n[Attached Document Data]:\n{doc_context}"

    # Use client.chats to avoid AFC warnings
    chat = client.chats.create(
        model="gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[calculator_tool, attendance_tool, timetable_analysis_tool],
            temperature=0.0
        )
    )

    # Retry loop to handle temporary 503 spikes
    for attempt in range(1, 4):
        try:
            response = chat.send_message(full_prompt)
            print(f"Assistant: {response.text}\n")
            break
        except ServerError as e:
            if "503" in str(e) and attempt < 3:
                print(f"[503 Spike: server busy. Retrying in 4 seconds (Attempt {attempt}/3)...]")
                time.sleep(4)
            else:
                raise e


# ==========================================
# 4. RUN ALL THREE ASSIGNMENT SCENARIOS
# ==========================================
if __name__ == "__main__":
    print("--- 1. TESTING ATTENDANCE CALCULATION ---")
    ask_assistant("I have attended 38 lectures out of 45. What is my attendance percentage?")

    print("--- 2. TESTING ATTENDANCE MARKING ---")
    ask_assistant("Mark student CS-202 Present for Operating Systems on 15-10-2026.")

    print("--- 3. TESTING TIMETABLE ANALYSIS WITH FILE ---")
    with open("timetable.txt", "w") as f:
        f.write("Monday: 09:00 AM - Computer Networks | 11:00 AM - Software Engineering\n")
        f.write("Tuesday: 10:00 AM - Database Systems | 02:00 PM - Python Lab\n")

    ask_assistant(
        user_message="What lecture do I have on Tuesday morning?",
        file_path="timetable.txt"
    )