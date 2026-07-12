import pytest
from omlx.compiler.providers.capability import ProviderCapability
from omlx.compiler.providers.registry import ProviderRegistry, get_registry

@pytest.fixture
def clean_registry():
    registry = ProviderRegistry()
    return registry

def test_registry_registration(clean_registry):
    cap = ProviderCapability(provider="test_provider", version="1.0")

    clean_registry.register(cap)

    retrieved = clean_registry.get_provider("test_provider")
    assert retrieved is not None
    assert retrieved.provider == "test_provider"

def test_registry_get_all(clean_registry):
    cap1 = ProviderCapability(provider="provider1", version="1.0")
    cap2 = ProviderCapability(provider="provider2", version="2.0")

    clean_registry.register(cap1)
    clean_registry.register(cap2)

    all_providers = clean_registry.get_all_providers()
    assert len(all_providers) == 2
    names = [p.provider for p in all_providers]
    assert "provider1" in names
    assert "provider2" in names

def test_registry_architectures(clean_registry):
    cap = ProviderCapability(
        provider="test_provider",
        version="1.0",
        architectures=["llama", "gemma"]
    )

    clean_registry.register(cap)

    archs = clean_registry.get_supported_architectures("test_provider")
    assert len(archs) == 2
    assert "llama" in archs
    assert "gemma" in archs

    # Non-existent provider
    assert clean_registry.get_supported_architectures("unknown") == []

def test_registry_unregister_and_clear(clean_registry):
    cap = ProviderCapability(provider="test_provider", version="1.0")
    clean_registry.register(cap)
    assert clean_registry.get_provider("test_provider") is not None

    clean_registry.unregister("test_provider")
    assert clean_registry.get_provider("test_provider") is None

    clean_registry.register(cap)
    clean_registry.clear()
    assert clean_registry.get_provider("test_provider") is None

def test_global_registry():
    reg = get_registry()
    assert isinstance(reg, ProviderRegistry)
