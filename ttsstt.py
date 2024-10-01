import os

from gtts import gTTS
from pydub import AudioSegment

def text_to_speach(user_message: str):

    tts = gTTS(user_message, lang='ru')

    tts.save("output.mp3")

def to_wav(path_to_mp3: str):
    # Генерируем имя файла с расширением .wav
    path_to_wav = os.path.splitext(path_to_mp3)[0] + ".wav"
    
    # Загружаем MP3
    audio = AudioSegment.from_mp3(path_to_mp3)
    
    # Экспортируем как WAV
    audio.export(path_to_wav, format="wav")
    print(f"Файл сохранен как {path_to_wav}")

if __name__ == '__main__':
    to_wav(path_to_mp3="output.mp3")