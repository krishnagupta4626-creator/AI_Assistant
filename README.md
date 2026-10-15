# 🎓 College AI Assistant

An intelligent assistant designed for college academic workflows, built using Python and LLM Function Calling (Tool Use)[span_2](start_span)[span_2](end_span). The assistant evaluates student queries, dynamically executes designated Python tools, and logs the tool name during each operation[span_3](start_span)[span_3](end_span).

---

## 📌 Features

1. **Attendance & Percentage Calculation**[span_4](start_span)[span_4](end_span)
   * Triggers `calculator_tool`[span_5](start_span)[span_5](end_span).
   * Automatically calculates attendance percentage ($\frac{\text{attended}}{\text{total}} \times 100$) and handles arithmetic requests[span_6](start_span)[span_6](end_span).

2. **Attendance Marking**[span_7](start_span)[span_7](end_span)
   * Triggers `attendance_tool`[span_8](start_span)[span_8](end_span).
   * Records student attendance (`Present` / `Absent`) by date, student ID, and subject[span_9](start_span)[span_9](end_span).

3. **Timetable & Schedule Analysis**[span_10](start_span)[span_10](end_span)
   * Triggers `timetable_analysis_tool`[span_11](start_span)[span_11](end_span).
   * Ingests schedule data from external files to resolve queries about lectures and class timings[span_12](start_span)[span_12](end_span).

4. **Multi-Format Document Ingestion**[span_13](start_span)[span_13](end_span)
   * Native parsing support for `.pdf`, `.docx`, and `.txt` files[span_14](start_span)[span_14](end_span).

5. **Explicit Tool Operation Logging**[span_15](start_span)[span_15](end_span)
   * Automatically prints the exact tool name and parameters invoked during an operation[span_16](start_span)[span_16](end_span).

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **LLM Engine:** Google GenAI SDK (`gemini-3.5-flash`)[span_17](start_span)[span_17](end_span)
* **Document Parsing:** `pypdf`, `python-docx`
* **Environment:** `python-dotenv`


