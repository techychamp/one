from typing import List, Optional, AsyncGenerator
from pydantic import BaseModel, Field
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

class GenerationService:
    def generate(self, request: GenerateRequest) -> GenerateResponse:
        return GenerateResponse(text="generated text", finish_reason="stop", tokens_generated=10)

    async def stream(self, request: StreamRequest) -> AsyncGenerator[StreamResponse, None]:
        yield StreamResponse(text_chunk="chunk", is_finished=False)
        yield StreamResponse(text_chunk="", is_finished=True)

    def batch_generate(self, requests: List[GenerateRequest]) -> List[GenerateResponse]:
        return [self.generate(r) for r in requests]
