from unittest.mock import patch

import pytest

from src.utils import get_random_proxy


@pytest.mark.parametrize("proxies, expected_result", [
    (['proxy1.com', 'proxy2.com', 'proxy3.com'], 'http://proxy1.com'),
    (['proxy1.com'], 'http://proxy1.com'),
    ([], None),
])
def test_get_random_proxy(proxies, expected_result):
    with patch('random.choice', return_value='proxy1.com'):
        result = get_random_proxy(proxies)
        assert result == expected_result
