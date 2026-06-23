from pathlib import Path

from src.config.config import PROJECT_ROOT, Settings, project_path
from src.config import genai_client


def test_os_environment_overrides_dotenv(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "EDUBOT_PORT=7000\n"
        "TAVILY_API_KEY=from-file\n"
        "TAVILY_INCLUDE_IMAGES=false\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("EDUBOT_PORT", "9000")
    monkeypatch.setenv("TAVILY_API_KEY", "from-process")

    config = Settings(_env_file=env_file)

    assert config.EDUBOT_PORT == 9000
    assert config.TAVILY_API_KEY == "from-process"
    assert config.TAVILY_INCLUDE_IMAGES is False


def test_explicit_settings_value_overrides_environment(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "model-from-process")

    config = Settings(LLM_MODEL="model-from-constructor", _env_file=None)

    assert config.LLM_MODEL == "model-from-constructor"


def test_project_path_resolves_relative_and_preserves_absolute(tmp_path):
    assert project_path("data/example.json") == PROJECT_ROOT / "data/example.json"
    assert project_path(tmp_path) == Path(tmp_path)


def test_genai_client_uses_configured_endpoint_and_timeout(monkeypatch):
    captured = {}

    def fake_client(**kwargs):
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(genai_client.genai, "Client", fake_client)
    monkeypatch.setattr(genai_client.settings, "GENAI_BASE_URL", "https://llm.example.test")
    monkeypatch.setattr(genai_client.settings, "GENAI_API_VERSION", "v1beta")

    genai_client.create_genai_client(api_key="explicit-key", timeout_seconds=12)

    assert captured["api_key"] == "explicit-key"
    assert captured["http_options"].base_url == "https://llm.example.test"
    assert captured["http_options"].api_version == "v1beta"
    assert captured["http_options"].timeout == 12000
