from langchain.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from typing import Optional, Dict

import asyncio
import os
import pandas as pd
from typing import List, Dict, Any

from scraper_service import scrape_url
from llm_service import generate_dynamic_pydantic_model
from models import Openrouter_LLM
from prompts import DATA_EXTRACTION_AGENT_PROMPT, EXTRACTION_USER_PROMPT

SystemPrompt = SystemMessage(DATA_EXTRACTION_AGENT_PROMPT)

def save_to_csv(data: List[Dict[str, Any]], filename: str = "extracted_data.csv"):
    try:
        output_dir = "data/output"
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
            model=Openrouter_LLM,
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
    print(f"--- Pipeline Started ---\n\nURL: {url}\n\nPrompt: {user_prompt}")
    # 1. Scrape
    print("Scraping...")
    content = await scrape_url(url)
    if not content:
        print("Scraping failed.")
        return
        

    print("Schema Generation (Verification)...")
    model = generate_dynamic_pydantic_model(user_prompt)
    if model:
        print("Schema generated successfully.")


    print("Extraction...")
    extracted_text = generate_agent_data(content, user_prompt)
    print(f"Extracted Data: {extracted_text}")

    import json
    try:

        if "```json" in extracted_text:
            json_str = extracted_text.split("```json")[1].split("```")[0].strip()
            data = json.loads(json_str)
        elif "```" in extracted_text:
             json_str = extracted_text.split("```")[1].split("```")[0].strip()
             data = json.loads(json_str)
        else:
            data = json.loads(extracted_text)
            
        save_to_csv([data] if isinstance(data, dict) else data)
    except:
        print("Could not parse JSON for CSV saving. Saving raw text.")
     

if __name__ == "__main__":
    # Test Run
    url = "https://webscraper.io/test-sites/e-commerce/allinone"
    prompt = "Extract product names and prices"
    asyncio.run(run_pipeline(url, prompt))