from crawl import PageData, extract_page_data, normalize_url
import asyncio
from asyncio import Lock, Semaphore
from aiohttp import ClientSession
from urllib.parse import urlsplit
from playwright.async_api import async_playwright, Playwright


class AsyncCrawler:
    def __init__(self, 
        base_url: str, 
        max_concurrency: int = 10, 
        max_pages: int = 100
    ) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url)[1]
        self.page_data = {}
        self.visited = set()
        self.lock = Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = Semaphore(self.max_concurrency)
        self.session: ClientSession
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()
    
    
    async def __aenter__(self):
        self.session = ClientSession()
        return self
    
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    
    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if self.should_stop or normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            if len(self.visited) > self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False
            return True
    
    
    async def get_html(self, url: str) -> str:
        async with async_playwright() as playwright:
            browser = await playwright.webkit.launch()
            page = await browser.new_page()
            await page.goto(url)
            html = await page.content()
            await browser.close()
            return html
    
    
    async def crawl_page(self, current_url: str) -> dict[str, PageData]:
        # Return if we've hit max pages
        if self.should_stop:
            return
        
        # Return if we're in a different domain
        if urlsplit(current_url)[1] != self.base_domain:
            return

        key = normalize_url(current_url)

        # Return if we've already checked this page
        if not await self.add_page_visit(key):
            return

        tasks: list[Task] = []
        async with self.semaphore:
            try:
                print(f"crawling {current_url}")
                html = await self.get_html(current_url)
                async with self.lock:
                    self.page_data[key] = extract_page_data(html, current_url)
                for link in self.page_data[key]["outgoing_links"]:
                    task = asyncio.create_task(self.crawl_page(link))
                    tasks.append(task)
                    self.all_tasks.add(task)
            except Exception as e:
                print(e)
        
        try:
            await asyncio.gather(*tasks)
        finally:
           return self.page_data
    
    
    async def crawl(self) -> dict[str, PageData]:
        return await self.crawl_page(self.base_url)


async def crawl_site_async(url: str, max_concurrency: int = 10, max_pages: int = 100) -> dict[str, PageData]:
    async with AsyncCrawler(url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
