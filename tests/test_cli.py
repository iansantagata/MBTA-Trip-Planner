from click.testing import CliRunner
from tabulate import tabulate

from cli import connections, routes, stops


def test_routes_without_flag_raises_exception() -> None:
    runner = CliRunner()
    result = runner.invoke(routes)

    assert result.exit_code != 0
    assert result.exception is not None


def test_routes_with_flag_succeeds(mocker) -> None:
    mock_data = {
        "Green-B": "Green Line B",
    }
    mocker.patch("cli.get_route_ids_to_long_names", return_value=mock_data)

    runner = CliRunner()

    result = runner.invoke(routes, ["-l"])
    expected = tabulate([["Green Line B"]], headers=["Route"])

    assert result.exit_code == 0
    assert result.exception is None
    assert result.output.strip("\n") == expected


def test_stops_without_flag_raises_exception() -> None:
    runner = CliRunner()
    result = runner.invoke(stops)

    assert result.exit_code != 0
    assert result.exception is not None


def test_stops_with_flag_succeeds(mocker) -> None:
    mock_route_data = {
        "Green-B": "Green Line B",
    }
    mocker.patch("cli.get_route_ids_to_long_names", return_value=mock_route_data)

    mock_stop_data = range(23)
    mocker.patch("cli.get_stops_on_route", return_value=mock_stop_data)

    runner = CliRunner()

    result = runner.invoke(stops, ["-l"])
    expected = tabulate([["Green Line B", 23]], headers=["Route", "Stops"])

    assert result.exit_code == 0
    assert result.exception is None
    assert result.output.strip("\n") == expected


def test_connections_without_flag_raises_exception() -> None:
    runner = CliRunner()
    result = runner.invoke(connections)

    assert result.exit_code != 0
    assert result.exception is not None


def test_connections_with_flag_succeeds(mocker) -> None:
    mock_route_data = {
        "Green-B": "Green Line B",
        "Green-E": "Green Line E",
    }
    mocker.patch("cli.get_route_ids_to_long_names", return_value=mock_route_data)

    first_request_mock_stop_data = [
        "Arlington",
        "Boylston",
        "Copley",
        "Government Center",
        "Hynes Convention Center",
        "Kenmore",
        "Park Street",
    ]
    second_request_mock_stop_data = [
        "Arlington",
        "Boylston",
        "Copley",
        "Government Center",
        "Haymarket",
        "Lechmere",
        "North Station",
        "Park Street",
        "Science Park/West End",
    ]
    mocker.patch(
        "cli.get_stops_on_route",
        side_effect=[first_request_mock_stop_data, second_request_mock_stop_data],
    )

    runner = CliRunner()
    result = runner.invoke(connections, ["-l"])

    table_data = [
        ["Arlington", "Green Line B, Green Line E"],
        ["Boylston", "Green Line B, Green Line E"],
        ["Copley", "Green Line B, Green Line E"],
        ["Government Center", "Green Line B, Green Line E"],
        ["Park Street", "Green Line B, Green Line E"],
    ]
    expected = tabulate(table_data, headers=["Stops", "Routes"])

    assert result.exit_code == 0
    assert result.exception is None
    assert result.output.strip("\n") == expected
