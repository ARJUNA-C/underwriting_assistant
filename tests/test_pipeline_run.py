import os
import pytest
from pipeline.orchestrator import run_pipeline

@pytest.mark.asyncio
async def test_full_pipeline_on_digital_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "fixtures", "sample_digital.pdf")
    assert os.path.exists(pdf_path)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # Run extraction stage without API key requirement
    from pipeline.ingest import extract_text
    extracted_text, meta = extract_text(pdf_bytes)

    assert meta.source == "digital"
    assert meta.page_count >= 1
    assert "John Edward Doe" in extracted_text
    assert "42 years old" in extracted_text
