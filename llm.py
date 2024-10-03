import google.generativeai as genai
from dotenv import load_dotenv
import os
from settings import Settings
from typing import Dict, Union

load_dotenv()


context_history = []

def load_knowledge_base(file_path='data.txt'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            knowledge_base = file.read()
        return knowledge_base
    except FileNotFoundError:
        return "База знаний не найдена."

knowledge_base = load_knowledge_base()

def gemini_query(user_query: str, settings: Settings) -> str:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    current_settings: dict = settings.get_settings()
    model = genai.GenerativeModel(model_name=current_settings['model_name'])

    context_history.append(f"Запрос: {user_query}")
    
    response = model.generate_content(f"""{current_settings['system_prompt']}
    Контекст предыдущих сообщений:
    {generate_context()}
    
    База знаний:
    
    --------------------------------
    
    {knowledge_base}
    
    --------------------------------
    
    Новый запрос: {user_query}""")

    context_history.append(f"Ответ: {response.text.strip()}") 

    return response.text

def generate_context() -> str:
    return "\n".join(context_history[-10:])

if __name__ == '__main__':
    result: str = gemini_query('привет')
    print(result)
