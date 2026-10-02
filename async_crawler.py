from crawl import PageData, extract_page_data, normalize_url
from asyncio import Lock, Semaphore, create_task, gather
from aiohttp import ClientSession
from urllib.parse import urlsplit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


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
        # So using Selenium does work correctly in that it only scrapes data
        # after the page has been fully loaded and javascript run.
        # The issue is that it's really slow.
        # I think it would be better to create multiple drivers that are each
        # scraping pages in parallel, assuming Selenium will allow that.
        # This would likely require creating multiple instances of AsyncCrawler;
        # a number of instances equal to max_concurrency.
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.find_element(By.TAG_NAME, "html").get_attribute("outerHTML")
        driver.quit()
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
                    task = create_task(self.crawl_page(link))
                    tasks.append(task)
                    self.all_tasks.add(task)
            except Exception as e:
                print(e)
        
        try:
            await gather(*tasks)
        finally:
           return self.page_data
    
    
    async def crawl(self) -> dict[str, PageData]:
        return await self.crawl_page(self.base_url)


async def crawl_site_async(url: str, max_concurrency: int = 10, max_pages: int = 100) -> dict[str, PageData]:
    async with AsyncCrawler(url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
