import pdfplumber
from pathlib import Path


class PDFReaderAgent:
    def __init__(self):
        self.name = "PDFReaderAgent"

    def read(self, pdf_path: str) -> list[dict]:
        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {pdf_path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a .pdf file, got: {path.suffix}")

        pages = []
        with pdfplumber.open(str(path)) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                pages.append({
                    "page": i,
                    "text": text.strip(),
                })

        if not any(p["text"] for p in pages):
            raise ValueError(
                "No text could be extracted from this PDF. "
                "The file may be scanned/image-based and requires OCR."
            )

        return pages
