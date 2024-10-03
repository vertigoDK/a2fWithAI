import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Храним последние 10 сообщений в глобальной переменной
context_history = []

# Функция для чтения базы знаний из файла
def load_knowledge_base(file_path='data.txt'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            knowledge_base = file.read()
        return knowledge_base
    except FileNotFoundError:
        return "База знаний не найдена."

# Читаем базу знаний при запуске
knowledge_base = load_knowledge_base()

def gemini_query(user_query: str) -> str:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Добавляем новое сообщение пользователя в историю
    context_history.append(f"Запрос: {user_query}")
    
    # Генерируем ответ AI
    response = model.generate_content(f"""Ответ должен быть кратким, без знаков препинания, специальных символов и пояснений в скобках, так как текст будет озвучиваться. Пожалуйста, выводите только то, что должно быть произнесено, без лишних символов.
    ОТВЕЧАЙ КАК МОЖНО КРАТЧЕ БЕЗ ЭМОДЗИ, используй контекст и базу знаний что бы давать как можно более релеватные ответ:
    Контекст предыдущих сообщений:
    {generate_context()}
    
    База знаний:
    
    --------------------------------
    
    {knowledge_base}
    
    --------------------------------
    
    Новый запрос: {user_query}""")

    # Добавляем ответ AI в историю
    context_history.append(f"Ответ: {response.text.strip()}")  # Добавляем ответ без лишних пробелов

    return response.text

def generate_context() -> str:
    # Формируем контекст из истории
    return "\n".join(context_history[-10:])  # Ограничиваем историю 10 последними сообщениями

if __name__ == '__main__':
    result: str = gemini_query('привет')
    print(result)
