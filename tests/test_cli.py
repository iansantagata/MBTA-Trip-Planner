from click.testing import CliRunner
from tabulate import tabulate

from cli import routes, stops


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

    mock_stop_data = 23
    mocker.patch("cli.get_num_stops_on_route", return_value=mock_stop_data)

    runner = CliRunner()

    result = runner.invoke(stops, ["-l"])
    expected = tabulate([["Green Line B", 23]], headers=["Route", "Stops"])

    assert result.exit_code == 0
    assert result.exception is None
    assert result.output.strip("\n") == expected
