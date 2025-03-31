from crawler.utils import get_random_headers


def test_get_random_headers():
    headers = get_random_headers()
    assert 'User-Agent' in headers
    assert 'Accept-Language' in headers
    assert 'Referer' in headers
    assert 'Accept-Encoding' in headers
    assert headers['Accept-Language'] in ['en-US,en;q=0.9', 'en-GB,en;q=0.8']
    assert headers['Accept-Encoding'] == 'gzip, deflate, br'
    assert headers['Referer'] == 'https://github.com/'
