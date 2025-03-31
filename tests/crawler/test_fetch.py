from unittest.mock import MagicMock, AsyncMock

import aiohttp
import pytest


pytest_plugins = ['tests.crawler.fixtures']


@pytest.mark.asyncio
async def test_fetch_success(crawler):
    url = 'https://github.com/search?q=python+ai&type=repositories'

    mock = aiohttp.ClientSession
    mock.get = MagicMock()
    mock.get.return_value.__aenter__.return_value.text.return_value = '{"result": "success"}'

    async with aiohttp.ClientSession() as session:
        crawler.session = session
        result = await crawler._fetch(url, {})

    assert result == '{"result": "success"}'


@pytest.mark.asyncio
async def test_fetch_client_error(crawler):
    url = 'https://github.com/search?q=python+ai&type=repositories'
    mock = aiohttp.ClientSession
    mock.get = MagicMock()
    mock.get.return_value.__aenter__.return_value.text.return_value = None

    async with aiohttp.ClientSession() as session:
        crawler.session = session
        result = await crawler._fetch(url, {})
        assert result is None


@pytest.mark.asyncio
async def test_fetch_retries_on_failure(crawler):
    url = 'https://github.com/search?q=python+ai&type=repositories'

    mock = aiohttp.ClientSession
    mock.get = MagicMock()
    mock.get.return_value.__aenter__.return_value.text.return_value = '{"result": "success"}'

    async with aiohttp.ClientSession() as session:
        crawler.session = session
        result = await crawler._fetch(url, {})
    assert result == '{"result": "success"}'


@pytest.mark.asyncio
async def test_fetch_exceed_retries(crawler):
    url = 'https://github.com/search?q=python+ai&type=repositories'
    mock = aiohttp.ClientSession
    mock.get = MagicMock()
    mock.get.return_value.__aenter__.return_value.text.return_value = None

    async with aiohttp.ClientSession() as session:
        crawler.session = session
        result = await crawler._fetch(url, {})
    assert result is None


@pytest.mark.asyncio
async def test_fetch_with_proxy_and_headers(crawler):
    url = 'https://github.com/search?q=python+ai&type=repositories'

    mock = aiohttp.ClientSession
    mock.get = MagicMock()
    mock.get.return_value.__aenter__.return_value.text.return_value = '{"result": "success"}'

    async with aiohttp.ClientSession() as session:
        crawler.session = session
        crawler.proxies = ['http://proxy1.com']
        result = await crawler._fetch(url, {})
    assert result == '{"result": "success"}'


@pytest.mark.asyncio
async def test_fetch_client_error_handling(crawler):
    url = 'https://github.com/search?q=python+ai&type=repositories'

    mock = aiohttp.ClientSession
    mock.get = MagicMock()
    mock.get = MagicMock(side_effect=aiohttp.ClientError("Mocked client error"))

    async with aiohttp.ClientSession() as session:
        crawler.session = session
        crawler.proxies = ['http://proxy1.com']
        result = await crawler._fetch(url, {})
    assert result is None
