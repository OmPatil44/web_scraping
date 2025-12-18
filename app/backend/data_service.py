import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from langchain.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from typing import Optional, Dict
import asyncio
import os
import pandas as pd
from typing import List, Dict, Any
import json

from app.backend.scraper_service import scrape_url
from app.backend.llm_service import generate_dynamic_pydantic_model
from app.backend.models import get_llm
from app.backend.prompts import DATA_EXTRACTION_AGENT_PROMPT, EXTRACTION_USER_PROMPT

SystemPrompt = SystemMessage(DATA_EXTRACTION_AGENT_PROMPT)

def save_to_csv(data: List[Dict[str, Any]], filename: str = "extracted_data.csv"):
    try:
        # Use absolute path for robustness, or relative to current working directory in a cross-platform way
        output_dir = os.path.join("data", "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filepath = os.path.join(output_dir, filename)
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        print(f"[Data Service] Data saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"[Data Service] CSV Save Error: {e}")
        return None

def generate_agent_data(content: str, user_prompt: str):
    """
    Generates data using a ReAct agent approach.
    """
    try:
     
        full_prompt = f"{EXTRACTION_USER_PROMPT}\n{content}\n\nUser Request: {user_prompt}"
        
        model = create_react_agent(
            model=get_llm(),
            tools=[],
            prompt=SystemPrompt
        )   
        result = model.invoke({'messages': [HumanMessage(content=full_prompt[:30000])]})
        
        if result and 'messages' in result and result['messages']:
            return result['messages'][-1].content
        else:
            return "No result generated."
            
    except Exception as e:
        print(f"[Data Service] Agent Execution Error: {e}")
        return None

async def run_pipeline(url: str, user_prompt: str): 
    print("[backend] Scraping...")
    content = await scrape_url(url)
    if not content:
        print("Scraping failed.")
        return
        
    print("[backend] Schema Generation...")
    model = generate_dynamic_pydantic_model(user_prompt)
    if model:
        print("[backend] Schema generated successfully.")

    print("[backend] Extraction...")
    extracted_text = generate_agent_data(content, user_prompt)
    try:
        cleaned_text = extracted_text.strip()
        if "```json" in cleaned_text:
            cleaned_text = cleaned_text.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_text:
            cleaned_text = cleaned_text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(cleaned_text)
            
        print(f"[backend] Extracted Data Type: {type(data)}")
        
        final_data = []
        
        if isinstance(data, list):
            final_data = data
        elif isinstance(data, dict):
            if all(k.isdigit() for k in data.keys()):
                 final_data = list(data.values())
            elif len(data) == 1 and isinstance(list(data.values())[0], list):
                final_data = list(data.values())[0]
            else:  
                final_data = [data]
        
        print(f"[backend] Final Data for CSV: {final_data}")


        if final_data and not isinstance(final_data[0], dict):
             final_data = [{"value": item} for item in final_data]

        save_to_csv(final_data)
        return final_data
    except Exception as e:
        print(f"JSON Parsing/Saving Error: {e}")
        print(f"Raw Content: {extracted_text}")
        return None
     

if __name__ == "__main__":
    # Test Run
    url = "https://huggingface.co/models"
    prompt = "List all the llm names along with their last updated date."
    asyncio.run(run_pipeline(url, prompt))