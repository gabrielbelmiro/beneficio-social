from pathlib import Path
import pdfplumber
import pytesseract
from PIL import Image


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_from_pdf(file_path: str) -> str:
    text_content = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)

    return "\n".join(text_content)


def extract_text_from_png(file_path: str) -> str:
    image = Image.open(file_path)
    return pytesseract.image_to_string(image, lang="por")


def extract_text(file_path: str, mime_type: str) -> str:
    if mime_type == "application/pdf":
        return extract_text_from_pdf(file_path)

    if mime_type == "image/png":
        return extract_text_from_png(file_path)

    raise ValueError("Tipo de arquivo não suportado para OCR")