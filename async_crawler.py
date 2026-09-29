from crawl import PageData, extract_page_data, normalize_url
from asyncio import Lock, Semaphore, create_task, gather
from aiohttp import ClientSession
from urllib.parse import urlsplit


class AsyncCrawler:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url)[1]
        self.page_data = {}
        self.visited = set()
        self.lock = Lock()
        self.max_concurrency = 12
        self.semaphore = Semaphore(self.max_concurrency)
        self.session: ClientSession
    
    
    async def __aenter__(self):
        self.session = ClientSession()
        return self
    
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    
    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True
    
    
    async def get_html(self, url: str) -> str:
        async with self.session.get(
            url, headers={"User-Agent": "webscraper/1.0"}
        ) as response:
            content_type = response.headers["content-type"]
            if response.status >= 400:
                response.raise_for_status()
            if not "text/html" in content_type:
                raise Exception(f'invalid content-type "{content_type}"')
            return await response.text()
    
    
    async def crawl_page(self, current_url: str) -> dict[str, PageData]:
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
            except Exception as e:
                print(e)
        
        await gather(*tasks)
        return self.page_data
    
    
    async def crawl(self) -> dict[str, PageData]:
        return await self.crawl_page(self.base_url)


async def crawl_site_async(url: str) -> dict[str, PageData]:
    async with AsyncCrawler(url) as crawler:
        return await crawler.crawl()
