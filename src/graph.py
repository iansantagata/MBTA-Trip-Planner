"""
A set of classes and functionality for working with graphs

Reference - https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    """
    Commonly referred to as a vertex in graphs. Identified exclusively by its name.

    Has additional properties for assisting with graph traversal as needed.
    """

    name: str
    adjacent_nodes: set["Node"] = field(default_factory=set)

    is_explored: bool = False
    previous_node: Optional["Node"] = None

    def __hash__(self):
        """
        Hashing function required for equivalence testing and set usage.
        """

        return hash(self.name)

    def __eq__(self, other):
        """
        Equivalance function using only each node's name as required for set usage.
        """

        if not isinstance(other, Node):
            return False

        return self.name == other.name


@dataclass
class Graph:
    """
    An unweighted graph that represents a collection of nodes that
    may be joined together with edges.

    There is no guarantee that this graph is not disjointed.
    """

    nodes: dict[str, Node] = field(default_factory=dict)

    def add_node(self, name: str) -> None:
        """
        Adds a new unconnected node with the given name to the graph's collection of nodes
        """
        if not self.get_node(name):
            self.nodes[name] = Node(name)

    def add_edge(self, start: str, end: str) -> None:
        """
        Adds an unweighted connection between two named nodes in the graph.

        If the node names provided do not represent unique nodes already in the graph,
        no connection will be made.
        """

        if start == end:
            return

        start_node = self.get_node(start)
        end_node = self.get_node(end)

        if start_node and end_node:
            start_node.adjacent_nodes.add(end_node)
            end_node.adjacent_nodes.add(start_node)

    def get_node(self, name: str) -> Optional[Node]:
        """
        Retrieves an existing node already in the graph by its unique name
        """

        return self.nodes.get(name)

    def get_path(self, start: str, end: str) -> list[Node]:
        """
        Given the current graph's nodes and edges between them, retrieves a path from
        the provided starting node name to the ending node name.

        Note that this path is only guaranteed to represent the shortest path between
        the two nodes if node adjacency is navigationally accurate (i.e. getting from
        node A to adjacent node B does not require moving through any other node).
        """

        start_node = self.get_node(start)
        end_node = self.get_node(end)
        if not start_node or not end_node:
            return []

        start_node.is_explored = True
        search_queue = [start_node]
        path: list[Node] = []

        while len(search_queue) > 0:
            node = search_queue.pop()

            if node.name == end:
                path.insert(0, node)
                while node.previous_node:
                    node = node.previous_node
                    path.insert(0, node)

                break

            # To make this deterministic, sort the unweighted adjacent nodes alphabetically.
            # Without an order, this could choose different adjacent nodes each run,
            # leading to different output on the same request and confusion from the user.
            adjacent_nodes = sorted(node.adjacent_nodes, key=lambda n: n.name)
            for adjacent_node in adjacent_nodes:

                if not adjacent_node.is_explored:
                    adjacent_node.is_explored = True
                    adjacent_node.previous_node = node
                    search_queue.append(adjacent_node)

        return path
