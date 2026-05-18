# Document Intelligence Agent

A multi-agent pipeline that reads a PDF document, extracts structured data, analyzes it for key findings, and generates a professional intelligence report.

## Architecture

```
PDF File
   |
   v
PDFReaderAgent       — extracts raw text page by page via pdfplumber
   |
   v
ExtractorAgent       — LLM: pulls entities, dates, amounts, document type, topics
   |
   v
AnalystAgent         — LLM: identifies important findings, risks, action items
   |
   v
ReportWriterAgent    — LLM: writes clean 300-400 word intelligence report
```

## Setup

1. Clone or download this project.

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=sk-or-...
   ```
   Get a key at: https://openrouter.ai/keys

4. Generate the sample PDF (one-time):
   ```bash
   python sample/create_sample.py
   ```

## Usage

Run with a PDF path as argument:
```bash
python main.py sample/sample_contract.pdf
```

Or run without arguments and enter the path interactively:
```bash
python main.py
```

## Output

The pipeline prints:
- Agent status as each step runs
- Extracted entities (names, dates, amounts, organizations)
- Document type and main topics
- Full intelligence report in a formatted panel

## Stack

- `openai` — OpenRouter-compatible API client
- `pdfplumber` — PDF text extraction
- `rich` — terminal output formatting
- `python-dotenv` — environment variable loading
- `reportlab` — sample PDF generation
