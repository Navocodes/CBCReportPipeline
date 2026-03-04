from pdf2image import convert_from_path
import pytesseract
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file using OCR (Tesseract).
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    try:
        images = convert_from_path(pdf_path)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return ""

    text = ""
    for image in images:
        text += pytesseract.image_to_string(image) + "\n"
    return text
