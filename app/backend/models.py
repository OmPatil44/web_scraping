import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

def get_openrouter_llm():
    api_key = os.getenv('OPENROUTER_API_KEY')
    base_url = os.getenv('BASE_URL', "https://openrouter.ai/api/v1")
    model_name = os.getenv('OPENROUTER_MODEL', 'xiaomi/mimo-v2-flash:free')
    
    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=1.0,
        default_headers={
            "HTTP-Referer": "http://localhost",   
            "X-Title": "Web Scraping"
        }
    )

def get_google_llm():
    api_key = os.getenv('GOOGLE_API_KEY')
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=1.0
    )

def get_ollama_llm():
    model_name = os.getenv('OLLAMA_MODEL', 'deepseek-r1:1.5b')
    base_url = os.getenv('OLLAMA_BASE_URL', "http://127.0.0.1:11434")
    
    return ChatOllama(
        model=model_name,
        temperature=1.0,
        base_url=base_url
    )

def get_llm():
    provider = os.getenv('LLM_PROVIDER', '').lower()
    
    if 'openrouter' in provider:
        return get_openrouter_llm()
    elif 'gemini' in provider:
        return get_google_llm()
    elif 'ollama' in provider:
        return get_ollama_llm()
    else:
        if os.getenv('OPENROUTER_API_KEY'):
            return get_openrouter_llm()
        elif os.getenv('GOOGLE_API_KEY'):
            return get_google_llm()
        else:
            return get_ollama_llm()

def test(input : str, model):
    if model.invoke(input).content:
        print(model.invoke(input).content)
        print("Model loaded successfully !")
    else:
        print("Error loading model !")


if __name__ == "__main__":
    test("What is Langchain ?", get_llm())