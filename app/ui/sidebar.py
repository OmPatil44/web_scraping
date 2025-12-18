import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
import requests

def validate_key(provider, api_key, model_name):
    try:
        if str(provider).strip().lower() == "openrouter api":
            # For validation, we use a temporary instance
            llm = ChatOpenAI(
                model=model_name,
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=1.0,
                default_headers={
                    "HTTP-Referer": "http://localhost",   
                    "X-Title": "Web Scraping"
                }
            )
        elif str(provider).strip().lower() == "gemini api":
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
        
        if len(llm.invoke([HumanMessage(content="Hi")]).content) >= 1:
            return True
        else:
            return False
    except Exception as e:
        return False

def render_sidebar():
    st.sidebar.markdown("# Configuration")

    provider = st.sidebar.selectbox(
        "LLM Provider",
        ("Ollama", "OpenRouter API", "Gemini API"),
        placeholder="Choose LLM Provider..."
    )

    api_key = None
    is_valid = False
    
    if 'llm_provider' not in st.session_state:
        st.session_state['llm_provider'] = provider

    if not str(provider).strip().lower() == "ollama":
        if str(provider).strip().lower() == "openrouter api":
            api_key = st.sidebar.text_input(label="OpenRouter API Key", type='password', placeholder="Enter API Key")
            model_name = st.sidebar.text_input(label="OpenRouter Model", placeholder="Enter Model Name (e.g. xiaomi/mimo-v2-flash:free)", value="xiaomi/mimo-v2-flash:free")
            
            if api_key and model_name:
                if validate_key(provider, api_key, model_name):
                    st.session_state['OPENROUTER_API_KEY'] = str(api_key)
                    st.session_state['OPENROUTER_MODEL'] = str(model_name)
                    os.environ['OPENROUTER_API_KEY'] = str(api_key)
                    os.environ['LLM_PROVIDER'] = "OpenRouter API"
                    os.environ['OPENROUTER_MODEL'] = str(model_name)
                    os.environ['BASE_URL'] = "https://openrouter.ai/api/v1" 
                    st.sidebar.success("Validated API Key", icon="🚀")
                    is_valid = True
                else:
                    st.sidebar.warning("Invalid API key or Model Name", icon="☢️")
        
        elif str(provider).strip().lower() == "gemini api" :
            api_key = st.sidebar.text_input(label="Gemini API Key", type='password', placeholder="Enter API Key")
            model_name = st.sidebar.text_input(label="Gemini Model", placeholder="Enter Model Name (e.g. gemini-2.5-flash)", value="gemini-2.5-flash")
            
            if api_key and model_name:
                if validate_key(provider, api_key, model_name):
                    st.session_state['GOOGLE_API_KEY'] = str(api_key)
                    st.session_state['GEMINI_MODEL'] = str(model_name)
                    os.environ['GOOGLE_API_KEY'] = str(api_key)
                    os.environ['LLM_PROVIDER'] = "Gemini API"
                    os.environ['GEMINI_MODEL'] = str(model_name)
                    
                    st.sidebar.success("Validated API Key", icon="🚀")
                    is_valid = True
                else:
                    st.sidebar.warning("Invalid API key or Model Name", icon="☢️")
            
    else:
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            response.raise_for_status()  
            data = response.json()

            models_list = []
            for m in data['models']:
                models_list.append(m['name'])
                
            if not models_list:
                st.sidebar.warning("Ollama is running, but no models found.", icon="☢️")
                models_list = ["No models available"]
            
            selected_model = st.sidebar.selectbox(
                label="Select local model",
                options=models_list,
                index=0,
                key="ollama_model_selector" 
            )
            
            if selected_model and selected_model != "No models available":
                is_valid = True
                st.session_state['OLLAMA_MODEL'] = selected_model
                os.environ['LLM_PROVIDER'] = "Ollama"
                os.environ['OLLAMA_MODEL'] = selected_model

        except requests.exceptions.ConnectionError:
            st.sidebar.error("Cannot connect to Ollama.", icon="🔌")
        except Exception as e:
            st.sidebar.error(f"Error: {e}", icon="⚠️")

    return api_key, provider, is_valid
        