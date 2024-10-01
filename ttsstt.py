import os

from gtts import gTTS
from pydub import AudioSegment

def text_to_speach(user_message: str):

    tts = gTTS(user_message, lang='ru')

    tts.save("output.mp3")

def to_wav(path_to_mp3: str):
    # Создаем папку audiofiles, если она не существует
    output_dir = "audiofiles"
    os.makedirs(output_dir, exist_ok=True)

    # Генерируем имя файла с расширением .wav в папке audiofiles
    path_to_wav = os.path.join(output_dir, os.path.splitext(os.path.basename(path_to_mp3))[0] + ".wav")
    
    # Загружаем MP3
    audio = AudioSegment.from_mp3(path_to_mp3)
    
    # Экспортируем как WAV
    audio.export(path_to_wav, format="wav")
    print(f"Файл сохранен как {path_to_wav}")

if __name__ == '__main__':
    text_to_speach("привет сколько будет 20 + 52")
    to_wav(path_to_mp3="output.mp3")