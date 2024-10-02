import customtkinter as ctk
import speech_recognition as sr
import threading  # Для выполнения длительных операций без блокировки интерфейса
import time
from mic import listen_from_microphone  # Функция для работы с микрофоном
from llm import gemini_query
from ttsstt import text_to_speach, to_wav
from a2fhandlers import A2FHandlers


# Создание окна приложения
class SpeechRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Recognition App")
        self.root.geometry("400x300")

        # Установка темы и размеров окна
        ctk.set_appearance_mode("System")  # Можно изменить на "Dark" или "Light"
        ctk.set_default_color_theme("blue")  # Основной цвет интерфейса

        # Текстовая метка
        self.label = ctk.CTkLabel(root, text="Нажмите на кнопку и говорите", font=("Arial", 16))
        self.label.pack(pady=20)

        # Поле для вывода распознанного текста
        self.textbox = ctk.CTkTextbox(root, width=300, height=100, state="disabled", wrap="word")
        self.textbox.pack(pady=20)

        # Кнопка для начала прослушивания
        self.listen_button = ctk.CTkButton(root, text="Начать прослушивание", command=self.start_listening)
        self.listen_button.pack(pady=10)

        # Кнопка для выхода
        self.exit_button = ctk.CTkButton(root, text="Выход", command=root.quit)
        self.exit_button.pack(pady=10)

    def start_listening(self):
        """Запуск процесса распознавания речи"""
        self.listen_button.configure(state="disabled")
        self.textbox.configure(state="normal")
        self.textbox.delete(1.0, "end")

        def listen_and_update():
            query = listen_from_microphone()  # Использование функции из mic.py
            if query:
                self.textbox.insert("1.0", query)
                self.process_llm(query)
            else:
                self.textbox.insert("1.0", "Ошибка при распознавании")

            # Возвращаем кнопке возможность быть нажатой
            self.listen_button.configure(state="normal")
            self.textbox.configure(state="disabled")

        # Запускаем процесс распознавания в отдельном потоке
        threading.Thread(target=listen_and_update).start()

    def process_llm(self, user_query):
        """Обрабатываем запрос с использованием LLM и выводим результат"""
        start_time = time.time()
        llm_response = gemini_query(user_query=user_query)
        llm_time = time.time() - start_time
        print(f"Время выполнения запроса к LLM: {llm_time:.2f} секунд")

        start_time = time.time()
        text_to_speach(user_message=llm_response)
        tts_time = time.time() - start_time
        print(f"Время преобразования текста в речь: {tts_time:.2f} секунд")

        to_wav("output.mp3")
        a2fHandler = A2FHandlers(host_url="http://localhost:8011/")
        a2fHandler.set_root_path(a2f_player="/World/audio2face/Player")
        a2fHandler.set_track(a2f_player="/World/audio2face/Player", file_name="output.wav")
        a2fHandler.play(a2f_player="/World/audio2face/Player")


if __name__ == '__main__':
    root = ctk.CTk()
    app = SpeechRecognitionApp(root)
    root.mainloop()
