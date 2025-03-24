import asyncio

import pytest
from src.crawler import GitHubCrawler


@pytest.fixture
def crawler():
    keywords = ['python', 'ai']
    proxy_file = 'path_to_proxy_file'
    search_type = 'repositories'
    return GitHubCrawler(keywords, proxy_file, search_type)
