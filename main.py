from pathlib import Path

from src.extraction.reader import load_all_resumes
from src.extraction.regex_extractor import process_resume_to_short_cv  # Tu extractor Regex

# 1. Cargar datos
data = load_all_resumes("data/raw_data")

# 2. Preparar la carpeta de salida
processed_dir = Path("data/processed")
processed_dir.mkdir(parents=True, exist_ok=True)

# 3. Procesar y guardar cada CV
for file_name, content in data.items():
    short_cv = process_resume_to_short_cv(content)
    output_path = processed_dir / f"{Path(file_name).stem}_processed.txt"
    output_path.write_text(short_cv["short_cv_text"], encoding="utf-8")

    print(f"Archivo: {file_name}")
    print(f"Processed CV guardado en: {output_path}")
    print("Extracted Short CV:")
    print(short_cv)