from pathlib import Path
import json
import re
import requests

BASE_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BASE_DIR / "projects" / "demo_project"

INPUT_JSON = PROJECT_DIR / "parsed" / "tz_parsed.json"
OUTPUT_JSON = PROJECT_DIR / "parsed" / "tz_ai_parsed.json"
LOG_FILE = PROJECT_DIR / "logs" / "parser_tz_ai.log"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"


def log(message: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(message + "\n")


def clean_model_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def normalize_result(data: dict) -> dict:
    systems = data.get("systems", [])

    if isinstance(systems, str):
        systems = [item.strip() for item in systems.split(",") if item.strip()]

    floors = data.get("floors")
    if isinstance(floors, str) and floors.lower() in ["не указано", "unknown", "null", "none", ""]:
        floors = None

    return {
        "document_type": data.get("document_type"),
        "customer": data.get("customer"),
        "object_name": data.get("object_name"),
        "address": data.get("address"),
        "systems": systems,
        "floors": floors,
    }


def main() -> None:
    try:
        if not INPUT_JSON.exists():
            print("Нет tz_parsed.json")
            return

        source_data = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
        text = source_data.get("preview", "")

        prompt = f"""
Ты инженер-проектировщик.
Извлеки данные из ТЗ и верни строго JSON без пояснений.

Требования:
- systems должен быть массивом строк
- floors должен быть числом или null
- никаких markdown-блоков
- никакого текста вне JSON

Поля:
document_type
customer
object_name
address
systems
floors

Текст:
{text}
"""

        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        result = r.json()

        if "response" not in result:
            msg = f"Нет ключа response: {result}"
            print(msg)
            log(msg)
            return

        raw_response = result["response"]
        cleaned = clean_model_json(raw_response)
        parsed = json.loads(cleaned)
        normalized = normalize_result(parsed)

        OUTPUT_JSON.write_text(
            json.dumps(normalized, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        print(f"OK -> {OUTPUT_JSON}")
        log(f"OK -> {OUTPUT_JSON}")

    except Exception as e:
        print("Ошибка:", e)
        log(f"Ошибка: {e}")


if __name__ == "__main__":
    main()