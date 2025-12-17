from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

OPENROUTER_API_KEY= os.getenv('OPENROUTER_API_KEY')
BASE_URL= os.getenv('BASE_URL')

available_models = [
    {'deepseek-r1:1.5b' : '1.1'},
    {'qwen2.5:3b' : '1.9'},
    {'qwen3:4b' : '2.5'},
    {'mistral:7b' : '4.4'}
]


model = ChatOllama(
    model='deepseek-r1:1.5b',
    temperature=1.0,
    base_url="http://127.0.0.1:11434"
)

Openrouter_LLM = ChatOpenAI(
    model='xiaomi/mimo-v2-flash:free',
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
    temperature=1.0,
    default_headers={
        "HTTP-Referer": "http://localhost",   
        "X-Title": "Web Scraping"
        }
)

Google_LLM = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=1.0
)

input = "What is Langchain ?"

def test(input : str, model):
    """
    Tests the connection to a given LLM model.
    
    Args:
        input (str): The prompt message to send to the model.
        model (BaseChatModel): The LangChain chat model instance to test.
        
    Returns:
        None: Prints the model response or error message to stdout.
    """
    if model.invoke(input).content:
        print(model.invoke(input).content)
        print("Model loaded successfully !")
    else:
        print("Error loading model !")


if __name__ == "__main__":
    test(input, Openrouter_LLM)