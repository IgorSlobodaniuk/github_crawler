pytest_plugins = ['tests.crawler.fixtures']


def test_parse_search_results_valid_html(crawler):
    html = """
    <div data-testid="results-list">
        <div class="search-title">
            <a href="/repo1">Repo 1</a>
        </div>
        <div class="search-title">
            <a href="/repo2">Repo 2</a>
        </div>
    </div>
    """

    results = crawler._parse_search_results(html)
    assert len(results) == 2

    assert results[0]['url'] == 'https://github.com/repo1'
    assert results[1]['url'] == 'https://github.com/repo2'


def test_parse_search_results_empty_html(crawler):
    html = """
    <div data-testid="results-list"></div>
    """

    results = crawler._parse_search_results(html)

    assert len(results) == 0


def test_parse_search_results_no_results_list(crawler):
    html = """
    <div>
        <p>No results found</p>
    </div>
    """

    results = crawler._parse_search_results(html)
    assert len(results) == 0


def test_parse_search_results_malformed_html(crawler):
    html = """
    <div data-testid="results-list">
        <div class="search-title">
            <a href="/repo1">Repo 1</a>
        </div>
        <div class="search-title">
            <span>Missing Link</span>
        </div>
    </div>
    """

    results = crawler._parse_search_results(html)

    assert len(results) == 1
    assert results[0]['url'] == 'https://github.com/repo1'
