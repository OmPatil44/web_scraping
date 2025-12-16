# Project Folder Structure

This structure is designed for modularity and clarity, separating UI code from backend logic.

```
web_scraping_project/
├── .streamlit/
│   └── config.toml          # Streamlit UI configuration (theme, server settings)
│
├── app/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── sidebar.py       # Sidebar components (Model selection)
│   │   └── widgets.py       # Reusable UI widgets (Inputs, Buttons)
│   │
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── scraper_service.py   # Logic using Crawl4AI
│   │   ├── llm_service.py       # Logic interacting with Ollama
│   │   └── data_service.py      # Logic for CSV formatting/saving
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py       # shared helper functions
│
├── data/
│   └── output/              # Directory where CSV files are saved
│
├── assets/                  # Images or static assets for the UI
│
├── main.py                  # Entry point: runs the Streamlit app
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (if needed)
├── .gitignore               # Git ignore rules
├── ROADMAP.md               # Development plan
└── FOLDER_STRUCTURE.md      # This file
```

## Key Files Description

- **`main.py`**: The orchestrator. It sets up the Streamlit page config and calls functions from `app/ui`.
- **`app/backend/scraper_service.py`**: Contains the `Crawl4AI` implementation to fetch page content.
- **`app/backend/llm_service.py`**: Handles the prompt engineering and connection to the local LLM (Ollama).
- **`app/backend/data_service.py`**: Responsible for parsing LLM JSON output and writing it to CSV files.
- **`app/ui/sidebar.py`**: Encapsulates the sidebar logic to keep `main.py` clean.
