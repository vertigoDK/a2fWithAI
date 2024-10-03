import customtkinter as ctk
import asyncio
import json
from llm import gemini_query
from settings import Settings
import os

# Настройка темы и размера окна
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Chat App")
        self.geometry("800x600")  # Увеличиваем размер для правой панели

        self.settings = Settings()  # Инициализация объекта настроек

        # Основная рамка, которая делится на левую (чат) и правую (настройки) части
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Левая часть с чатом
        self.chat_frame = ctk.CTkFrame(self.main_frame)
        self.chat_frame.pack(side="left", fill="both", expand=True)

        self.chat_display = ctk.CTkTextbox(self.chat_frame, width=380, height=450, state='disabled')
        self.chat_display.pack(pady=10)

        self.message_entry = ctk.CTkEntry(self.chat_frame, placeholder_text="Type your message...", width=300)
        self.message_entry.pack(pady=10, side="left", padx=10)

        self.send_button = ctk.CTkButton(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="left")

        # Правая часть с настройками
        self.settings_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.settings_frame.pack(side="right", fill="both", expand=False, padx=10)

        # Настройки ИИ модели
        self.model_label = ctk.CTkLabel(self.settings_frame, text="Модель ИИ")
        self.model_label.pack(pady=10)

        self.model_var = ctk.StringVar(value=self.settings._model_name)  # Используем значение из настроек
        self.model_dropdown = ctk.CTkOptionMenu(self.settings_frame, variable=self.model_var,
                                                values=["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"])
        self.model_dropdown.pack(pady=10)

        # Настройка температуры
        self.temperature_label = ctk.CTkLabel(self.settings_frame, text="Температура (0 - 1)")
        self.temperature_label.pack(pady=10)

        self.temperature_frame = ctk.CTkFrame(self.settings_frame)
        self.temperature_frame.pack(pady=10)

        self.temperature_slider = ctk.CTkSlider(self.temperature_frame, from_=0, to=1, number_of_steps=10,
                                                 command=self.update_temperature_display)
        self.temperature_slider.set(self.settings._model_temperature)  # Устанавливаем значение из настроек
        self.temperature_slider.pack(side="left", padx=(0, 10))

        # Поле для ввода температуры
        self.temperature_entry = ctk.CTkEntry(self.temperature_frame, width=50)
        self.temperature_entry.insert(0, str(self.settings._model_temperature))
        self.temperature_entry.pack(side="left")

        # Системный промпт
        self.system_prompt_label = ctk.CTkLabel(self.settings_frame, text="Системный промпт")
        self.system_prompt_label.pack(pady=10)

        # Изменяем CTkEntry на CTkTextbox для многострочного ввода
        self.system_prompt_entry = ctk.CTkTextbox(self.settings_frame, height=100, width=200)
        self.system_prompt_entry.insert('1.0', self.settings._system_prompt)  # Устанавливаем значение из настроек
        self.system_prompt_entry.pack(pady=10)

        # Кнопка для сохранения настроек
        self.save_button = ctk.CTkButton(self.settings_frame, text="Сохранить настройки", command=self.save_settings)
        self.save_button.pack(pady=10)

        # Метка для вывода сообщений о сохранении
        self.save_status_label = ctk.CTkLabel(self.settings_frame, text="")
        self.save_status_label.pack(pady=10)

        # Загружаем настройки после завершения инициализации
        self.load_settings()

        # Перехват события закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_message(self):
        message = self.message_entry.get()
        if message.strip():
            self.update_chat_display(f"You: {message}\n")
            self.message_entry.delete(0, 'end')

            # Асинхронный вызов ответа от бота
            asyncio.create_task(self.bot_response(message))

    async def bot_response(self, user_message: str):
        # Пример простого ответа от бота
        response = await self.async_gemini_query(user_message, self.settings)
        self.update_chat_display(f"{response}\n")

    async def async_gemini_query(self, message: str, settings: Settings):
        return gemini_query(message, settings)  # Здесь передаем оба аргумента в gemini_query

    def update_chat_display(self, message):
        # Разблокируем текстовое поле для добавления сообщений
        self.chat_display.configure(state='normal')
        self.chat_display.insert(ctk.END, message + "\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(ctk.END)

    def update_temperature_display(self, value):
        # Обновляем текстовое поле для отображения значения температуры
        self.temperature_entry.delete(0, ctk.END)
        self.temperature_entry.insert(0, f"{value:.1f}")

    def save_settings(self):
        # Обновляем настройки перед сохранением
        self.settings._model_name = self.model_var.get()
        self.settings._model_temperature = self.temperature_slider.get()
        self.settings._system_prompt = self.system_prompt_entry.get("1.0", ctk.END).strip()  # Получаем текст из текстового поля

        # Сохранение настроек в settings.json
        self.settings.save_settings("settings.json")
        self.save_status_label.configure(text="Настройки сохранены.")

    def load_settings(self):
        if os.path.exists("settings.json"):
            self.settings.load_settings("settings.json")

            # Обновляем поля настройки в интерфейсе
            self.model_var.set(self.settings._model_name)
            self.temperature_slider.set(self.settings._model_temperature)
            self.temperature_entry.delete(0, ctk.END)
            self.temperature_entry.insert(0, str(self.settings._model_temperature))
            self.system_prompt_entry.delete("1.0", ctk.END)
            self.system_prompt_entry.insert("1.0", self.settings._system_prompt)

    def on_close(self):
        self.destroy()  # Завершаем работу приложения

# Запускаем приложение
if __name__ == "__main__":
    app = ChatApp()
    app.mainloop() 