from typing import List, Optional
from dataclasses import dataclass
from .capability import ProviderCapability

@dataclass
class ValidationIssue:
    severity: str # "error" or "warning"
    message: str
    field: Optional[str] = None

class ProviderValidator:
    def validate(self, capability: ProviderCapability) -> List[ValidationIssue]:
        issues = []

        # Check required fields
        if not capability.provider:
            issues.append(ValidationIssue("error", "Provider name is required", "provider"))
        if not capability.version:
            issues.append(ValidationIssue("error", "Provider version is required", "version"))

        # Check architectures
        if not capability.architectures:
            issues.append(ValidationIssue("warning", "No supported architectures defined", "architectures"))

        # Check operators
        if not capability.operators:
            issues.append(ValidationIssue("warning", "No supported operators defined", "operators"))

        # Check quantization
        if not capability.quantization:
            issues.append(ValidationIssue("warning", "No supported quantization formats defined", "quantization"))

        # Consistency checks
        if capability.platform_constraints.apple_silicon_only and capability.platform_constraints.cuda_required:
            issues.append(ValidationIssue("error", "Contradictory platform constraints: apple_silicon_only and cuda_required cannot both be True", "platform_constraints"))

        if capability.platform_constraints.cpu_only and (capability.platform_constraints.cuda_required or capability.platform_constraints.metal_required):
            issues.append(ValidationIssue("error", "Contradictory platform constraints: cpu_only cannot be combined with GPU requirements", "platform_constraints"))

        return issues

    def is_valid(self, capability: ProviderCapability) -> bool:
        issues = self.validate(capability)
        return not any(issue.severity == "error" for issue in issues)
