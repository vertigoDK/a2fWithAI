import time
import customtkinter as ctk
from ttsstt import text_to_speach, to_wav
from llm import gemini_query
from a2fhandlers import A2FHandlers
import threading
import speech_recognition as sr
from settings import Settings

class SpeechRecognitionApp:
    def __init__(self, root):
        self._settings = Settings()
        
        self.root = root
        self.root.title("Speech Recognition App")
        self.root.geometry("600x400")


        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Заголовок
        self.label = ctk.CTkLabel(root, text="Нажмите на кнопку и говорите", font=("Arial", 16))
        self.label.pack(pady=20)

        # Поле для отображения распознанного текста
        self.textbox = ctk.CTkTextbox(root, width=500, height=100, state="disabled", wrap="word")
        self.textbox.pack(pady=10)

        # Кнопка для начала прослушивания
        self.listen_button = ctk.CTkButton(root, text="Начать прослушивание", command=self.start_listening)
        self.listen_button.pack(pady=10)

        # Кнопка выхода
        self.exit_button = ctk.CTkButton(root, text="Выход", command=root.quit)
        self.exit_button.pack(pady=10)

        # Поле для отображения отладочной информации
        self.debug_box = ctk.CTkTextbox(root, width=500, height=150, state="disabled", wrap="word")
        self.debug_box.pack(pady=20)

    def listen_from_microphone(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            self.label.configure(text="Слушаю... говорите")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            self.label.configure(text="Распознаю речь...")
            query = recognizer.recognize_google(audio, language="ru-RU")
            self.label.configure(text="Распознано:")
            return query
        except sr.UnknownValueError:
            self.label.configure(text="Не удалось распознать речь")
            self.log_debug("Ошибка: Не удалось распознать речь.")
            return None
        except sr.RequestError as e:
            self.label.configure(text=f"Ошибка сервиса распознавания речи: {e}")
            self.log_debug(f"Ошибка: {e}")
            return None

    def start_listening(self):
        self.listen_button.configure(state="disabled")
        self.textbox.configure(state="normal")
        self.textbox.delete(1.0, "end")

        def listen_and_update():
            user_query = self.listen_from_microphone()
            if user_query:
                self.textbox.insert("1.0", user_query)
                self.process_query(user_query)  # Обработка запроса пользователя
            else:
                self.textbox.insert("1.0", "Ошибка при распознавании")

            self.listen_button.configure(state="normal")
            self.textbox.configure(state="disabled")

        threading.Thread(target=listen_and_update).start()

    def log_debug(self, message):
        self.debug_box.configure(state="normal")
        self.debug_box.insert("end", message + "\n")
        self.debug_box.configure(state="disabled")
        self.debug_box.yview("end")  # Прокрутка вниз

    def process_query(self, user_query):
        a2f_instance_path = "/World/audio2face/CoreFullface"
        a2f_player_path = "/World/audio2face/Player"
        a2fHandler = A2FHandlers(host_url="http://localhost:8011/")

        # start_time = time.time()
        # a2fHandler.remove_keys(a2f_instance=a2f_instance_path)
        # remove_keys_time = time.time() - start_time
        # self.log_debug(f"Время удаления ключей для анимации: {remove_keys_time:.2f} секунд")


        # Замеряем время выполнения запроса к LLM
        start_time = time.time()
        llm_response: str = gemini_query(user_query=user_query, settings=self._settings)
        llm_time = time.time() - start_time
        self.log_debug(f"Время выполнения запроса к LLM: {llm_time:.2f} секунд")

        # Замеряем время преобразования текста в речь
        start_time = time.time()
        text_to_speach(user_message=llm_response)
        tts_time = time.time() - start_time
        self.log_debug(f"Преобразование текста в речь: {tts_time:.2f} секунд")

        start_time = time.time()
        to_wav("output.mp3")
        wav_time = time.time() - start_time
        self.log_debug(f"Время конвертирования в WAV: {wav_time:.2f} секунд")

        start_time = time.time()
        a2fHandler.set_root_path(a2f_player=a2f_player_path)
        set_root_time = time.time() - start_time
        self.log_debug(f"Время установки корневого пути: {set_root_time:.2f} секунд")

        a2fHandler.set_track(a2f_player=a2f_player_path, file_name="output.wav")

        # Замеряем время воспроизведения
        start_time = time.time()
        a2fHandler.play(a2f_player=a2f_player_path)
        play_time = time.time() - start_time
        self.log_debug(f"Время воспроизведения: {play_time:.2f} секунд")

if __name__ == '__main__':
    root = ctk.CTk()  # Создаем объект CTk
    app = SpeechRecognitionApp(root)
    root.mainloop()  # Запускаем главный цикл