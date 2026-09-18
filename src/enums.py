"""
Contains any enumerations that help to translate from CLI usage to MBTA API values
"""

from enum import IntEnum


class RouteType(IntEnum):
    """
    An enum representing different route types used by the MBTA

    Reference: https://github.com/google/transit/blob/master/gtfs/spec/en/reference.md#routestxt
    """

    LIGHT_RAIL = 0
    HEAVY_RAIL = 1
    COMMUTER_RAIL = 2
    BUS = 3
    FERRY = 4
