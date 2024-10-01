import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

def gemini_query(user_query: str) -> str:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
    context = """\
1. Название: Библиотека имени Оралхана Бокея
2. Год основания: 1995
3. Основатель: Айдархан Каирбеков
4. Миссия: Доступ к культурному наследию Казахстана
5. Количество пользователей: 20,000 зарегистрированных, 3,000 ежемесячных
6. Проект "Цифровой Казахстан": оцифровка культурного наследия
7. Веб-сайт: www.bokei-library.kz
"""
    response = model.generate_content(f"""ОТВЕЧАЙ КАК МОЖНО КРАТЧЕ БЕЗ ЭМОДЗИ:
    CONTEXT: {context}
    Запрос: {user_query}""")

    return response.text

if __name__ == '__main__':
    result: str = gemini_query('кто такой Илон Маск?')
    print(result)
