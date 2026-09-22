from typing import Any

import pytest


@pytest.fixture()
def mock_route_data() -> dict[str, Any]:
    return {
        "data": [
            {
                "attributes": {"long_name": "Green Line B"},
                "id": "Green-B",
                "links": {"self": "/routes/Green-B"},
                "relationships": {
                    "agency": {"data": {"id": "1", "type": "agency"}},
                    "line": {"data": {"id": "line-Green", "type": "line"}},
                },
                "type": "route",
            },
        ],
        "jsonapi": {"version": "1.0"},
    }


@pytest.fixture()
def mock_stop_data() -> dict[str, Any]:
    return {
        "data": [
            {
                "attributes": {
                    "name": "Government Center",
                },
                "id": "place-gover",
                "links": {"self": "/stops/place-gover"},
                "relationships": {
                    "facilities": {
                        "links": {"related": "/facilities/?filter[stop]=place-gover"}
                    },
                    "parent_station": {"data": None},
                    "zone": {"data": None},
                },
                "type": "stop",
            },
            {
                "attributes": {
                    "name": "Park Street",
                },
                "id": "place-pktrm",
                "links": {"self": "/stops/place-pktrm"},
                "relationships": {
                    "facilities": {
                        "links": {"related": "/facilities/?filter[stop]=place-pktrm"}
                    },
                    "parent_station": {"data": None},
                    "zone": {"data": None},
                },
                "type": "stop",
            },
            {
                "attributes": {
                    "name": "Boylston",
                },
                "id": "place-boyls",
                "links": {"self": "/stops/place-boyls"},
                "relationships": {
                    "facilities": {
                        "links": {"related": "/facilities/?filter[stop]=place-boyls"}
                    },
                    "parent_station": {"data": None},
                    "zone": {"data": None},
                },
                "type": "stop",
            },
        ],
        "jsonapi": {"version": "1.0"},
    }


@pytest.fixture()
def mock_requests_with_route_data(mocker, mock_route_data: dict[str, Any]) -> None:
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_route_data
    mocker.patch("requests.get", return_value=mock_response)


@pytest.fixture()
def mock_requests_with_stop_data(mocker, mock_stop_data: dict[str, Any]) -> None:
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_stop_data
    mocker.patch("requests.get", return_value=mock_response)


@pytest.fixture()
def mock_requests_triggered_exception(mocker) -> None:
    mock_response = mocker.MagicMock()
    mock_response.json.side_effect = Exception("Testing Triggered Exception")
    mocker.patch("requests.get", return_value=mock_response)
