import time
import speech_recognition as sr  # Добавлено для распознавания речи
from ttsstt import text_to_speach, to_wav
from llm import gemini_query
from a2fhandlers import A2FHandlers
from mic import listen_from_microphone

def main():
    
    a2f_instance_path = "/World/audio2face/CoreFullface"
    
    # Получаем текст из микрофона
    while True:
        user_query = listen_from_microphone()
    
        if user_query is None:
            print("Не удалось получить запрос от пользователя.")
            return

        # Замеряем время выполнения запроса к LLM
        start_time = time.time()
        llm_response: str = gemini_query(user_query=user_query)
        llm_time = time.time() - start_time
        print(f"Время выполнения запроса к LLM: {llm_time:.2f} секунд")

        # Замеряем время преобразования текста в речь
        start_time = time.time()
        text_to_speach(user_message=llm_response)
        to_wav("output.mp3")
        tts_time = time.time() - start_time
        print(f"Время преобразования текста в речь: {tts_time:.2f} секунд")

        a2f_player_path = "/World/audio2face/Player"
        a2fHandler = A2FHandlers(host_url="http://localhost:8011/")

        a2fHandler.set_root_path(a2f_player=a2f_player_path)

        start_time = time.time()
        a2fHandler.remove_keys(a2f_instance=a2f_instance_path)
        remove_keys_time = time.time() - start_time
        print(f"Время удаления ключей: {remove_keys_time:.2f} секунд")

        start_time = time.time()
        a2fHandler.set_root_path(a2f_player=a2f_player_path)
        set_root_time = time.time() - start_time
        print(f"Время установки корневого пути: {set_root_time:.2f} секунд")
        
        # Замеряем время установки трека
        start_time = time.time()
        a2fHandler.set_track(a2f_player=a2f_player_path, file_name="output.wav")
        set_track_time = time.time() - start_time
        print(f"Время установки трека: {set_track_time:.2f} секунд")
        
        # Замеряем время воспроизведения
        start_time = time.time()
        a2fHandler.play(a2f_player=a2f_player_path)
        play_time = time.time() - start_time
        print(f"Время воспроизведения: {play_time:.2f} секунд")

if __name__ == '__main__':
    main()
