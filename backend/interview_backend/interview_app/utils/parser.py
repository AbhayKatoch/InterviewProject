import re
import pdfplumber
from docx import Document
from typing import Dict

EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_REGEX = re.compile(r'(\+?\d[\d\-\s]{6,}\d)')

def text_from_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or '')
    return '\n'.join(text)

def text_from_docx(path):
    doc = Document(path)
    return '\n'.join(p.text for p in doc.paragraphs)