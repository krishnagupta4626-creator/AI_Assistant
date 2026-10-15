# 🎓 College AI Assistant

An intelligent assistant designed for college academic workflows, built using Python and LLM Function Calling (Tool Use). The assistant evaluates student queries, dynamically executes designated Python tools, and logs the tool name during each operation.

---

## 📌 Features

1. **Attendance & Percentage Calculation**
   * Triggers `calculator_tool`).
   * Automatically calculates attendance percentage ($\frac{\text{attended}}{\text{total}} \times 100$) and handles arithmetic requests.

2. **Attendance Marking**
   * Triggers `attendance_tool`.
   * Records student attendance (`Present` / `Absent`) by date, student ID, and subject.

3. **Timetable & Schedule Analysis**
   * Triggers `timetable_analysis_tool`.
   * Ingests schedule data from external files to resolve queries about lectures and class timings.

4. **Multi-Format Document Ingestion**
   * Native parsing support for `.pdf`, `.docx`, and `.txt` files.

5. **Explicit Tool Operation Logging**
   * Automatically prints the exact tool name and parameters invoked during an operation.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **LLM Engine:** Google GenAI SDK (`gemini-3.5-flash`)
* **Document Parsing:** `pypdf`, `python-docx`
* **Environment:** `python-dotenv`


