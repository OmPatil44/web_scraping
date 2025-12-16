import json
from typing import Dict, Type, Any
from pydantic import BaseModel, create_model, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models import Openrouter_LLM
from pydantic import create_model

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
    if 'int' in type_str:
        return 'int'
    elif 'float' in type_str:
        return 'float'
    elif 'bool' in type_str:
        return 'bool'
    elif 'list' in type_str:
        return 'list'
    else:
        return 'str'

def format_json(input_schema : Dict):
    schema = {}
    for key, value in input_schema.items():
        schema[key] = map_datatype(value)

    return schema

pydanticmodel = create_model(str(data))
