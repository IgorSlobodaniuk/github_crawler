pytest_plugins = ['tests.crawler.fixtures']


def test_parse_language_stats_valid_html(crawler):
    html = """
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
    """

    language_stats = crawler._parse_language_stats(html)
    assert language_stats == {
        'Python': 80.0,
        'JavaScript': 20.0
    }


def test_parse_language_stats_empty_html(crawler):
    html = """
    <div>
        <p>No language stats available</p>
    </div>
    """

    language_stats = crawler._parse_language_stats(html)
    assert language_stats == {}


def test_parse_language_stats_no_languages(crawler):
    html = """
    <h2>Languages</h2>
    <ul>
        <!-- No language entries here -->
    </ul>
    """

    language_stats = crawler._parse_language_stats(html)
    assert language_stats == {}
