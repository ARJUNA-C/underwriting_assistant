import fitz  # PyMuPDF
import logging
from models.schema import ExtractionMeta
from .ocr import perform_ocr

logger = logging.getLogger(__name__)

class ExtractionError(Exception):
    """Raised when PDF text extraction completely fails."""
    pass

def extract_text(pdf_bytes: bytes) -> tuple[str, ExtractionMeta]:
    """
    Extracts text from PDF bytes using PyMuPDF.
    If extracted text is under threshold (< 50 chars), attempts OCR fallback.
    Returns (extracted_text, ExtractionMeta).
    """
    if not pdf_bytes:
        raise ExtractionError("PDF file content is empty.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(doc)
        text_pages = []
        for page in doc:
            text_pages.append(page.get_text())
        doc.close()

        digital_text = "\n".join(text_pages).strip()

        # If text is substantial, return digital extraction
        if len(digital_text) >= 50:
            meta = ExtractionMeta(
                source="digital",
                page_count=page_count,
                ocr_failed=False
            )
            return digital_text, meta

        # Fallback to OCR if digital text is empty or negligible
        logger.info("Digital text length < 50 chars. Attempting OCR fallback...")
        ocr_text, ocr_failed = perform_ocr(pdf_bytes)

        source_type = "ocr" if not ocr_failed and len(ocr_text) > 0 else "digital"
        final_text = ocr_text if len(ocr_text) > 0 else digital_text

        meta = ExtractionMeta(
            source=source_type,
            page_count=page_count,
            ocr_failed=ocr_failed
        )
        return final_text, meta

    except Exception as e:
        if isinstance(e, ExtractionError):
            raise e
        raise ExtractionError(f"Failed to parse PDF document: {str(e)}") from e
