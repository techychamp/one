# SPDX-License-Identifier: Apache-2.0

import pytest
import os
import json
import tempfile
from pathlib import Path
from types import MappingProxyType

from omlx.framework.model_intelligence.descriptor import ModelDescriptor
from omlx.planner.ir.graph import ExecutionIR
from omlx.planner.ir.nodes import IRNode, IRNodeType
from omlx.compiler.analysis import (
    GraphAnalyzer,
    AnalysisCache,
    CapabilityReport,
    CapabilityCompiler,
    FeatureDetector,
    ConstraintCompiler,
    DiagnosticsEngine
)

@pytest.fixture
def dummy_descriptor():
    return ModelDescriptor(
        model_id="test/llama-3-8b",
        architecture="llama",
        task="chat",
        parameter_count=8_000_000_000,
        context_length=8192,
        tokenizer_family="llama",
        attention_type="gqa",
        kv_cache_support=True
    )

@pytest.fixture
def dummy_ir():
    nodes = {
        "node1": IRNode(id="node1", node_type=IRNodeType.ATTENTION, metadata=MappingProxyType({"rope": True, "rope_type": "dynamic"})),
        "node2": IRNode(id="node2", node_type=IRNodeType.FORWARD, metadata=MappingProxyType({"precision": "fp16"}))
    }
    return ExecutionIR(nodes=MappingProxyType(nodes), roots=("node2",))

def test_capability_compiler(dummy_descriptor, dummy_ir):
    compiler = CapabilityCompiler()
    caps = compiler.extract_capabilities(dummy_descriptor, dummy_ir)

    assert caps["chat"] is True
    assert caps["moe"] is False
    assert caps["vision"] is False

def test_feature_detector(dummy_descriptor, dummy_ir):
    detector = FeatureDetector()
    features = detector.detect_features(dummy_descriptor, dummy_ir)

    assert features["gqa"] is True
    assert features["attention_type"] == "gqa"
    assert features["rope"] == "dynamic"
    assert "flash_attention" not in features

def test_constraint_compiler(dummy_descriptor, dummy_ir):
    compiler = ConstraintCompiler()

    constraints = compiler.compile_constraints(dummy_descriptor, dummy_ir)
    assert "minimum_memory" in constraints
    assert constraints["maximum_sequence_length"] == 8192
    assert "fp16" in constraints["required_precision"]

    features = MappingProxyType({"rope": "dynamic", "gqa": True})
    reqs = compiler.compile_requirements(dummy_descriptor, dummy_ir, features)
    assert "kv_cache" in reqs
    assert "rotary_embedding" in reqs
    assert "tokenizer" in reqs
    assert "sampling" in reqs

def test_diagnostics_engine():
    engine = DiagnosticsEngine()

    desc = ModelDescriptor(task="chat", tokenizer_family="") # Missing tokenizer
    ir = ExecutionIR(nodes=MappingProxyType({
        "n1": IRNode(id="n1", node_type=IRNodeType.FORWARD, metadata=MappingProxyType({"unsupported": True}))
    }), roots=("n1",))

    unsupported = engine.analyze_unsupported(desc, ir)
    assert "missing_tokenizer" in unsupported
    assert "unsupported_operator:forward" in unsupported

def test_report_serialization():
    report = CapabilityReport(
        architecture="llama",
        capabilities=MappingProxyType({"chat": True}),
        features=MappingProxyType({"gqa": True}),
        requirements=("kv_cache",),
        constraints=MappingProxyType({"minimum_memory": "16GB"}),
        unsupported=()
    )

    json_str = report.to_json()
    assert '"architecture": "llama"' in json_str

    data = json.loads(json_str)
    report2 = CapabilityReport.from_dict(data)

    assert report2.architecture == report.architecture
    assert dict(report2.capabilities) == dict(report.capabilities)
    assert report2.requirements == report.requirements

def test_analysis_cache(dummy_descriptor):
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        report = CapabilityReport(architecture="llama")

        cache.save("test/model", report)

        loaded = cache.load("test/model")
        assert loaded is not None
        assert loaded.architecture == "llama"

        assert cache.load("missing/model") is None

def test_graph_analyzer(dummy_descriptor, dummy_ir):
    with tempfile.TemporaryDirectory() as tmpdir:
        analyzer = GraphAnalyzer(use_cache=False)
        analyzer.cache = AnalysisCache(cache_dir=tmpdir)

        report = analyzer.analyze(dummy_descriptor, dummy_ir)

        assert report.architecture == "llama"
        assert report.capabilities["chat"] is True
        assert report.features["rope"] == "dynamic"
        assert "kv_cache" in report.requirements
        assert "minimum_memory" in report.constraints

        # Test loading from cache
        report2 = analyzer.analyze(dummy_descriptor, dummy_ir)
        assert report2.architecture == report.architecture
