import pytest
from src.utils import load_proxies


@pytest.mark.parametrize("file_content, expected_result", [
    ("proxy1.com\nproxy2.com\nproxy3.com\n", ['proxy1.com', 'proxy2.com', 'proxy3.com']),
    ("", []),
    (None, []),
])
def test_load_proxies(file_content, expected_result, tmpdir):
    proxy_file = tmpdir.join("proxylist.txt")

    if file_content is not None:
        proxy_file.write(file_content)

    result = load_proxies(str(proxy_file))
    assert result == expected_result
