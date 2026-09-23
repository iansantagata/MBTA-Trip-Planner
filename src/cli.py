"""
The CLI entry point for this MBTA wrapper app
"""

import click
from tabulate import tabulate

from client import get_route_ids_to_long_names, get_stops_on_route
from enums import RouteType
from graph import Graph, Node
from utils import invert_dictionary

# Common CLI Options
_light_rail_option = click.option(
    "--light-rail",
    "-l",
    is_flag=True,
    type=bool,
    default=False,
    help="Light rail routes will be included in the search",
)

_heavy_rail_option = click.option(
    "--heavy-rail",
    "-h",
    is_flag=True,
    type=bool,
    default=False,
    help="Heavy rail routes will be included in the search",
)

_commuter_rail_option = click.option(
    "--commuter-rail",
    "-c",
    is_flag=True,
    type=bool,
    default=False,
    help="Commuter rail routes will be included in the search",
)

_bus_option = click.option(
    "--bus",
    "-b",
    is_flag=True,
    type=bool,
    default=False,
    help="Bus routes will be included in the search",
)

_ferry_option = click.option(
    "--ferry",
    "-f",
    is_flag=True,
    type=bool,
    default=False,
    help="Ferry routes will be included in the search",
)


# Helper methods
def _validate_route_types(route_types: list[RouteType]) -> None:
    """
    Validates that at least one route type is included to be queried
    """

    if not route_types:
        raise click.UsageError(
            "At least one route type option must be included in the search"
        )


def _validate_stop_name(stop_name: str, valid_stop_names: list[str]) -> None:
    """
    Validates that a given stop name is within a list of valid stop names
    """

    if stop_name not in valid_stop_names:
        separated_valid_station_names = "\n".join(valid_stop_names)
        raise click.UsageError(
            f"Station name '{stop_name}' not found.\n\n"
            f"Valid station names for the provided route types include:\n"
            f"{separated_valid_station_names}"
        )


def _validate_path(start: str, end: str, path: list[Node]) -> None:
    """
    Validates that a given path has nodes and that it starts and ends where the user specified
    """

    if not path:
        raise click.ClickException(f"Could not find path between {start} and {end}")

    path_start = path[0].name
    if path_start != start:
        raise click.ClickException(
            f"Computed path starts at {path_start} instead of intended start at {start}"
        )

    path_end = path[-1].name
    if path_end != end:
        raise click.ClickException(
            f"Computed path ends at {path_end} instead of intended end at {end}"
        )


def _get_stops_by_route(route_ids: list[str]) -> dict[str, list[str]]:
    """
    Retrieves all the stop names along each route ID.

    Useful for determining which stops are along a single route or which routes have stop overlaps.
    """

    stops_by_route: dict[str, list[str]] = {}
    for route_id in route_ids:
        stops_on_route = get_stops_on_route(route_id)
        stops_by_route[route_id] = stops_on_route

    return stops_by_route


def _get_graph_from_stops(
    stop_names: list[str], stops_by_route: dict[str, list[str]]
) -> Graph:
    """
    Given a list of stops and the stops separated by their route, this function constructs
    and returns an unweighted graph of stop nodes.

    Useful for determining a path between various stops.

    Note - This functionality assumes that stop nodes are "adjacent" if they are on the same route
    as other stop nodes. This implies that moving along an edge on a route from any one stop to
    another is an atomic action and of equal weight, which is clearly not the case in real life.
    """

    graph = Graph()
    for stop_name in stop_names:
        graph.add_node(stop_name)

    for stop_names_on_route in list(sorted(stops_by_route.values())):
        for first_stop in stop_names_on_route:
            for second_stop in stop_names_on_route:
                if first_stop != second_stop:
                    graph.add_edge(first_stop, second_stop)

    return graph


