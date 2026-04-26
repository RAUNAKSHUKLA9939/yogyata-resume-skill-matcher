from pdfminer.high_level import extract_text

def extract_resume_text(file):
    try:
        file.seek(0)
        return extract_text(file.file)
    except Exception:
        return ""