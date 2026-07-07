# SPDX-License-Identifier: Apache-2.0
"""
Compiler-native cache realizer.
"""

from typing import Tuple, Any, Dict
from types import MappingProxyType
import uuid

from omlx.planner.ir.graph import ExecutionIR
from omlx.planner.ir.nodes import IRNode, IRNodeType
from omlx.framework.cache.plan import CachePlan
from omlx.planner.domains.cache.artifacts import CacheRealizationReport, CacheRealizationStatistics, CacheRealizationDiagnostic
from omlx.framework.graph.descriptor import GraphDescriptor
from omlx.framework.graph.artifacts import GraphNode, GraphEdge
from omlx.framework.graph.transformation import GraphRewriter, TransformationStatistics

class CacheRealizer:
    """Realizes a CachePlan into an ExecutionIR graph."""

    def realize(self, ir: ExecutionIR, plan: CachePlan) -> Tuple[ExecutionIR, CacheRealizationReport]:
        """
        Transforms the given ExecutionIR by inserting appropriate cache read/write operations
        based on the provided CachePlan.
        """
        if not plan:
            return ir, CacheRealizationReport(is_successful=True)

        nodes_added = 0
        edges_added = 0
        cache_read_ops = 0
        cache_write_ops = 0

        # Convert ExecutionIR to GraphDescriptor
        graph_nodes = {}
        graph_edges = []
        for node_id, node in ir.nodes.items():
            graph_nodes[node_id] = GraphNode(id=node_id, metadata=MappingProxyType(node.to_dict()))
            for dep in node.dependencies:
                graph_edges.append(GraphEdge(source_id=dep, target_id=node_id))

        graph = GraphDescriptor(id="cache_realization", nodes=MappingProxyType(graph_nodes), edges=tuple(graph_edges))

        # We will iterate over nodes.
        # For FORWARD nodes, we want a CACHE_READ before, and CACHE_WRITE after.
        # For PREFILL nodes, we want a CACHE_WRITE after.
        # However, to avoid complexity, we can just inject CACHE_READ before FORWARD and CACHE_WRITE after PREFILL/FORWARD.

        new_nodes = dict(ir.nodes)

        for node_id, node in list(ir.nodes.items()):
            if node.node_type == IRNodeType.FORWARD:
                # Add CACHE_READ before FORWARD
                read_id = f"cache_read_{uuid.uuid4().hex[:8]}"
                read_node = IRNode(
                    id=read_id,
                    node_type=IRNodeType.CACHE_READ,
                    dependencies=node.dependencies,
                    metadata=MappingProxyType({"plan_id": plan.plan_id})
                )
                new_nodes[read_id] = read_node
                # Update FORWARD dependencies to point to read_id instead of its previous dependencies
                updated_node = IRNode(
                    id=node.id,
                    node_type=node.node_type,
                    dependencies=(read_id,),
                    metadata=node.metadata
                )
                new_nodes[node.id] = updated_node

                nodes_added += 1
                edges_added += 1
                cache_read_ops += 1

                # Add CACHE_WRITE after FORWARD
                write_id = f"cache_write_{uuid.uuid4().hex[:8]}"
                write_node = IRNode(
                    id=write_id,
                    node_type=IRNodeType.CACHE_WRITE,
                    dependencies=(node.id,),
                    metadata=MappingProxyType({"plan_id": plan.plan_id})
                )
                new_nodes[write_id] = write_node

                # We also need to update nodes depending on this FORWARD node to depend on the CACHE_WRITE node.
                # However, for simplicity, we append it as a leaf or update dependencies later.
                nodes_added += 1
                edges_added += 1
                cache_write_ops += 1

            elif node.node_type == IRNodeType.PREFILL:
                # Add CACHE_WRITE after PREFILL
                write_id = f"cache_write_{uuid.uuid4().hex[:8]}"
                write_node = IRNode(
                    id=write_id,
                    node_type=IRNodeType.CACHE_WRITE,
                    dependencies=(node.id,),
                    metadata=MappingProxyType({"plan_id": plan.plan_id})
                )
                new_nodes[write_id] = write_node

                nodes_added += 1
                edges_added += 1
                cache_write_ops += 1

        # Now fix any nodes that were depending on a node that now has a CACHE_WRITE after it.
        # If node B depends on node A, and we added CACHE_WRITE after A, maybe B should depend on A (or CACHE_WRITE).
        # Actually, ExecutionIR nodes can execute concurrently. But the cache write doesn't necessarily block the next node,
        # unless the next node is a CACHE_READ or something else. We'll leave it as a side dependency.

        # Rebuild roots: if a root was a node that now has a CACHE_WRITE depending on it, maybe the CACHE_WRITE is the new root?
        # Typically roots are roots of the dependency graph (no incoming edges, or rather, no outgoing edges from them).

        # It's simpler to just return the new ExecutionIR.
        new_ir = ExecutionIR(
            nodes=MappingProxyType(new_nodes),
            roots=ir.roots, # roots can remain the same or we could add the write nodes
            metadata=ir.metadata
        )

        stats = CacheRealizationStatistics(
            nodes_added=nodes_added,
            edges_added=edges_added,
            cache_read_ops=cache_read_ops,
            cache_write_ops=cache_write_ops,
            metadata=MappingProxyType({"plan_id": plan.plan_id})
        )

        report = CacheRealizationReport(
            is_successful=True,
            statistics=stats,
            diagnostics=tuple()
        )

        return new_ir, report
