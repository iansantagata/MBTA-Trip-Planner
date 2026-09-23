import pytest

from graph import Graph, Node


def test_graph_node_addition_success() -> None:
    test_node_name = "test"
    test_node = Node(name=test_node_name)

    graph = Graph()
    graph.add_node(test_node_name)

    assert list(graph.nodes.keys()) == [test_node_name]
    assert list(graph.nodes.values()) == [test_node]


def test_graph_node_addition_does_not_add_duplicate_node_with_name_collision() -> None:
    test_node_name = "test"

    graph = Graph()
    graph.add_node(test_node_name)
    graph.add_node(test_node_name)

    assert len(graph.nodes) == 1


def test_graph_node_retrieval_success() -> None:
    test_node_name = "test"

    graph = Graph()
    graph.add_node(test_node_name)

    actual = Node(test_node_name)
    expected = graph.get_node(test_node_name)

    assert actual == expected


def test_graph_node_retrieval_returns_none_on_failure() -> None:
    graph = Graph()

    actual = graph.get_node("test")
    expected = None

    assert actual == expected


def test_graph_edge_addition_success() -> None:
    first_node_name = "first"
    second_node_name = "second"

    graph = Graph()

    graph.add_node(first_node_name)
    graph.add_node(second_node_name)

    graph.add_edge(first_node_name, second_node_name)

    first_node = graph.get_node(first_node_name)
    second_node = graph.get_node(second_node_name)

    assert first_node
    assert second_node
    assert first_node in second_node.adjacent_nodes
    assert second_node in first_node.adjacent_nodes


def test_graph_edge_addition_does_not_add_edge_on_same_node() -> None:
    test_node_name = "test"

    graph = Graph()

    graph.add_node(test_node_name)

    graph.add_edge(test_node_name, test_node_name)

    test_node = graph.get_node(test_node_name)

    assert test_node
    assert len(test_node.adjacent_nodes) == 0


def test_graph_edge_addition_does_not_add_edge_on_missing_node() -> None:
    test_node_name = "test"
    missing_node_name = "missing"

    graph = Graph()

    graph.add_node(test_node_name)

    graph.add_edge(test_node_name, missing_node_name)
    graph.add_edge(missing_node_name, test_node_name)

    test_node = graph.get_node(test_node_name)

    assert test_node
    assert len(test_node.adjacent_nodes) == 0


def test_graph_path_finding_success() -> None:
    first_node_name = "first"
    second_node_name = "second"
    third_node_name = "third"

    first_node = Node(first_node_name)
    second_node = Node(second_node_name)
    third_node = Node(third_node_name)

    graph = Graph()

    graph.add_node(first_node_name)
    graph.add_node(second_node_name)
    graph.add_node(third_node_name)

    graph.add_edge(first_node_name, second_node_name)
    graph.add_edge(second_node_name, third_node_name)

    actual = graph.get_path(first_node_name, third_node_name)
    expected = [first_node, second_node, third_node]

    assert actual == expected


def test_graph_path_finding_returns_empty_list_on_invalid_start_node() -> None:
    test_node_name = "test"
    missing_node_name = "missing"

    graph = Graph()

    graph.add_node(test_node_name)

    actual = graph.get_path(test_node_name, missing_node_name)
    expected: list = []

    assert actual == expected


def test_graph_path_finding_returns_empty_list_on_invalid_end_node() -> None:
    test_node_name = "test"
    missing_node_name = "missing"

    graph = Graph()

    graph.add_node(test_node_name)

    actual = graph.get_path(missing_node_name, test_node_name)
    expected: list = []

    assert actual == expected


def test_graph_path_finding_returns_empty_list_on_disjointed_graph() -> None:
    first_node_name = "first"
    second_node_name = "second"
    third_node_name = "third"

    graph = Graph()

    graph.add_node(first_node_name)
    graph.add_node(second_node_name)
    graph.add_node(third_node_name)

    graph.add_edge(first_node_name, second_node_name)

    actual = graph.get_path(first_node_name, third_node_name)
    expected: list = []

    assert actual == expected
