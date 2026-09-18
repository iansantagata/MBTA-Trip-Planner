"""
The CLI entry point for this MBTA wrapper app
"""

import click

from client import get_route_long_names
from enums import RouteType


@click.command()
@click.option(
    "--light-rail",
    "-l",
    is_flag=True,
    type=bool,
    default=False,
    help="Resulting route names will include light rail routes",
)
@click.option(
    "--heavy-rail",
    "-h",
    is_flag=True,
    type=bool,
    default=False,
    help="Resulting route names will include heavy rail routes",
)
@click.option(
    "--commuter-rail",
    "-c",
    is_flag=True,
    type=bool,
    default=False,
    help="Resulting route names will include commuter rail routes",
)
@click.option(
    "--bus",
    "-b",
    is_flag=True,
    type=bool,
    default=False,
    help="Resulting route names will include bus routes",
)
@click.option(
    "--ferry",
    "-f",
    is_flag=True,
    type=bool,
    default=False,
    help="Resulting route names will include ferry routes",
)
def routes(
    light_rail: bool,
    heavy_rail: bool,
    commuter_rail: bool,
    bus: bool,
    ferry: bool,
) -> None:
    """
    Get an ordered list of all of the names of routes of all chosen route types.

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

    route_names = get_route_long_names(route_types)
    click.echo(", ".join(route_names))


def _validate_route_types(route_types: list[RouteType]) -> None:
    """
    Validates that at least one route type is included to be queried
    """

    if not route_types:
        raise click.UsageError(
            "At least one route type option must be included in the search"
        )
