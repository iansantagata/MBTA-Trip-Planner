from client import get_route_long_names
from enums import RouteType


def test_get_route_long_names_without_route_types_returns_empty_list() -> None:
    result = get_route_long_names(route_types=[])
    assert result == []


def test_get_route_long_names_with_valid_route_type_returns_valid_result() -> None:
    result = get_route_long_names(route_types=[RouteType.LIGHT_RAIL])
    assert result
    assert result[0]  # At least one non-empty element
