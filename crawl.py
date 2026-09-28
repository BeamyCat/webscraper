from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag


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
    
    main_p = soup.find('main').find('p')
    if main_p:
        return main_p.get_text()
    
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