def _get_path_route_guidance(
    path: list[Node], routes_by_stop: dict[str, list[str]]
) -> dict[str, set[str]]:
    """
    Given a path and a list of routes associated with each stop, produce a list of stops
    and matching recommended routes that offer guidance along the path from start to end.
    """

    path_route_guidance: dict[str, set[str]] = {}
    previous_stop = ""
    for stop_node in path:
        if previous_stop:
            current_routes = set(routes_by_stop[stop_node.name])
            path_route_guidance[previous_stop].intersection_update(current_routes)

        path_route_guidance[stop_node.name] = set(routes_by_stop[stop_node.name])
        previous_stop = stop_node.name

    # Clear out final set of routes guiding away from the last stop
    # The last stop is the destination
    if previous_stop:
        path_route_guidance[previous_stop] = set()

    return path_route_guidance


@click.command()
@_light_rail_option
@_heavy_rail_option
@_commuter_rail_option
@_bus_option
@_ferry_option
def routes(
    light_rail: bool,
    heavy_rail: bool,
    commuter_rail: bool,
    bus: bool,
    ferry: bool,
) -> None:
    """
    Get a list of all of the names of routes of all chosen route types.

    List is ordered alphabetically by route name.

    At least one route type flag is required.
    """

    # Validate inputs
    route_types: list[RouteType] = []
    if light_rail:
        route_types.append(RouteType.LIGHT_RAIL)

    if heavy_rail:
        route_types.append(RouteType.HEAVY_RAIL)

    if commuter_rail:
        route_types.append(RouteType.COMMUTER_RAIL)

    if bus:
        route_types.append(RouteType.BUS)

    if ferry:
        route_types.append(RouteType.FERRY)

    _validate_route_types(route_types)

    # Retrieve the data
    route_names_by_id = get_route_ids_to_long_names(route_types)
    route_names = route_names_by_id.values()

    # Format the output into a table
    table_data = {"Route": route_names}

    click.echo()
    click.echo(tabulate(table_data, headers="keys"))
    click.echo()


@click.command()
@_light_rail_option
@_heavy_rail_option
@_commuter_rail_option
@_bus_option
@_ferry_option
def stops(
    light_rail: bool,
    heavy_rail: bool,
    commuter_rail: bool,
    bus: bool,
    ferry: bool,
) -> None:
    """
    Get a table of route names with number of stops of all chosen route types.

    Table is ordered first from most to least number of stops and then alphabetically
    by route name.

    At least one route type flag is required.
    """

    # Validate inputs
    route_types: list[RouteType] = []
    if light_rail:
        route_types.append(RouteType.LIGHT_RAIL)

    if heavy_rail:
        route_types.append(RouteType.HEAVY_RAIL)

    if commuter_rail:
        route_types.append(RouteType.COMMUTER_RAIL)

    if bus:
        route_types.append(RouteType.BUS)

    if ferry:
        route_types.append(RouteType.FERRY)

    _validate_route_types(route_types)

    # Retrieve the data
    route_names_by_id = get_route_ids_to_long_names(route_types)
    route_ids = list(route_names_by_id.keys())
    stops_by_route = _get_stops_by_route(route_ids)

    # Filter and sort the data
    stop_count_by_route = {
        route_id: len(stop_names) for route_id, stop_names in stops_by_route.items()
    }
    stop_count_by_route = dict(
        sorted(stop_count_by_route.items(), key=lambda item: item[1], reverse=True)
    )

    # Format the output into a table and render
    table_data: dict[str, list] = {
        "Route": [],
        "Stops": [],
    }
    for route_id, num_stops in stop_count_by_route.items():
        table_data["Route"] += [route_names_by_id[route_id]]
        table_data["Stops"] += [num_stops]

    click.echo()
    click.echo(tabulate(table_data, headers="keys"))
    click.echo()


