import sys
import os
import asyncio
import streamlit as st
import pandas as pd

os.system("playwright install chromium")

# for async error
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# import errors
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.backend.data_service import run_pipeline
from app.ui.sidebar import render_sidebar

st.set_page_config(page_title="AI Web Scraper", page_icon="🕷️", layout="wide")

# First page
api_key, provider, is_valid = render_sidebar()

if is_valid:
    st.title("🕷️ AI Powered WebCrawler")
    
    url_input = st.text_input("Target URL", placeholder="https://example.com/products")
    user_prompt = st.text_area("What to extract?", placeholder="E.g., Extract product names...", height=150)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        scrape_clicked = st.button("Start Scraping", use_container_width=True)
    
    with col2:
        download_placeholder = st.empty()
    
    
    async def execute_scraping():
        try:
            content = await run_pipeline(url_input, user_prompt)
            return content
        except Exception as e:
            st.error(f"Scraping Error: {e}")
            return None
    
    if scrape_clicked:
        if not url_input or not user_prompt:
            st.error("Please provide both a URL and extraction instructions.")
        else:
            with st.spinner("🕷️ Scraping and extracting data..."):
                try:
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop() # Async loop errors
                        asyncio.set_event_loop(loop)
                    
                    result = loop.run_until_complete(execute_scraping())
                   
                    if result:
                        st.success("✅ Extraction Complete!")
                        output_file = r"data\output\extracted_data.csv"
                        if os.path.exists(output_file):
                            with open(output_file, 'r') as f:
                                csv_data = f.read()
                            
                            with download_placeholder:
                                st.download_button(
                                    label="⬇️ Download CSV",
                                    data=csv_data,
                                    file_name="extracted_data.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            try:
                                content = pd.DataFrame(result)
                                st.dataframe(content) 
                            except Exception as e:
                                st.warning(f"Could not preview CSV: {e}")
                except Exception as e:
                    st.error(f"Critical Failure: {e}")

else:
    st.title("🕷️ AI Web Scraper")
    st.info("👈 Please configure the LLM Provider in the sidebar to continue.")
    st.markdown("""
    ### How to use:
    1. Select your LLM Provider (Ollama, OpenRouter, or Gemini).
    2. Enter your API Key if required.
    3. Once validated, you can enter the URL and extraction details here.
    """)
