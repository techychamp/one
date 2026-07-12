from omlx.compiler.graph.builder import Graph
from omlx.compiler.ir.core import Node, Edge
from omlx.compiler.operators.standard import Attention
from omlx.compiler.cmr.models import CanonicalModelRepresentation
from omlx.compiler.validation.validator import GraphValidator

def test_graph_validation_cycle():
    graph = Graph()

    op1 = Attention(name="attn1", inputs=["x"], outputs=["y"])
    node1 = Node(id="n1", operator=op1)

    op2 = Attention(name="attn2", inputs=["y"], outputs=["x"])
    node2 = Node(id="n2", operator=op2)

    graph.add_node(node1)
    graph.add_node(node2)

    graph.add_edge(Edge(source_node="n1", target_node="n2", tensor_name="y"))
    graph.add_edge(Edge(source_node="n2", target_node="n1", tensor_name="x"))

    cmr = CanonicalModelRepresentation(architecture="llama")
    validator = GraphValidator()

    errors = validator.validate(graph, cmr)
    assert len(errors) == 1
    assert "Graph contains a cycle" in errors[0]
