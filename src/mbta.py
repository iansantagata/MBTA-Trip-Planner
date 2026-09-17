import click
from enums import RouteType
import requests

# TODO - Move these URLs to a different function
BASE_URL = "https://api-v3.mbta.com"
ROUTES_ENDPOINT = "/routes"


@click.command()
@click.option("--include-light-rail", "-l", is_flag=True, type=bool, default=False, help="TODO")
@click.option("--include-heavy-rail", "-h", is_flag=True, type=bool, default=False, help="TODO")
@click.option("--include-commuter-rail", "-c", is_flag=True, type=bool, default=False, help="TODO")
@click.option("--include-bus", "-b", is_flag=True, type=bool, default=False, help="TODO")
@click.option("--include-ferry", "-f", is_flag=True, type=bool, default=False, help="TODO")
def main(
    include_light_rail: bool,
    include_heavy_rail: bool,
    include_commuter_rail: bool,
    include_bus: bool,
    include_ferry: bool,
) -> None:
    """
    TODO - Comment me!
    """

    route_types: list[RouteType] = []
    if include_light_rail:
        route_types.append(RouteType.LIGHT_RAIL)

    if include_heavy_rail:
        route_types.append(RouteType.HEAVY_RAIL)

    if include_commuter_rail:
        route_types.append(RouteType.COMMUTER_RAIL)

    if include_bus:
        route_types.append(RouteType.BUS)

    if include_ferry:
        route_types.append(RouteType.FERRY)

    _validate_route_types(route_types)
    route_type_values = [str(route_type.value) for route_type in route_types]

    # TODO - Separate this request aspect into its own module
    url = BASE_URL + ROUTES_ENDPOINT
    parameters = {
        "fields[route]": "long_name",
        "filter[type]": ",".join(route_type_values),
    }

    response = requests.get(url, params=parameters)
    # TODO - Error handling
    response_body = response.json()

    # TODO - Separate this response processing aspect into a different function
    route_names = set()
    routes: list[dict] = response_body.get("data", [])
    for route in routes:
        route_attributes = route.get("attributes", {})
        route_name = route_attributes.get("long_name", None)
        if route_name:
            route_names.add(route_name)

    ordered_route_names = sorted(route_names)
    click.echo(", ".join(ordered_route_names))


def _validate_route_types(route_types: list[RouteType]) -> None:
    """
    Validates that at least one route type is included to be queried
    """

    if not route_types:
        raise click.UsageError("At least one route type option must be included in the search")


if __name__ == "__main__":
    main()