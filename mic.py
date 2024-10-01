import time
import speech_recognition as sr  # Добавлено для распознавания речи
from ttsstt import text_to_speach, to_wav
from llm import gemini_query
from a2fhandlers import A2FHandlers

def listen_from_microphone():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Слушаю... говорите:")
        recognizer.adjust_for_ambient_noise(source)  # Настройка на уровень окружающего шума
        # Используем timeout для ограничения молчания и максимального времени ожидания
        audio = recognizer.listen(source)  # Завершается, если тишина более 2 секунд

    try:
        print("Распознаю речь...")
        query = recognizer.recognize_google(audio, language="ru-RU")  # Используем Google Speech Recognition API
        print(f"Вы сказали: {query}")
        return query
    except sr.UnknownValueError:
        print("Не удалось распознать речь")
        return None
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи: {e}")
        return None
    
if __name__ == '__main__':
    while True:
        print(listen_from_microphone())
