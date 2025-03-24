from src.utils import get_random_headers


def test_get_random_headers():
    # We will test if the headers contain 'User-Agent' and a valid value from the `ua.random` generated list.
    headers = get_random_headers()

    assert 'User-Agent' in headers
    assert 'Accept-Language' in headers
    assert 'Referer' in headers
    assert 'Accept-Encoding' in headers
    assert headers['Accept-Language'] in ['en-US,en;q=0.9', 'en-GB,en;q=0.8']  # Check valid language
    assert headers['Accept-Encoding'] == 'gzip, deflate, br'
    assert headers['Referer'] == 'https://github.com/'
