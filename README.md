# a2fWithAI

Этот проект позволяет взаимодействовать с Audio2Face от NVIDIA в Omniverse с помощью голосовых команд.  Он использует Google AI для распознавания речи и отправляет полученный текст в Audio2Face для анимации лица.

## Требования

* NVIDIA Omniverse
* NVIDIA Audio2Face
* Видеокарта NVIDIA RTX
* Python 3.7+

## Установка

1. Установите Omniverse и Audio2Face, следуя инструкциям на официальном сайте NVIDIA.
2. Клонируйте этот репозиторий: `git clone https://github.com/vertigoDK/a2fWithAI.git`
3. Установите необходимые зависимости: `pip install -r requirements.txt`
4. Создайте файл `.env` в корневой директории проекта и скопируйте содержимое из `EXAMPLE.env`.
5. Получите ваш `GOOGLE_API_KEY` на [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) и вставьте его в файл `.env`.
6. Настройте пути в файле `conf.py`:
    * `a2f_instance_path`: Путь к экземпляру Audio2Face.  Его можно найти, перейдя по ссылке [http://127.0.0.1:8011/A2F/GetInstances](http://127.0.0.1:8011/A2F/GetInstances) и скопировав значение из `fullface_instances`.  Например: `/World/audio2face/CoreFullface`.
    * `a2f_player_path`: Путь к плееру Audio2Face.  Его можно получить, кликнув на меш в Omniverse и скопировав путь. Например: `/World/audio2face/Player`.

## Использование

1. Запустите скрипт: `python main.py`
2. Нажмите на кнопку в интерфейсе, чтобы начать запись вашего голоса.
3. Задайте свой вопрос или произнесите фразу.  Скрипт распознает вашу речь, отправит текст в Audio2Face и анимирует лицо персонажа.
