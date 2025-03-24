from urllib.parse import urlparse, parse_qs

pytest_plugins = ['tests.crawler.fixtures']


def test_get_search_url_success(crawler):
    search_url = crawler._get_search_url()
    parsed_url = urlparse(search_url)

    assert parsed_url.scheme == 'https'
    assert parsed_url.netloc == 'github.com'
    assert parsed_url.path == '/search'

    query_params = parse_qs(parsed_url.query)
    assert query_params['q'] == ['python ai']
    assert query_params['type'] == ['repositories']
