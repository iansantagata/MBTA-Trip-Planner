from typing import Any

import pytest

from client import get_route_long_names
from enums import RouteType


def test_get_route_long_names_without_route_types_returns_empty_list() -> None:
    result = get_route_long_names(route_types=[])
    assert result == []


def test_get_route_long_names_with_valid_route_type_returns_valid_result(
    mock_requests_with_route_data,
) -> None:
    actual = get_route_long_names(route_types=[RouteType.LIGHT_RAIL])
    expected = ["Green Line B"]

    assert actual == expected


def test_get_route_long_names_raises_exception_when_request_fails(
    mock_requests_triggered_exception,
) -> None:
    with pytest.raises(Exception):
        get_route_long_names(route_types=[RouteType.LIGHT_RAIL])