@click.command()
@_light_rail_option
@_heavy_rail_option
@_commuter_rail_option
@_bus_option
@_ferry_option
def connections(
    light_rail: bool,
    heavy_rail: bool,
    commuter_rail: bool,
    bus: bool,
    ferry: bool,
) -> None:
    """
    Get a table of stops that serve as connections between multiple routes.

    Table is ordered alphabetically by stop name with corresponding routes also
    order alphabetically.

    At least one route type flag is required.
    """

    # Validate inputs
    route_types: list[RouteType] = []
    if light_rail:
        route_types.append(RouteType.LIGHT_RAIL)

    if heavy_rail:
        route_types.append(RouteType.HEAVY_RAIL)

    if commuter_rail:
        route_types.append(RouteType.COMMUTER_RAIL)

    if bus:
        route_types.append(RouteType.BUS)

    if ferry:
        route_types.append(RouteType.FERRY)

    _validate_route_types(route_types)

    # Retrieve the data
    route_names_by_id = get_route_ids_to_long_names(route_types)
    route_ids = list(route_names_by_id.keys())
    stops_by_route = _get_stops_by_route(route_ids)
    routes_by_stop = invert_dictionary(stops_by_route)

    # Filter and sort the data
    connecting_stops_to_route_ids = {
        stop_name: sorted(route_ids)
        for stop_name, route_ids in routes_by_stop.items()
        if len(route_ids) > 1
    }
    connecting_stops_to_route_ids = dict(sorted(connecting_stops_to_route_ids.items()))

    # Format the output into a table and render
    table_data: dict[str, list] = {
        "Stops": [],
        "Routes": [],
    }
    for stop_name, route_ids in connecting_stops_to_route_ids.items():
        table_data["Stops"] += [stop_name]

        route_names = []
        for route_id in route_ids:
            route_names += [route_names_by_id[route_id]]

        table_data["Routes"] += [", ".join(route_names)]

    click.echo()
    click.echo(tabulate(table_data, headers="keys"))
    click.echo()


# Intentional pylint disable block (re-enabled after function below)
# pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals


@click.command()
@click.argument(
    "start",
    required=True,
    type=str,
    help="The origin station at the start of the intended travel path",
)
@click.argument(
    "end",
    required=True,
    type=str,
    help="The destination station at the end of the intended travel path",
)
@_light_rail_option
@_heavy_rail_option
@_commuter_rail_option
@_bus_option
@_ferry_option
def travel(
    start: str,
    end: str,
    light_rail: bool,
    heavy_rail: bool,
    commuter_rail: bool,
    bus: bool,
    ferry: bool,
) -> None:
    """
    Get a table of steps that serve as directions on how to get from a starting
    station to a destination station across all route types selected.

    Table is ordered chronologically by step with user-friendly instructions.

    At least one route type flag is required.
    """

    # Validate inputs
    start = start.title()
    end = end.title()

    route_types: list[RouteType] = []
    if light_rail:
        route_types.append(RouteType.LIGHT_RAIL)

    if heavy_rail:
        route_types.append(RouteType.HEAVY_RAIL)

    if commuter_rail:
        route_types.append(RouteType.COMMUTER_RAIL)

    if bus:
        route_types.append(RouteType.BUS)

    if ferry:
        route_types.append(RouteType.FERRY)

    _validate_route_types(route_types)

    # Retrieve the data
    route_names_by_id = get_route_ids_to_long_names(route_types)
    route_ids = list(route_names_by_id.keys())
    stops_by_route = _get_stops_by_route(route_ids)
    routes_by_stop = invert_dictionary(stops_by_route)

    valid_stop_names = [
        stop_name.title() for stop_name in sorted(routes_by_stop.keys())
    ]
    _validate_stop_name(start, valid_stop_names)
    _validate_stop_name(end, valid_stop_names)

    # Setup data structures
    graph = _get_graph_from_stops(valid_stop_names, stops_by_route)

    # Navigate through the graph
    path = graph.get_path(start, end)
    _validate_path(start, end, path)

    path_route_guidance = _get_path_route_guidance(path, routes_by_stop)

    # Format the output into a table and render
    table_data: dict[str, list] = {
        "Step": [],
        "From Here": [],
        "Take Any of These Routes to the Next Step": [],
    }
    step_number = 1
    for stop_name, guiding_route_ids in path_route_guidance.items():
        table_data["Step"] += [step_number]
        table_data["From Here"] += [stop_name]

        route_names = []
        for route_id in guiding_route_ids:
            route_names += [route_names_by_id[route_id]]

        table_data["Take Any of These Routes to the Next Step"] += [
            ", ".join(route_names)
        ]
        step_number += 1

    click.echo()
    click.echo(tabulate(table_data, headers="keys"))
    click.echo()


# pylint: enable=too-many-arguments,too-many-positional-arguments,too-many-locals
