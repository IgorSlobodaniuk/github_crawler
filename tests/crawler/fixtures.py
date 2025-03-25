import pytest
from src.crawler import GitHubCrawler


@pytest.fixture
def crawler():
    keywords = ['python', 'ai']
    proxies = ['http://127.0.0.1:1080', 'http://127.0.0.1:1000']
    search_type = 'repositories'
    return GitHubCrawler(keywords, proxies, search_type)
