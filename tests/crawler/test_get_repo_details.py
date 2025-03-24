import pytest
from unittest.mock import patch, AsyncMock
from src.crawler import GitHubCrawler

pytest_plugins = ['tests.crawler.fixtures']


@pytest.mark.asyncio
@patch.object(GitHubCrawler, '_fetch', new_callable=AsyncMock)
@patch.object(GitHubCrawler, '_parse_language_stats', return_value={'Python': 80.0, 'JavaScript': 20.0})
async def test_get_repo_details_success(mock_parse_language_stats, mock_fetch, crawler):
    repo_data = {'url': 'https://github.com/user/repo1'}

    html = """
    <h1>Repository 1</h1>
    <div class="repository-language-stats">
        <h2>Languages</h2>
        <ul>
            <a class="d-inline-flex" href="/languages/python">
                <span>Python</span>
                <span>80%</span>
            </a>
            <a class="d-inline-flex" href="/languages/javascript">
                <span>JavaScript</span>
                <span>20%</span>
            </a>
        </ul>
    </div>
    """

    mock_fetch.return_value = html
    repo_details = await crawler._get_repo_details(repo_data)
    assert repo_details['extra'] == {
        'owner': 'user',
        'language_stats': {'Python': 80.0, 'JavaScript': 20.0}
    }
    mock_fetch.assert_called_once_with('https://github.com/user/repo1')
    mock_parse_language_stats.assert_called_once_with(html)


@pytest.mark.asyncio
@patch.object(GitHubCrawler, '_fetch', new_callable=AsyncMock)
@patch.object(GitHubCrawler, '_parse_language_stats', return_value={})
async def test_get_repo_details_fetch_failure(mock_parse_language_stats, mock_fetch, crawler):
    repo_data = {'url': 'https://github.com/user/repo1'}
    mock_fetch.return_value = None
    repo_details = await crawler._get_repo_details(repo_data)
    assert 'extra' not in repo_details
    mock_fetch.assert_called_once_with('https://github.com/user/repo1')
    mock_parse_language_stats.assert_not_called()


@pytest.mark.asyncio
@patch.object(GitHubCrawler, '_fetch', new_callable=AsyncMock)
@patch.object(GitHubCrawler, '_parse_language_stats', return_value={'Python': 90.0})
async def test_get_repo_details_partial_language_stats(mock_parse_language_stats, mock_fetch, crawler):
    repo_data = {'url': 'https://github.com/user/repo1'}

    html = """
    <h1>Repository 1</h1>
    <div class="repository-language-stats">
        <h2>Languages</h2>
        <ul>
            <a class="d-inline-flex" href="/languages/python">
                <span>Python</span>
                <span>90%</span>
            </a>
        </ul>
    </div>
    """

    mock_fetch.return_value = html
    repo_details = await crawler._get_repo_details(repo_data)
    assert repo_details['extra'] == {
        'owner': 'user',
        'language_stats': {'Python': 90.0}
    }
    mock_fetch.assert_called_once_with('https://github.com/user/repo1')
    mock_parse_language_stats.assert_called_once_with(html)
