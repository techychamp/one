from typing import List, Optional
from pydantic import BaseModel, Field
import asyncio

class ModelDescriptor(BaseModel, frozen=True):
    model_id: str
    architecture: str
    parameters_billions: float
    quantization: str

class ModelInfo(BaseModel, frozen=True):
    descriptor: ModelDescriptor
    is_loaded: bool
    memory_usage_mb: float

class ModelLoadBuilder:
    def __init__(self):
        self._model_id = None
        self._backend = "mlx"

    def with_model_id(self, model_id: str) -> 'ModelLoadBuilder':
        self._model_id = model_id
        return self

    def with_backend(self, backend: str) -> 'ModelLoadBuilder':
        self._backend = backend
        return self

    def build(self) -> dict:
        return {"model_id": self._model_id, "backend": self._backend}

class ModelService:
    def load_model(self, request: dict) -> bool:
        return True

    def unload_model(self, model_id: str) -> bool:
        return True

    def list_models(self) -> List[ModelInfo]:
        return []

    def model_information(self, model_id: str) -> Optional[ModelInfo]:
        return None
