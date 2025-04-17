import fitz
import docx
import re
from io import BytesIO


def extract_resume_text(file):
    name = file.name.lower()
    content = file.read()
    try:
        if name.endswith('.pdf'):
            stream = BytesIO(content)
            doc = fitz.open(stream=stream, filetype="pdf")
            pages = []
            for i, page in enumerate(doc, start=1):
                raw = page.get_text("text") or ""
                lines = [ln.strip() for ln in raw.split('\n')]
                cleaned = []
                for ln in lines:
                    if not ln:
                        continue
                    ln = re.sub(r'\s{2,}', ' ', ln)
                    if cleaned and cleaned[-1].endswith('-'):
                        cleaned[-1] = cleaned[-1][:-1] + ln
                    else:
                        cleaned.append(ln)
                page_text = "\n".join(cleaned)
                page_text = re.sub(r'\n{3,}', '\n\n', page_text)
                pages.append(page_text)
            full = "\n\n".join(pages)
            return full.strip()

        elif name.endswith('.docx'):
            doc = docx.Document(BytesIO(content))
            paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paras).strip()

        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

    except Exception as e:
        raise ValueError(f"Failed to extract text: {e}")