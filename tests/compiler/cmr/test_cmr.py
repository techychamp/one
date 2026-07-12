from omlx.compiler.cmr.models import CanonicalModelRepresentation

def test_cmr_serialization():
    cmr = CanonicalModelRepresentation(
        architecture="llama",
        tensor_metadata={"layers": 32, "hidden_size": 4096},
        capabilities={"chat", "embeddings"}
    )

    data = cmr.to_dict()
    assert data["architecture"] == "llama"
    assert data["tensor_metadata"]["layers"] == 32
    assert "chat" in data["capabilities"]
    assert "embeddings" in data["capabilities"]

    cmr2 = CanonicalModelRepresentation.from_dict(data)
    assert cmr2.architecture == "llama"
    assert cmr2.tensor_metadata["layers"] == 32
    assert cmr2.capabilities == {"chat", "embeddings"}
