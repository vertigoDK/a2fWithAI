import customtkinter as ctk
import random
from llm import gemini_query


# Настройка темы и размера окна
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Chat App")
        self.geometry("400x600")

        # Текстовое поле для чата (где будут отображаться сообщения)
        self.chat_display = ctk.CTkTextbox(self, width=380, height=450, state='disabled')
        self.chat_display.pack(pady=10)

        # Поле ввода сообщения
        self.message_entry = ctk.CTkEntry(self, placeholder_text="Type your message...", width=300)
        self.message_entry.pack(pady=10, side="left", padx=10)

        # Кнопка отправки сообщения
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.pack(side="left")

    def send_message(self):
        message = self.message_entry.get()
        if message.strip():
            self.update_chat_display(f"You: {message}\n")
            self.message_entry.delete(0, 'end')

            self.bot_response(message)

    def bot_response(self, user_message: str):
        self.update_chat_display(f"{gemini_query(user_query=user_message)}\n")

    def update_chat_display(self, message):
        # Разблокируем текстовое поле для добавления сообщений
        self.chat_display.configure(state='normal')
        # Добавляем сообщение с дополнительным отступом
        self.chat_display.insert(ctk.END, message + "\n")  # Добавляем еще одну пустую строку
        # Снова блокируем, чтобы пользователь не мог вручную редактировать
        self.chat_display.configure(state='disabled')
        # Прокручиваем вниз
        self.chat_display.see(ctk.END)

# Запуск приложения
if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
