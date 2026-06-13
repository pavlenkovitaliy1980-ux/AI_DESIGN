from src.utils.context_manager import ProjectContext

ctx = ProjectContext()

ctx.update("object_info", "object_name", "ЖК Северный")
ctx.update("object_info", "stage", "ПД")
ctx.add_to_list("design_scope", "systems_requested", "АПС")
ctx.add_to_list("design_scope", "systems_requested", "СОТ")

print("Название объекта:", ctx.get("object_info", "object_name"))
print("Стадия:", ctx.get("object_info", "stage"))
print("Системы:", ctx.get("design_scope", "systems_requested"))