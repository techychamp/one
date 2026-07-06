from typing import List, Optional, AsyncGenerator, Any
from pydantic import BaseModel, Field, ConfigDict
import asyncio

class GenerateRequest(BaseModel, frozen=True):
    model_id: str
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class GenerateResponse(BaseModel, frozen=True):
    text: str
    finish_reason: str
    tokens_generated: int

class StreamRequest(BaseModel, frozen=True):
    model_id: str
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class StreamResponse(BaseModel, frozen=True):
    text_chunk: str
    is_finished: bool

class GenerateRequestBuilder:
    def __init__(self):
        self._model_id = ""
        self._prompt = ""
        self._max_tokens = 100

    def with_model(self, model_id: str) -> 'GenerateRequestBuilder':
        self._model_id = model_id
        return self

    def with_prompt(self, prompt: str) -> 'GenerateRequestBuilder':
        self._prompt = prompt
        return self

    def build(self) -> GenerateRequest:
        return GenerateRequest(model_id=self._model_id, prompt=self._prompt, max_tokens=self._max_tokens)

class StreamRequestBuilder:
    def __init__(self):
        self._model_id = ""
        self._prompt = ""

    def with_model(self, model_id: str) -> 'StreamRequestBuilder':
        self._model_id = model_id
        return self

    def with_prompt(self, prompt: str) -> 'StreamRequestBuilder':
        self._prompt = prompt
        return self

    def build(self) -> StreamRequest:
        return StreamRequest(model_id=self._model_id, prompt=self._prompt)

class RequestContext:
    def __init__(self, model: str, prompt: str):
        self.model = model
        self.prompt = prompt

class GenerationService:
    def __init__(self, internal_runtime: Any):
        self._runtime = internal_runtime

    def generate(self, request: GenerateRequest) -> GenerateResponse:
        ctx = RequestContext(model=request.model_id, prompt=request.prompt)
        res = self._runtime.generate(
            request_context=ctx,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return GenerateResponse(
            text=res.get("generated_text", ""),
            finish_reason="stop",
            tokens_generated=len(res.get("tokens", []))
        )

    async def stream(self, request: StreamRequest) -> AsyncGenerator[StreamResponse, None]:
        ctx = RequestContext(model=request.model_id, prompt=request.prompt)
        # Note: In a fully implemented async streaming environment we would listen to events
        # but the current generate() method blocks and runs synchronously.
        # This is a shim simulating async delivery for API contracts using run_in_executor
        res = await asyncio.to_thread(self._runtime.generate, ctx, request.max_tokens, request.temperature)
        yield StreamResponse(text_chunk=res.get("generated_text", ""), is_finished=True)

    def batch_generate(self, requests: List[GenerateRequest]) -> List[GenerateResponse]:
        return [self.generate(r) for r in requests]
