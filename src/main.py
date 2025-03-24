import asyncio
import json

from src.crawler import GitHubCrawler


async def main():
    keywords = input("Enter keywords (comma-separated): ").strip().split(",")
    search_type = input("Enter search type (e.g., Repositories, Code, Issues): ").strip()
    input_data = {
        'keywords': [kw.strip() for kw in keywords],
        'type': search_type
    }

    crawler = GitHubCrawler(
        keywords=input_data['keywords'],
        proxy_file='../proxylist.txt',
        search_type=input_data['type']
    )

    results = await crawler.run()
    print(json.dumps(results, indent=2))
    return results


if __name__ == '__main__':
    asyncio.run(main())
