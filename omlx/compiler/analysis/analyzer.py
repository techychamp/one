# SPDX-License-Identifier: Apache-2.0

import os
import json
from pathlib import Path
from typing import Optional, Any
from omlx.framework.model_intelligence.descriptor import ModelDescriptor
from omlx.planner.ir.graph import ExecutionIR
from .report import CapabilityReport
from .capability_compiler import CapabilityCompiler
from .feature_detector import FeatureDetector
from .constraint_compiler import ConstraintCompiler
from .diagnostics import DiagnosticsEngine

class AnalysisCache:
    """Persists analysis results to disk."""

    def __init__(self, cache_dir: str = ".omlx_cache/analysis"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, model_id: str) -> Path:
        # Sanitize model_id for filename
        safe_id = model_id.replace("/", "_").replace("\\", "_")
        return self.cache_dir / f"{safe_id}.analysis.json"

    def save(self, model_id: str, report: CapabilityReport) -> None:
        path = self._get_path(model_id)
        with open(path, "w") as f:
            f.write(report.to_json())

    def load(self, model_id: str) -> Optional[CapabilityReport]:
        path = self._get_path(model_id)
        if not path.exists():
            return None

        with open(path, "r") as f:
            data = json.load(f)
            return CapabilityReport.from_dict(data)

class GraphAnalyzer:
    """Orchestrates model analysis."""

    def __init__(self, use_cache: bool = True):
        self.capability_compiler = CapabilityCompiler()
        self.feature_detector = FeatureDetector()
        self.constraint_compiler = ConstraintCompiler()
        self.diagnostics_engine = DiagnosticsEngine()
        self.cache = AnalysisCache() if use_cache else None

    def analyze(self, descriptor: ModelDescriptor, ir: ExecutionIR) -> CapabilityReport:
        """Analyzes a model and produces a CapabilityReport."""

        if self.cache and descriptor.model_id:
            cached_report = self.cache.load(descriptor.model_id)
            if cached_report:
                return cached_report

        # Phase 1-2: Extract Capabilities
        capabilities = self.capability_compiler.extract_capabilities(descriptor, ir)

        # Phase 3: Detect Features
        features = self.feature_detector.detect_features(descriptor, ir)

        # Phase 5-6: Constraints and Requirements
        constraints = self.constraint_compiler.compile_constraints(descriptor, ir)
        requirements = self.constraint_compiler.compile_requirements(descriptor, ir, features)

        # Phase 7: Diagnostics (Unsupported features)
        unsupported = self.diagnostics_engine.analyze_unsupported(descriptor, ir)

        # Phase 8: Generate Report
        report = CapabilityReport(
            architecture=descriptor.architecture,
            capabilities=capabilities,
            features=features,
            requirements=requirements,
            constraints=constraints,
            unsupported=unsupported
        )

        # Phase 9: Cache Analysis
        if self.cache and descriptor.model_id:
            self.cache.save(descriptor.model_id, report)

        return report
