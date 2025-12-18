# Project Folder Structure

This structure is designed for modularity and clarity, separating UI code from backend logic.

```
web_scraping_project/
├── .streamlit/
│   └── config.toml                     # Streamlit UI configuration (theme, server settings)
│
├── app/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── sidebar.py                  # Sidebar components (Model selection)
│   │   └── main.py                     # Main page for URL and Data Extraction
│   │
│   └── backend/
│       ├── __init__.py
│       ├── scraper_service.py          # Logic using Crawl4AI
│       ├── llm_service.py              # Logic interacting with Ollama
│       ├── data_service.py             # Logic for main pipeline
│       ├── models.py                   # Dynamic model provider selecting
│       └── prompts.py                  # Prompts for pydantic model and data extraction
│     
│     
│
├── data/
│   └── output/                         # Directory where CSV files are saved
│
│
├── testing/
│   ├── crawler_response                # Testing for crawler response
│   └── llm_response                    # Testing for LLM response
│
│
├── pyproject.toml                      # UV Dependency Manager
├── uv.lock                             # UV Dependency Manager   
├── image.png                           # Expected UI
├── .gitignore                          # Git ignore rules
├── README.md                           # Readme file for users
├── ROADMAP.md                          # Development plan
└── FOLDER_STRUCTURE.md                 # Folder structure of project
```
