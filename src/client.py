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
_STOPS_ENDPOINT = "/stops"


def get_route_ids_to_long_names(route_types: list[RouteType]) -> dict[str, str]:
    """
    Get a dictionary of route IDs to their respective long names for all
    provided route types using the MBTA API.

    The dictionary is sorted in alphabetical order by value (route long name).
    """

    # Short circuit in case of falsy inputs (e.g. None or empty list)
    if not route_types:
        return {}

    route_type_values = [str(route_type.value) for route_type in route_types]

    url = _API_BASE_URL + _ROUTES_ENDPOINT
    parameters = {
        "fields[route]": "long_name",  # Restrict output to only the relevant fields
        "filter[type]": ",".join(route_type_values),
        "sort": "long_name",
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

    # Process the response and deduplicate route IDs using dictionary keys
    route_names_by_id: dict[str, str] = {}
    routes: list[dict] = response_body.get("data", [])
    for route in routes:
        route_id = route.get("id", None)
        route_attributes = route.get("attributes", {})
        route_long_name = route_attributes.get("long_name", None)
        if route_id and route_long_name:
            route_names_by_id[route_id] = route_long_name

    return route_names_by_id


def get_num_stops_on_route(route_id: str) -> int:
    """
    Get the number of stops along a given route from the MBTA API.

    If the route ID is invalid, returns 0 stops.
    """

    # Short circuit in case of falsy inputs (e.g. None or empty string)
    if not route_id:
        return 0

    url = _API_BASE_URL + _STOPS_ENDPOINT
    parameters = {
        "fields[stop]": "",  # Restrict output to only the relevant fields (i.e. None)
        "filter[route]": route_id,
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

    # Process the response and use a set to deduplicate stop IDs
    stops_on_route: set[str] = set()
    stops: list[dict] = response_body.get("data", [])
    for stop in stops:
        stop_id = stop.get("id", None)
        if stop_id:
            stops_on_route.add(stop_id)

    return len(stops_on_route)
