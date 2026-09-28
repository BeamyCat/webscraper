from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(url: str) -> str:
    items = urlsplit(url)
    netloc = items[1]
    path = items[2]
    query = ('?' if len(items[3]) > 0 else '') + items[3]
    fragment = ('#' if len(items[4]) > 0 else '') + items[4]
    return (netloc + path + query + fragment).rstrip('/')


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    
    h1 = soup.find('h1')
    if h1:
        return h1.get_text()
    
    h2 = soup.find('h2')
    if h2:
        return h2.get_text()
        
    return ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    
    main = soup.find('main')
    if main:
        p = main.find('p')
        if p:
            return p.get_text()
    
    p = soup.find('p')
    if p:
        return p.get_text()
        
    return ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    
    urls: list[str] = []
    for a in soup.body.find_all('a'):
        url = a.get('href')
        if url:
            if url.startswith('/'):
                urls.append(urljoin(base_url, url))
            else:
                urls.append(url)
            
    return urls


def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    
    urls: list[str] = []
    for img in soup.body.find_all('img'):
        url = img.get('src')
        if url:
            if url.startswith('/'):
                urls.append(urljoin(base_url, url))
            else:
                urls.append(url)
            
    return urls


def extract_page_data(html: str, page_url: str) -> PageData:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }


def get_html(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": "webscraper/1.0"})
    content_type = response.headers["content-type"]
    if response.status_code >= 400:
        response.raise_for_status()
    if not "text/html" in content_type:
        raise Exception(f'invalid content-type "{content_type}"')
    return response.text


def crawl_page(base_url: str, current_url: str = None, page_data: dict[str, PageData] = {}) -> dict[str, PageData]:
    # Default current_url to base_url
    if not current_url:
        current_url = base_url
    
    # Return if we're in a different domain
    if urlsplit(current_url)[1] != urlsplit(base_url)[1]:
        return
    
    key = normalize_url(current_url)
    
    # Return if we've already checked this page
    if key in page_data:
        return
    
    try:
        print(f"crawling {current_url}")
        html = get_html(current_url)
        page_data[key] = extract_page_data(html, current_url)
        for link in page_data[key]["outgoing_links"]:
            crawl_page(base_url, link, page_data)
    except Exception as e:
        print(e)
    
    return page_data










