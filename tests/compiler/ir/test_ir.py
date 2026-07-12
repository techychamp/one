from omlx.compiler.ir.core import Node, Edge
from omlx.compiler.operators.standard import Linear

def test_node_serialization():
    op = Linear(name="lin1", inputs=["x"], outputs=["y"])
    node = Node(id="n1", operator=op)

    data = node.to_dict()
    assert data["id"] == "n1"
    assert data["operator_name"] == "lin1"
    assert data["operator_type"] == "Linear"
    assert data["inputs"] == ["x"]
    assert data["outputs"] == ["y"]

def test_edge_serialization():
    edge = Edge(source_node="n1", target_node="n2", tensor_name="h")
    data = edge.to_dict()
    assert data["source_node"] == "n1"
    assert data["target_node"] == "n2"
    assert data["tensor_name"] == "h"
