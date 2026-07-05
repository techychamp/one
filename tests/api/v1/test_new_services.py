import pytest
import asyncio
from omlx.api.v1 import (
    ModelService, ModelLoadBuilder, ModelDescriptor, ModelInfo,
    GenerationService, GenerateRequestBuilder, StreamRequestBuilder,
    StreamingService,
    ObservationService, ObservationQueryBuilder,
    QuantizationService, CapabilityService
)

def test_model_service():
    service = ModelService()
    builder = ModelLoadBuilder()
    req = builder.with_model_id("test").build()

    assert service.load_model(req)
    assert service.unload_model("test")
    assert isinstance(service.list_models(), list)
    assert service.model_information("test") is None

def test_generation_service():
    service = GenerationService()
    builder = GenerateRequestBuilder()
    req = builder.with_model("test").with_prompt("hello").build()

    resp = service.generate(req)
    assert resp.text == "generated text"

    batch_resp = service.batch_generate([req])
    assert len(batch_resp) == 1
    assert batch_resp[0].text == "generated text"

@pytest.mark.asyncio
async def test_streaming_service():
    service = GenerationService()
    builder = StreamRequestBuilder()
    req = builder.with_model("test").with_prompt("hello").build()

    chunks = []
    async for chunk in service.stream(req):
        chunks.append(chunk)

    assert len(chunks) == 2
    assert chunks[0].text_chunk == "chunk"
    assert chunks[1].is_finished

def test_streaming_lifecycle():
    service = StreamingService()
    assert isinstance(service.stream_subscriptions(), list)
    assert service.stream_status("id") == "active"
    assert service.stream_lifecycle("id", "stop")

def test_observation_service():
    service = ObservationService()
    builder = ObservationQueryBuilder()
    req = builder.with_session("sess").build()

    assert isinstance(service.sessions(), list)
    assert isinstance(service.timeline("sess"), list)
    assert isinstance(service.statistics("sess"), dict)
    assert isinstance(service.diagnostics("sess"), dict)

def test_quantization_service():
    service = QuantizationService()
    info = service.get_info("test")
    assert info.method == "awq"

def test_capability_service():
    service = CapabilityService()
    caps = service.list_capabilities()
    assert len(caps) > 0
    assert caps[0].name == "attention"
