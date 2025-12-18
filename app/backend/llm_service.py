import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import json
from typing import Dict, Type, Any, Optional
import asyncio
import re

from pydantic import BaseModel, create_model, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.backend.models import get_llm
from app.backend.scraper_service import scrape_url

from app.backend.prompts import SCHEMA_GEN_SYSTEM_PROMPT, SCHEMA_GEN_USER_PROMPT

type_map = {
    'int' : int,
    'float' : float,
    'bool' : bool,
    'str' : str,
    'list' : list,
    'dict' : dict
}

schema_prompt = PromptTemplate.from_template(SCHEMA_GEN_SYSTEM_PROMPT + " " + SCHEMA_GEN_USER_PROMPT)

def generate_json_schema(input_request : str):
    llm = get_llm()
    chain = schema_prompt | llm | JsonOutputParser()
    result = chain.invoke({'user_prompt' : input_request})
    return result

def map_datatype(type_str: str):
    type_str = type_str.lower().strip()
    return type_map.get(type_str, str)

def format_json(input_schema : Dict):
    schema = {}
    for key, value in input_schema.items():
        schema[key] = (map_datatype(value), ...)
    
    return schema

def get_pydantic_model(schema):
    model = create_model("JSON_SCHEMA" , **schema)

    return model


def extract_json_from_markdown(text: str) -> str:
    pattern = r"^```(?:json)?\s*|\s*```$"
    return re.sub(pattern, "", text, flags=re.MULTILINE | re.IGNORECASE).strip()

def generate_dynamic_pydantic_model(user_prompt: str):
    json_schema = generate_json_schema(user_prompt)
    formatted_schema = format_json(json_schema)
    print(f"[backend] Formatted Schema : {formatted_schema}")
    return get_pydantic_model(formatted_schema)




if __name__ == "__main__":
    extracted_content = scrape_url(url="https://webscraper.io/test-sites/e-commerce/allinone")
    llm_output = generate_json_schema("I want to extract names of the products")
    formatted_schema = format_json(llm_output)
    print(f"Formatted Schema : {formatted_schema}")
    pydantic_model = get_pydantic_model(formatted_schema)

    fields = pydantic_model.model_fields 
 
    print("Field Names:", list(fields.keys()))

    for name, field_info in fields.items():
        print(f"Field: {name}, Type: {field_info.annotation}")




