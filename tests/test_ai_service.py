import pytest

from app.services.ai_service import AIService
from app.config import settings


def test_ensure_gemini_api_key_missing(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")

    service = AIService()

    with pytest.raises(RuntimeError, match="GEMINI_API_KEY not set"):
        service._ensure_gemini()


def test_generate_success(monkeypatch):
    class FakeResponse:
        text = "AI response"

    class FakeModel:
        def __init__(self, model_name):
            self.model_name = model_name

        def generate_content(self, prompt):
            return FakeResponse()

    class FakeGenAI:
        def configure(self, api_key):
            pass

        GenerativeModel = FakeModel

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "fake-key")
    monkeypatch.setattr(settings, "GEMINI_MODEL", "gemini-test")

    service = AIService()
    service._gemini = FakeGenAI()

    result = service.generate("Hello")

    assert result == "AI response"


def test_generate_empty_response(monkeypatch):
    class FakeResponse:
        text = None

    class FakeModel:
        def __init__(self, model_name):
            pass

        def generate_content(self, prompt):
            return FakeResponse()

    class FakeGenAI:
        def configure(self, api_key):
            pass

        GenerativeModel = FakeModel

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "fake-key")

    service = AIService()
    service._gemini = FakeGenAI()

    result = service.generate("Hello")

    assert result == ""


def test_generate_raises_exception(monkeypatch):
    class FakeModel:
        def __init__(self, model_name):
            pass

        def generate_content(self, prompt):
            raise Exception("Gemini error")

    class FakeGenAI:
        def configure(self, api_key):
            pass

        GenerativeModel = FakeModel

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "fake-key")

    service = AIService()
    service._gemini = FakeGenAI()

    with pytest.raises(Exception, match="Gemini error"):
        service.generate("Hello")
        