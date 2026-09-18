"""
A light-weight client to interact with the MBTA's API

Reference - https://api-v3.mbta.com/docs/swagger/index.html
"""

import requests

from enums import RouteType

_API_BASE_URL = "https://api-v3.mbta.com"
_TIMEOUT_IN_SECONDS = 5

# Endpoints
_ROUTES_ENDPOINT = "/routes"


def get_route_long_names(route_types: list[RouteType]) -> list[str]:
    """
    Get an ordered and deduplicated list of all route long names of the
    provided route types from the MBTA API.
    """
    # Short circuit in case of falsy inputs (e.g. None or empty list)
    if not route_types:
        return []

    route_type_values = [str(route_type.value) for route_type in route_types]

    url = _API_BASE_URL + _ROUTES_ENDPOINT
    parameters = {
        "fields[route]": "long_name",  # Restrict output to only the relevant fields
        "filter[type]": ",".join(route_type_values),
    }

    # Make the request to the MBTA API
    try:
        response = requests.get(url, params=parameters, timeout=_TIMEOUT_IN_SECONDS)
        response.raise_for_status()
        response_body = response.json()
    except Exception as ex:
        raise RuntimeError(
            f"Failed to retrieve data from MBTA API request to URL: {url}"
        ) from ex

    # Process the response and use a set to deduplicate route names
    route_long_names: set[str] = set()
    routes: list[dict] = response_body.get("data", [])
    for route in routes:
        route_attributes = route.get("attributes", {})
        route_long_name = route_attributes.get("long_name", None)
        if route_long_name:
            route_long_names.add(route_long_name)

    # Sort the route names into alphabetical order
    ordered_route_names = sorted(route_long_names)
    return ordered_route_names
