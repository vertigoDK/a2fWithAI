import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

def gemini_query(user_query: str) -> str:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(f"ОТВЕЧАЙ КАК МОЖНО КРАТЧЕ ОТВЕЧАЙ БЕЗ ЭМОДЗИ:\n Запрос {user_query}")

    return response.text

if __name__ == '__main__':
    result: str =  gemini_query('привет как твои дела?')
    print(result)