from crawl4ai import *
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling import DFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter
from crawl4ai import AdaptiveCrawler
from crawl4ai import LLMTableExtraction, LLMConfig
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
llm_config = LLMConfig(
    provider="gemini-2.5-flash", 
    api_token=GEMINI_API_KEY,
    temperature=0.1
)

URL = "https://ollama.com/library/nemotron-3-nano"

tableExtraction = LLMTableExtraction(
    llm_config=llm_config,
    max_tries=3,                      # Retry up to 3 times if extraction fails
    css_selector="table",             # Optional: focus on specific tables
    enable_chunking=True,             # Automatically chunk large tables (default: True)
    chunk_token_threshold=3000,       # Split tables larger than this (default: 3000 tokens)
    min_rows_per_chunk=10,            # Minimum rows per chunk (default: 10)
    max_parallel_chunks=5,            # Process up to 5 chunks in parallel (default: 5)
    verbose=True
)

browserConfig = BrowserConfig(
    browser_type='chromium',
    headless=True,
    text_mode=True,
    light_mode=True
)

crawlerConfig = CrawlerRunConfig(
    # deep_crawl_strategy=BFSDeepCrawlStrategy(
    #     max_depth=1,
    #     max_pages=10,
    # ),
    scraping_strategy=LXMLWebScrapingStrategy(),
    only_text=True,
    exclude_internal_links=True,
    exclude_social_media_domains=True,
    magic=True,
    # table_extraction=tableExtraction
)


async def main():
    async with AsyncWebCrawler(config=browserConfig) as crawler:
        result = await crawler.arun(URL, config=crawlerConfig)
        
        if not result.success:
            print(f"[Backend] Error : {result.error_message}")
            return None
        
        if result.status_code == 404:
            print(f"[Backend] Page not found !")
            return None

        if str(result.markdown).strip() == "":
            print("[Backend] No results found !")
            return None
        # print(type(result))
    return result.markdown

if __name__ == "__main__":
    asyncio.run(main())