from abc import ABC, abstractmethod
from omlx.compiler.cmr.models import CanonicalModelRepresentation
from omlx.compiler.graph.builder import Graph

class BaseImporter(ABC):
    @abstractmethod
    def build_cmr(self, model_path: str) -> CanonicalModelRepresentation:
        pass

    @abstractmethod
    def generate_ir(self, model_path: str, cmr: CanonicalModelRepresentation) -> Graph:
        pass
