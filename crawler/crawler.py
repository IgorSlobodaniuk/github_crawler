import random

import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Optional, Any, Tuple

from crawler.utils import get_random_headers

BASE_URL = 'https://github.com'
NUMBER_OF_RETRIES = 3
RANGE_FROM = 1
RANGE_TO = 3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitHubCrawler:
    """
    A class to crawl GitHub search results and extract repository details such as language statistics.

    Attributes:
        keywords (List[str]): The keywords to search for on GitHub.
        proxy (List[str]): A random proxy URL to be used for all requests in one session.
        search_type (str): The type of GitHub search (e.g., 'repositories', 'users').
        session (Optional[aiohttp.ClientSession]): The aiohttp session for making requests.

    Methods:
        run() -> List[Dict]: Starts the crawling process and returns a list of repositories with details.
    """
    def __init__(self, keywords: List[str], proxy: str, search_type: str) -> None:
        """
        Initializes the GitHubCrawler instance.

        Args:
            keywords (List[str]): The list of keywords to search for.
            proxy (str]: A random proxy URL to be used for all requests in one session.
            search_type (str): The search type (e.g., 'repositories').
        """
        self.keywords = keywords
        self.proxy = proxy
        self.search_type = search_type
        self.session: Optional[aiohttp.ClientSession] = None

    def _get_search_url(self) -> Tuple[str, Dict[str, str]]:
        """
        Constructs the search URL for GitHub with the specified keywords and search type.

        Returns:
            tuple: The search URL and query parameters.
        """
        query_params = {'q': ' '.join(self.keywords), 'type': self.search_type}
        return urljoin(BASE_URL, '/search'), query_params

    async def _fetch(self, url: str, query_params: Dict[str, str]) -> Optional[str]:
        """
        Fetches the HTML content of a given URL using aiohttp with retries.

        Args:
            url (str): The URL to fetch.

        Returns:
            Optional[str]: The HTML content if successful, or None if failed after retries.
        """
        for attempt in range(NUMBER_OF_RETRIES):
            headers = get_random_headers()
            try:
                logger.info('Attempting to fetch %s with proxy %s (Attempt %d)', url, self.proxy, attempt + 1)
                async with self.session.get(url, params=query_params, headers=headers, timeout=5, proxy=self.proxy) as response:
                    response.raise_for_status()
                    logger.info('Successfully fetched %s', url)
                    return await response.text()

            except aiohttp.ClientError as e:
                logger.error('Attempt %d failed for %s: %s', attempt + 1, url, str(e))
                if attempt == NUMBER_OF_RETRIES - 1:
                    return

                await asyncio.sleep(random.randint(RANGE_FROM, RANGE_TO))

    def _parse_search_results(self, html: str) -> List[Dict[str, str]]:
        """
        Parses the search results page HTML and extracts repository URLs.

        Args:
            html (str): The HTML content of the search results page.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing repository URLs.
        """
        logger.info('Parsing search results...')
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for link in soup.select("div[data-testid='results-list'] [class~='search-title'] a"):
            results.append({'url': urljoin(BASE_URL, link['href'])})
        logger.info('Found %d repositories', len(results))
        return results

    def _parse_language_stats(self, html: str) -> Dict[str, float]:
        logger.info('Parsing language stats...')
        """
        Parses the language statistics from the repository details page.

        Args:
            html (str): The HTML content of the repository details page.

        Returns:
            Dict[str, float]: A dictionary mapping language names to their usage percentages.
        """
        logger.info("Parsing language stats...")
        language_stats = {}
        soup = BeautifulSoup(html, 'html.parser')
        h2 = soup.find('h2', string='Languages')
        if not h2:
            logger.info('No language stats found')
            return {}

        languages_container = h2.find_next('ul').select('a.d-inline-flex')
        for language_container in languages_container:
            lang_name = language_container.select_one('span').get_text(strip=True)
            lang_percent = language_container.select_one('span + span').get_text(strip=True).strip('%')
            language_stats[lang_name] = float(lang_percent)
        logger.info('Parsed language stats: %s', language_stats)
        return language_stats

    async def _get_repo_details(self, repo: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetches additional details for a repository, such as the owner and language statistics.

        Args:
            repo (Dict[str, str]): A dictionary containing the repository URL.

        Returns:
            Dict[str, str]: A dictionary containing repository details with extra information.
        """
        logger.info('Fetching details for repo: %s', repo['url'])
        html = await self._fetch(repo['url'], query_params={})
        if html:
            repo['extra'] = {
                'owner': urlparse(repo['url']).path.split('/')[1],
                'language_stats': self._parse_language_stats(html)
            }
            logger.info('Fetched details for repo: %s', repo['url'])
        return repo

    def _get_next_page_url(self, html: str) -> Optional[str]:
        """
        Extracts the URL for the next page of search results from the current page's HTML.

        Args:
            html (str): The HTML content of the current page.

        Returns:
            Optional[str]: The URL of the next page, or None if no next page exists.
        """
        soup = BeautifulSoup(html, 'html.parser')
        next_link = soup.find('a', rel='next')
        return next_link.get('href') if next_link else None

    async def run(self) -> List[Dict[str, str]]:
        """
        Starts the crawling process by fetching pages of search results and extracting repository details.

        Returns:
            List[Dict[str, str]]: A list of repositories with their details (URLs, owners, language stats, etc.).
        """
        logger.info('Starting GitHub crawling process')
        search_url, query_params = self._get_search_url()
        all_repos: List[Dict[str, str]] = []
        async with aiohttp.ClientSession() as session:
            self.session = session
            while search_url:
                logger.info('Fetching page: %s', search_url)
                html = await self._fetch(search_url, query_params)
                if not html:
                    logger.error('Failed to fetch page: %s', search_url)
                    break

                repos = self._parse_search_results(html)
                repo_details = await asyncio.gather(*[self._get_repo_details(repo) for repo in repos])
                all_repos.extend(repo_details)
                search_url = self._get_next_page_url(html)
                query_params = {}
        logger.info('Finished crawling. Found %d repositories.', len(all_repos))
        return all_repos
