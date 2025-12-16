from crawl4ai import *
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling import DFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter
from crawl4ai import AdaptiveCrawler
import asyncio

LINK="https://openai.com/"

browser_config = BrowserConfig(
    browser_type='chromium',
    headless=False,
    text_mode=True,
    light_mode=True
)

# async def main():
#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         resutl = await crawler.arun(LINK)
#         print(resutl.markdown)

# url_filter = URLPatternFilter(patterns=['news', 'index'])


# async def main():
#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         crawler_config = CrawlerRunConfig(
#             deep_crawl_strategy=BFSDeepCrawlStrategy(
#                 max_depth=1,
#                 include_external=False,
#                 filter_chain=FilterChain([url_filter])
#             ),
#             scraping_strategy=LXMLWebScrapingStrategy(),
#             verbose=True,
            
#         )
#         result = await crawler.arun(LINK, config=crawler_config)

#         print(f"Number of results : {len(result)}")

#         for i in result:
#             print("="*40)
#             print(i.markdown)


async def main():
    async with AsyncWebCrawler() as crawler:
        adaptive_crawler = AdaptiveCrawler(crawler)

        result = await adaptive_crawler.digest(
            start_url=LINK,
            query="ChatGPT Atlas"
        )

        adaptive_crawler.print_stats()

        relevant_pages = adaptive_crawler.get_relevant_content(top_k=5)

        for i in relevant_pages:
            print(f"URL : {i['url']}\nScore : {i['score']}")

if __name__=="__main__":
    asyncio.run(main())