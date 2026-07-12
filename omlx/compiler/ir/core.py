from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from omlx.compiler.operators.base import Operator

@dataclass
class Node:
    id: str
    operator: Operator

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "operator_name": self.operator.name,
            "operator_type": self.operator.__class__.__name__,
            "inputs": self.operator.inputs,
            "outputs": self.operator.outputs,
            "parameters": self.operator.parameters,
            "attributes": self.operator.attributes
        }

@dataclass
class Edge:
    source_node: str
    target_node: str
    tensor_name: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
