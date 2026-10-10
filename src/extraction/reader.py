# src/extraction/reader.py
from pathlib import Path

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


def load_all_resumes(data_dir: str = "data/raw_data") -> dict:
    path = Path(data_dir)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró la carpeta: {data_dir}")

    resumes = {}
    files = sorted([f for f in path.iterdir() if f.suffix.lower() in [".txt", ".pdf"]])# puede leer pdfs o txt

    for file_path in files:
        if file_path.suffix.lower() == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                resumes[file_path.name] = f.read()
        elif file_path.suffix.lower() == ".pdf" and PYPDF_AVAILABLE:
            reader = PdfReader(file_path)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            resumes[file_path.name] = text

    return resumes