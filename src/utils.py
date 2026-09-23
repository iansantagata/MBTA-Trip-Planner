"""
A set of utility functions that are more generalizable than business logic type functionality
"""

from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")


def invert_dictionary(d: dict[T, list[U]], /) -> dict[U, list[T]]:
    """
    Given a dictionary of keys and values, where the values is a list of some kind,
    invert the dictionary so that the list values are now the keys.

    This inversion makes anything that was previously a key a new member of the list of values.
    """

    inverted: dict[U, list[T]] = {}
    for key, values in d.items():
        for value in values:
            inverted.setdefault(value, []).append(key)

    inverted = dict(sorted(inverted.items()))
    return inverted
