import io
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

def perform_ocr(pdf_bytes: bytes) -> Tuple[str, bool]:
    """
    Perform Tesseract OCR fallback on PDF bytes via pdf2image and pytesseract.
    Returns (extracted_text, ocr_failed).
    """
    try:
        from pdf2image import convert_from_bytes
        import pytesseract

        # Convert PDF pages to PIL images
        images = convert_from_bytes(pdf_bytes)
        ocr_texts = []
        for i, img in enumerate(images):
            page_text = pytesseract.image_to_string(img)
            ocr_texts.append(page_text)
        
        full_text = "\n".join(ocr_texts).strip()
        return full_text, False

    except Exception as e:
        logger.warning(f"OCR fallback failed: {e}")
        return "", True
