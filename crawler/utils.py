import random
import logging
from fake_useragent import UserAgent

ua = UserAgent(browsers=['Edge', 'Chrome'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_random_proxy(proxy_file):
    """Load proxies from proxylist.txt and return a random one"""
    try:
        with open(proxy_file, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
            return random.choice(proxies) if proxies else None
    except FileNotFoundError:
        logger.warning('Proxy file not found. Proceeding without proxies.')
        return []


def get_random_headers():
    """Generate random headers for each request."""
    return {
        'User-Agent': ua.random,
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8']),
        'Referer': 'https://github.com/',
        'Accept-Encoding': 'gzip, deflate, br',
    }
