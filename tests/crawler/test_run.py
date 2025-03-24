import pytest
from unittest.mock import patch, AsyncMock, Mock
from src.crawler import GitHubCrawler

pytest_plugins = ['tests.crawler.fixtures']

@pytest.mark.asyncio
@patch.object(GitHubCrawler, '_get_search_url', return_value='https://github.com/search?q=python+ai&type=repositories')
@patch.object(GitHubCrawler, '_fetch', new_callable=AsyncMock)
@patch.object(GitHubCrawler, '_get_repo_details', new_callable=AsyncMock)
@patch.object(GitHubCrawler, '_parse_search_results', return_value=(Mock, Mock))
@patch.object(GitHubCrawler, '_get_next_page_url', return_value=None)
async def test_run_success(mock_get_next_page_url, mock_parse_search_results, mock_get_repo_details, mock_fetch, mock_get_search_url, crawler):
    mock_fetch.return_value = """
    <html>
        <body>
            <div data-testid="results-list">
                <a href="/user/repo1">Repo 1</a>
                <a href="/user/repo2">Repo 2</a>
            </div>
        </body>
    </html>
    """

    # Mock the repo details retrieval
    mock_get_repo_details.side_effect = [
        {'url': 'https://github.com/user/repo1', 'extra': {'owner': 'user', 'language_stats': {'Python': 80.0}}},
        {'url': 'https://github.com/user/repo2', 'extra': {'owner': 'user', 'language_stats': {'Python': 60.0}}}
    ]

    # Run the crawler
    result = await crawler.run()

    # Debugging: Print the result to see if it's empty
    print("Result:", result)

    # Verify the length of the result list
    assert len(result) == 2
    assert result[0]['url'] == 'https://github.com/user/repo1'
    assert result[1]['url'] == 'https://github.com/user/repo2'
    assert 'extra' in result[0]
    assert 'extra' in result[1]
    assert mock_get_repo_details.call_count == 2

    # Check if the methods are called with correct arguments
    mock_get_search_url.assert_called_once()
    mock_fetch.assert_called_once_with('https://github.com/search?q=python+ai&type=repositories')
    mock_parse_search_results.assert_called_once()
    mock_get_next_page_url.assert_called_once()
