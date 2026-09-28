from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    items = urlsplit(url)
    netloc = items[1]
    path = items[2]
    query = ('?' if len(items[3]) > 0 else '') + items[3]
    fragment = ('#' if len(items[4]) > 0 else '') + items[4]
    return (netloc + path + query + fragment).rstrip('/')
