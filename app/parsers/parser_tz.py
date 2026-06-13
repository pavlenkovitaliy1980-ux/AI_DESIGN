from pathlib import Path
import json
import pdfplumber
from docx import Document


BASE_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BASE_DIR / "projects" / "demo_project"

INPUT_DIR = PROJECT_DIR / "input"
PARSED_DIR = PROJECT_DIR / "parsed"
LOGS_DIR = PROJECT_DIR / "logs"


def extract_text_from_pdf(file_path: Path) -> str:
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_path: Path) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return extract_text_from_pdf(file_path)

    if suffix == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")


def save_log(message: str):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOGS_DIR / "parser_tz.log", "a", encoding="utf-8") as f:
        f.write(message + "\n")
def main():
    PARSED_DIR.mkdir(parents=True, exist_ok=True)

    files = list(INPUT_DIR.glob("*.pdf")) + list(INPUT_DIR.glob("*.docx"))

    if not files:
        msg = "Нет входных файлов ТЗ"
        print(msg)
        save_log(msg)
        return

    source_file = files[0]

    try:
        text = extract_text(source_file)

        result = {
            "source_file": source_file.name,
            "systems": [],
            "floors": None,
            "preview": text[:3000]
        }

        out = PARSED_DIR / "tz_parsed.json"
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        msg = f"OK → {out}"
        print(msg)
        save_log(msg)

    except Exception as e:
        err = f"Ошибка: {e}"
        print(err)
        save_log(err)


if __name__ == "__main__":
    main()