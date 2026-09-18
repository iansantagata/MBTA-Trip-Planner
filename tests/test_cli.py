from typing import Any

from click.testing import CliRunner

from cli import routes


def test_routes_without_flag_raises_exception() -> None:
    runner = CliRunner()
    result = runner.invoke(routes)

    assert result.exit_code != 0
    assert result.exception is not None


def test_routes_with_flag_succeeds(mock_requests_with_route_data) -> None:
    runner = CliRunner()

    result = runner.invoke(routes, ["-l"])
    expected = "Green Line B\n"

    assert result.exit_code == 0
    assert result.exception is None
    assert result.output == expected
