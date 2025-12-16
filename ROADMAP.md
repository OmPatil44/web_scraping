# Project Roadmap: Universal Web Scraper with LLM Extraction

This document outlines the phased approach to building the local web scraping and extraction tool using Crawl4AI, Ollama, and Streamlit.

## Phase 1: Foundation & Setup
**Goal**: Establish the environment and verify core technologies work in isolation.
- [ ] **Environment Setup**: Initialize Python virtual environment.
- [ ] **Dependency Installation**: Install `crawl4ai`, `streamlit`, `langchain` (or `ollama` lib), `pandas`.
- [ ] **Tech Validation - Crawling**: Write a minimal script to crawl a test URL using Crawl4AI and print raw markdown.
- [ ] **Tech Validation - LLM**: Write a minimal script to send raw text to a local Ollama instance and get a structured JSON response.

## Phase 2: Backend Architecture
**Goal**: Build the core logic modules that run the scraping and extraction pipeline.
- [ ] **Scraper Module (`scraper.py`)**:
    - Function to accept a URL.
    - specialized configuration for Crawl4AI (managing sessions, bypassing simple blocks if needed).
    - Return clean markdown/text content.
- [ ] **LLM Extractor Module (`llm_extractor.py`)**:
    - Function to accept `content` and `fields_list`.
    - Construct a dynamic prompt instructing the LLM to extract specific fields.
    - Enforce JSON output format for reliable parsing.
- [ ] **Data Handler (`file_handler.py`)**:
    - Function to convert list of extracted dictionaries to CSV.
    - Ensure correct headers and formatting.

## Phase 3: UI Development (Streamlit)
**Goal**: Create the Single Page Application (SPA) interface.
- [ ] **Sidebar Development**:
    - Dropdown to select available local models (fetch from Ollama API or hardcode for MVP).
- [ ] **Main Area Layout**:
    - Project Title & Info.
    - Input: Text field for Target URL.
    - Input: Text field/Tags input for "Fields to Extract" (e.g., "Price, Title, Rating").
- [ ] **State Management**:
    - Handle loading states ("Crawling...", "Extracting...").
    - Store results in Session State to prevent loss on re-renders.

## Phase 4: Integration & Polish
**Goal**: Connect UI to Backend and ensure smooth user experience.
- [ ] **Pipeline Integration**:
    - Wire the "Start" button to trigger the backend pipeline.
    - Display live progress logs or status indicators.
- [ ] **Results Display**:
    - Show a preview of the extracted data (dataframe) on the screen.
- [ ] **Export Feature**:
    - Enable the "Download CSV" button only after successful extraction.
- [ ] **Error Handling**:
    - Graceful messages for invalid URLs, LLM timeouts, or empty scrape results.

## Phase 5: Testing & Handoff
- [ ] End-to-end testing with various website types (blogs, e-commerce).
- [ ] Code cleanup and final documentation.
