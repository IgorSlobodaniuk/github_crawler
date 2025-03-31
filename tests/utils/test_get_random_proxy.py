import pytest
from crawler.utils import get_random_proxy


@pytest.mark.parametrize("file_content, expected_results", [
    ("proxy1.com\nproxy2.com\nproxy3.com\n", ['proxy1.com', 'proxy2.com', 'proxy3.com']),
    ("", []),
])
def test_load_proxies(file_content, expected_results, tmpdir):
    proxy_file = tmpdir.join("proxylist.txt")

    if file_content is not None:
        proxy_file.write(file_content)

    result = get_random_proxy(str(proxy_file))
    expected_results = expected_results or [None]
    assert result in expected_results
