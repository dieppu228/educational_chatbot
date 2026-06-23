import json

import numpy as np

from src.rag import retrieve_rebuild


def test_custom_search_warms_embedding_before_loading_embeddings(monkeypatch, tmp_path):
    events = []

    class FakeEmbeddingModel:
        def warm_up(self):
            events.append("warm_up")

    def fake_load(path):
        events.append("np_load")
        assert events == ["warm_up", "np_load"]
        return np.ones((1, 2), dtype=np.float32)

    chunks_path = tmp_path / "chunks.json"
    chunks_path.write_text(
        json.dumps([{"content": "test", "full_content": "test"}]),
        encoding="utf-8",
    )

    monkeypatch.setattr(retrieve_rebuild, "EmbeddingModel", FakeEmbeddingModel)
    monkeypatch.setattr(retrieve_rebuild.np, "load", fake_load)

    search = retrieve_rebuild.CustomSearch(
        chunks_path=str(chunks_path),
        embeddings_path=str(tmp_path / "embeddings.npy"),
    )

    assert isinstance(search._model, FakeEmbeddingModel)
    assert events == ["warm_up", "np_load"]
