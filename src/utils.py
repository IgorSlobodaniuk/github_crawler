import random
from fake_useragent import UserAgent

ua = UserAgent(browsers=['Edge', 'Chrome'])


def load_proxies(proxy_file):
    """Load proxies from proxylist.txt"""
    try:
        with open(proxy_file, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Proxy file not found. Proceeding without proxies.")
        return []


def get_random_proxy(proxies):
    """Retrieve a random proxy from the list."""
    return f'http://{random.choice(proxies)}' if proxies else None


def get_random_headers():
    """Generate random headers for each request."""
    return {
        'User-Agent': ua.random,
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8']),
        'Referer': 'https://github.com/',
        'Accept-Encoding': 'gzip, deflate, br',
    }
