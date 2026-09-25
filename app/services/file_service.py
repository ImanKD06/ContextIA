from fastapi import UploadFile
from pypdf import PdfReader
from docx import Document as DocxDocument
from io import BytesIO


async def extract_text_from_txt(file: UploadFile) -> str:
    content = await file.read()
    return content.decode("utf-8")


async def extract_text_from_pdf(file: UploadFile) -> str:
    content = await file.read()

    pdf = PdfReader(BytesIO(content))

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


async def extract_text_from_docx(file: UploadFile) -> str:
    content = await file.read()

    document = DocxDocument(BytesIO(content))

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

    return text