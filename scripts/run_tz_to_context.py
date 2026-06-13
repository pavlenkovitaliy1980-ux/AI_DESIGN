from src.utils.context_manager import ProjectContext
from pathlib import Path


def parse_tz_text(text: str) -> dict:
    return {
        "object_name": "ЖК Северный",
        "object_type": "Многоквартирный жилой дом",
        "stage": "ПД",
        "systems_requested": ["АПС", "СОТ", "СКУД"],
        "tz_summary": "Требуется разработать проект слаботочных систем для жилого комплекса."
    }


def main():
    # ЖЁСТКО фиксируем путь (чтобы исключить ошибки)
    context_path = Path("C:/Users/Vet2/AI_DESIGN/data/structured/project_context.json")

    ctx = ProjectContext(path=context_path)

    print("📂 Работаем с файлом:", ctx.path)

    tz_text = "Пример текста технического задания"
    parsed = parse_tz_text(tz_text)

    ctx.update("object_info", "object_name", parsed["object_name"])
    ctx.update("object_info", "object_type", parsed["object_type"])
    ctx.update("object_info", "stage", parsed["stage"])
    ctx.update("parsed_data", "tz_summary", parsed["tz_summary"])

    existing_systems = ctx.get("design_scope", "systems_requested") or []
    for system in parsed["systems_requested"]:
        if system not in existing_systems:
            ctx.add_to_list("design_scope", "systems_requested", system)
            existing_systems.append(system)

    ctx.update("generation_flags", "tz_parsed", True)

    print("✅ ТЗ успешно записано в project_context.json")


if __name__ == "__main__":
    main()