"""
The CLI entry point for this MBTA wrapper app
"""

import click
from tabulate import tabulate

from client import get_num_stops_on_route, get_route_ids_to_long_names
from enums import RouteType

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
    route_ids = route_names_by_id.keys()
    route_stops_by_id: dict[str, int] = {}
    for route_id in route_ids:
        num_stops = get_num_stops_on_route(route_id)
        route_stops_by_id[route_id] = num_stops

    # Sort the data
    sorted_route_stops_by_id = dict(
        sorted(route_stops_by_id.items(), key=lambda item: item[1], reverse=True)
    )

    # Format the output into a table
    table_data: dict[str, list] = {
        "Route": [],
        "Stops": [],
    }
    for route_id, num_stops in sorted_route_stops_by_id.items():
        table_data["Route"] += [route_names_by_id[route_id]]
        table_data["Stops"] += [num_stops]

    click.echo()
    click.echo(tabulate(table_data, headers="keys"))
    click.echo()


def _validate_route_types(route_types: list[RouteType]) -> None:
    """
    Validates that at least one route type is included to be queried
    """

    if not route_types:
        raise click.UsageError(
            "At least one route type option must be included in the search"
        )
