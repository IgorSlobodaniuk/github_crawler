import pytest
from unittest.mock import patch, AsyncMock
import main


@pytest.mark.asyncio
@patch('main.get_random_proxy', return_value='http://mocked-proxy.com')
@patch('main.GitHubCrawler.run', new_callable=AsyncMock, return_value=[{'repo': 'test-repo'}])
async def test_main(mock_run, mock_get_random_proxy, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'test,repo' if _.startswith('Enter keywords') else 'repositories')
    result = await main.main()

    assert isinstance(result, list)
    assert result == [{'repo': 'test-repo'}]

    mock_get_random_proxy.assert_called_once_with('proxylist.txt')
    mock_run.assert_called_once()
