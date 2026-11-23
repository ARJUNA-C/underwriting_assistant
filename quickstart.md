# Quickstart

## Overview
This project is a Streamlit-based AI underwriting assistant that processes a single proposal PDF, extracts profile data, identifies risk factors, surfaces gaps/missing info, and renders a dashboard.

## Prerequisites
- Python 3.11+ installed
- `pip` available
- System binaries installed:
  - Tesseract OCR
  - Poppler utilities

## Recommended setup
1. Open a terminal in the project root:
   ```powershell
   cd c:\RTD\Underwrting_assistant
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Configure API key
1. Copy the example environment file:
   ```powershell
   copy .env.example .env
   ```
2. Open `.env` and set `GROQ_API_KEY`:
   ```text
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. Alternatively, you may export the value in your shell before running Streamlit.

## Run the app
Start the Streamlit app from the project root:

```powershell
streamlit run app.py
```

Then open the browser URL shown by Streamlit.

## How to use
- Upload a proposal PDF in the sidebar.
- The app runs the staged underwriting pipeline.
- Results appear as profile data, risk cards, gap cards, and a summary.

## Testing
Run tests from the project root:

```powershell
pytest
```

## Notes
- The app requires `GROQ_API_KEY` to run LLM inference.
- If PDF text extraction fails, the pipeline falls back to OCR.
- The project is designed for a single PDF upload at a time.
