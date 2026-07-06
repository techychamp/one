from typing import List, Optional, Any
from pydantic import BaseModel, Field

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
    def __init__(self, internal_runtime: Any):
        self._runtime = internal_runtime

    def load_model(self, request: dict) -> bool:
        # Pass to internal engine pool if implemented
        if hasattr(self._runtime, "engine_pool") and self._runtime.engine_pool:
            # Assuming a load method exists on the pool
            if hasattr(self._runtime.engine_pool, "load"):
                return self._runtime.engine_pool.load(request["model_id"])
        return True

    def unload_model(self, model_id: str) -> bool:
        if hasattr(self._runtime, "engine_pool") and self._runtime.engine_pool:
            if hasattr(self._runtime.engine_pool, "unload"):
                return self._runtime.engine_pool.unload(model_id)
        return True

    def list_models(self) -> List[ModelInfo]:
        if hasattr(self._runtime, "engine_pool") and self._runtime.engine_pool:
             if hasattr(self._runtime.engine_pool, "list_models"):
                 return [ModelInfo(descriptor=ModelDescriptor(model_id=m, architecture="unknown", parameters_billions=0.0, quantization="none"), is_loaded=True, memory_usage_mb=0) for m in self._runtime.engine_pool.list_models()]
        return []

    def model_information(self, model_id: str) -> Optional[ModelInfo]:
        return None
