from unittest.mock import patch

pytest_plugins = ['tests.crawler.fixtures']


@patch('crawler.crawler.BeautifulSoup')
def test_get_next_page_url_exists(mock_beautiful_soup, crawler):
    html = """
    <html>
        <body>
            <div class="pagination">
                <a href="/search?page=2" rel="next">Next</a>
            </div>
        </body>
    </html>
    """

    mock_beautiful_soup.return_value.find.return_value = {'href': '/search?page=2'}
    next_page_url = crawler._get_next_page_url(html)
    assert next_page_url == '/search?page=2'


@patch('crawler.crawler.BeautifulSoup')
def test_get_next_page_url_no_next(mock_beautiful_soup, crawler):
    html = """
    <html>
        <body>
            <div class="pagination">
                <!-- No next page link -->
            </div>
        </body>
    </html>
    """

    mock_beautiful_soup.return_value.find.return_value = None
    next_page_url = crawler._get_next_page_url(html)
    assert next_page_url is None
