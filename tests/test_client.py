from typing import Any

import pytest

from client import get_num_stops_on_route, get_route_ids_to_long_names
from enums import RouteType


def test_get_route_ids_to_long_names_without_route_types_returns_empty_list() -> None:
    actual = get_route_ids_to_long_names(route_types=[])
    expected: dict = {}

    assert actual == expected


def test_get_route_ids_to_long_names_with_valid_route_type_returns_valid_result(
    mock_requests_with_route_data,
) -> None:
    actual = get_route_ids_to_long_names(route_types=[RouteType.LIGHT_RAIL])
    expected = {"Green-B": "Green Line B"}

    assert actual == expected


def test_get_route_ids_to_long_names_raises_exception_when_request_fails(
    mock_requests_triggered_exception,
) -> None:
    with pytest.raises(Exception):
        get_route_ids_to_long_names(route_types=[RouteType.LIGHT_RAIL])


def test_get_num_stops_on_route_with_empty_string_route_returns_zero() -> None:
    actual = get_num_stops_on_route(route_id="")
    expected = 0

    assert actual == expected


def test_get_num_stops_on_route_with_valid_route_id_returns_valid_result(
    mock_requests_with_stop_data,
) -> None:
    actual = get_num_stops_on_route("Green-B")
    expected = 3  # Mocked data quantity

    assert actual == expected


def test_get_num_stops_on_route_raises_exception_when_request_fails(
    mock_requests_triggered_exception,
) -> None:
    with pytest.raises(Exception):
        get_num_stops_on_route("Green-B")
