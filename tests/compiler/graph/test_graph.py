from omlx.compiler.graph.builder import Graph
from omlx.compiler.ir.core import Node, Edge
from omlx.compiler.operators.standard import Attention, Linear

def test_graph_building_and_sorting():
    graph = Graph()

    op1 = Attention(name="attn1", inputs=["x"], outputs=["h1"])
    node1 = Node(id="n1", operator=op1)

    op2 = Linear(name="lin1", inputs=["h1"], outputs=["y"])
    node2 = Node(id="n2", operator=op2)

    graph.add_node(node1)
    graph.add_node(node2)

    edge = Edge(source_node="n1", target_node="n2", tensor_name="h1")
    graph.add_edge(edge)

    sorted_nodes = graph.topological_sort()
    assert len(sorted_nodes) == 2
    assert sorted_nodes[0].id == "n1"
    assert sorted_nodes[1].id == "n2"

    data = graph.to_dict()
    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1
