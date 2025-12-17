import json
from typing import Dict, Type, Any, Optional

from pydantic import BaseModel, create_model, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models import Openrouter_LLM

type_map = {
    'int' : int,
    'float' : float,
    'bool' : bool,
    'str' : str,
    'list' : list,
    'dict' : dict
}

SYSTEM_PROMPT = """
You are an expert data schema architect. 
Your task is to convert a user's natural language request for data extraction into a JSON schema definition.
Analyze the user's request and identify the specific fields they want to extract.
For each field, determine the most appropriate Python data type: 'str', 'int', 'float', 'bool', or 'list'.

Output strictly a JSON object where keys are field names and values are the data types.
Do NOT include any markdown formatting, ```json blocks, or explanatory text. Just the raw JSON.

Example Input: "I want the product title, current price, and a list of features."
Example Output:
{{
    "product_title": "str",
    "current_price": "float",
    "features": "list"
}}
"""

USER_PROMPT = "User Request to extract fields: {user_prompt}"

schema_prompt = PromptTemplate.from_template(SYSTEM_PROMPT + " " + USER_PROMPT)

def generate_json_schema(input_request : str):
    chain = schema_prompt | Openrouter_LLM | JsonOutputParser()
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

def generate_pydantic_model(input_request : str):
    schema = generate_json_schema(input_request)
    if not schema or schema.strip() == "":
        print("[Backend] Error: Empty Schema from LLM")

    formatted_schema = format_json(schema)
    pydantic_model = get_pydantic_model(formatted_schema)

    return pydantic_model

if __name__ == "__main__":
    # Simulate the LLM output for testing
    llm_output = generate_json_schema("I want to extract name , age and email address.")
    print(f"LLM Schema : {llm_output}")
    print("="*40)
    formatted_schema = format_json(llm_output)
    print(f"Formatted Schema : {formatted_schema}")
    print("="*40)
    pydantic_model = get_pydantic_model(formatted_schema)
    print(f"Pydantic Schema : {pydantic_model}")
    print("="*40)

    user_data = {'name' : 'Om', 'age' : 19, 'email_address' : 'om@example.com'}
    try:
        instance = pydantic_model.model_validate(user_data)
        print(instance)
        print("Model validated successfully !")
    except Exception as e:
        print(f"Error : {e}")

