import json
from typing import List

class Settings:

    def __init__(self):
        self._model_name: str = "gemini-1.5-flash"
        self._model_temperature: int = 0
        self._additional_data_path: List[str] = []
        self._system_prompt: str = ""

    def get_settings(self):
        return {
            "model_name": self._model_name,
            "model_temperature": self._model_temperature,
            "additional_data_path": self._additional_data_path,
            "system_prompt": self._system_prompt,
        }

    def save_settings(self, file_path: str):
        """Сохранить настройки в файл."""
        with open(file_path, 'w') as file:
            json.dump({
                "model_name": self._model_name,
                "model_temperature": self._model_temperature,
                "additional_data_path": self._additional_data_path,
                "system_prompt": self._system_prompt,
            }, file, indent=4)

    def load_settings(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self._model_name = data.get("model_name", self._model_name)
                self._model_temperature = data.get("model_temperature", self._model_temperature)
                self._additional_data_path = data.get("additional_data_path", self._additional_data_path)
                self._system_prompt = data.get("system_prompt", self._system_prompt)
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден. Загружены настройки по умолчанию.")
        except json.JSONDecodeError:
            print(f"Ошибка при чтении файла '{file_path}'. Убедитесь, что он в правильном формате JSON.")

if __name__ == '__main__':
    settings: Settings = Settings()

    settings.load_settings('settings.json')

    print("Текущие настройки:", settings.get_settings())

    settings.save_settings('settings.json')
