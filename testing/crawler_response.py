from crawl4ai import *
import asyncio

LINK="https://openai.com/news/?display=list"

browser_config = BrowserConfig(
    browser_type='chromium',
    headless=False,
    text_mode=True,
    light_mode=True
)

crawler_config = CrawlerRunConfig()

async def main():
    async with AsyncWebCrawler(config=browser_config) as crawler:
        resutl = await crawler.arun(LINK)
        print(resutl.markdown)


if __name__=="__main__":
    asyncio.run(main())