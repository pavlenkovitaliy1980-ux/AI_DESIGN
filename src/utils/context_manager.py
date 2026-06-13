import json
from pathlib import Path


class ProjectContext:
    def __init__(self, path="data/structured/project_context.json"):
        self.path = Path(path)
        self.data = self._load()

    def _load(self):
        if not self.path.exists():
            raise FileNotFoundError(f"Context file not found: {self.path}")
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        print(f"[SAVE] Запись в файл: {self.path}")
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def reload(self):
        self.data = self._load()
        return self.data

    def update(self, section, key, value):
        if section not in self.data:
            raise KeyError(f"Section '{section}' not found")
        self.data[section][key] = value
        self.save()

    def get(self, section, key=None):
        if section not in self.data:
            raise KeyError(f"Section '{section}' not found")
        if key is None:
            return self.data[section]
        return self.data[section].get(key)

    def add_to_list(self, section, key, value):
        if section not in self.data:
            raise KeyError(f"Section '{section}' not found")

        if key not in self.data[section]:
            self.data[section][key] = []

        if not isinstance(self.data[section][key], list):
            raise TypeError(f"{section}.{key} is not a list")

        if value not in self.data[section][key]:
            self.data[section][key].append(value)
            self.save()