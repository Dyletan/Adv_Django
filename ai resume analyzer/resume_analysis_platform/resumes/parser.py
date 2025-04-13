import spacy
from PyPDF2 import PdfReader
from docx import Document
from .models import ParsedResume, Experience

nlp = spacy.load("en_core_web_md")

def parse_resume(file_path, user_id):
    """Parse a resume file and save to MongoDB."""
    text = extract_text(file_path)
    doc = nlp(text)
    
    # Extract skills (simplified, using keywords and entities)
    skills = [ent.text for ent in doc.ents if ent.label_ in ["SKILL", "ORG", "PRODUCT"]]
    skills = list(set(skills))  # Remove duplicates
    
    # Extract experience (placeholder: use regex or patterns for real projects)
    experience = [Experience(
        title="Sample Role",
        duration="Unknown",
        responsibilities="Extracted responsibilities"
    )]
    
    # Extract education (simplified)
    education = " ".join([chunk.text for chunk in doc.noun_chunks if "degree" in chunk.text.lower() or "university" in chunk.text.lower()])
    
    # Save to MongoDB
    parsed_resume = ParsedResume(
        user_id=user_id,
        skills=skills,
        experience=experience,
        education=education,
        certifications=[],
        match_scores=[],
        feedback=""
    )
    parsed_resume.save()
    
    return parsed_resume

def extract_text(file_path):
    """Extract text from PDF, DOCX, or TXT files."""
    text = ""
    if file_path.endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        except Exception as e:
            print(f"Error reading PDF: {e}")
            raise
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = " ".join(paragraph.text for paragraph in doc.paragraphs)
    elif file_path.endswith(".txt"):  # Added fallback for text files
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX, or TXT.")
    return text