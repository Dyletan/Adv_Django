import PyPDF2
from io import BytesIO
import docx

def extract_resume_text(file):
    """
    Extract raw text from a PDF or DOCX resume file.
    
    Args:
        file: File object (e.g., from request.FILES).
    
    Returns:
        str: Extracted text or empty string if extraction fails.
    """
    try:
        if file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text.strip()
        elif file.name.endswith('.docx'):
            doc = docx.Document(BytesIO(file.read()))
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text.strip()
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")
    except Exception as e:
        raise ValueError(f"Failed to extract text: {str(e)}")