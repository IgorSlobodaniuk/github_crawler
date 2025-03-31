import asyncio
import json
from typing import List, Optional, Literal

from pydantic import BaseModel

from crawler.crawler import GitHubCrawler
from crawler.utils import get_random_proxy

PROXY_PATH = 'proxylist.txt'


class SearchFilterModel(BaseModel):
    keywords: List[str]
    proxy: Optional[str] = None
    search_type: Literal['repositories', 'issues', 'wikis']


async def main():
    keywords = input("Enter keywords (comma-separated): ").strip().split(",")
    search_type = input("Enter search type (e.g., Repositories, Code, Issues): ").lower().strip()
    input_data = {
        'keywords': [kw.strip() for kw in keywords],
        'search_type': search_type,
        'proxy': get_random_proxy(PROXY_PATH)
    }

    validated_data = SearchFilterModel(**input_data)
    crawler = GitHubCrawler(
        keywords=validated_data.keywords,
        proxy=validated_data.proxy,
        search_type=validated_data.search_type
    )
    results = await crawler.run()
    print(json.dumps(results, indent=2))
    return results


if __name__ == '__main__':
    asyncio.run(main())
