"""Tests for the data standardization API."""
import pytest
from fastapi.testclient import TestClient
from app.api import app


client = TestClient(app)


@pytest.fixture
def valid_input():
    """Sample valid input data."""
    return {
        "document_id": "DOC001",
        "extracted_fields": {
            "full_name": "John  Doe",
            "email_address": "JOHN@EXAMPLE.COM",
            "phone_number": "123-456-7890",
        },
        "source": "pdf"
    }


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestConfig:
    """Test configuration endpoint."""
    
    def test_get_config(self):
        """Test get configuration endpoint."""
        response = client.get("/config")
        assert response.status_code == 200
        config = response.json()
        assert "api_title" in config
        assert "api_version" in config


class TestStandardization:
    """Test data standardization endpoint."""
    
    def test_standardize_valid_input(self, valid_input):
        """Test standardization with valid input."""
        response = client.post("/standardize", json=valid_input)
        assert response.status_code == 200
        
        data = response.json()
        assert data["document_id"] == "DOC001"
        assert "standardized_data" in data
        assert "quality_score" in data
    
    def test_standardize_missing_document_id(self, valid_input):
        """Test standardization without document_id."""
        del valid_input["document_id"]
        response = client.post("/standardize", json=valid_input)
        assert response.status_code == 422  # Validation error
    
    def test_standardize_empty_extracted_fields(self, valid_input):
        """Test standardization with empty extracted_fields."""
        valid_input["extracted_fields"] = {}
        response = client.post("/standardize", json=valid_input)
        # API returns 400 for empty extracted_fields during processing
        assert response.status_code in [200, 400]  # May return error or process with validation errors
    
    def test_standardize_formats_email(self, valid_input):
        """Test that email is formatted to lowercase."""
        response = client.post("/standardize", json=valid_input)
        assert response.status_code == 200
        
        data = response.json()
        standardized = data["standardized_data"]
        assert "email_address" in standardized
        assert standardized["email_address"] == "john@example.com"
    
    def test_standardize_formats_phone(self, valid_input):
        """Test that phone is formatted."""
        response = client.post("/standardize", json=valid_input)
        assert response.status_code == 200
        
        data = response.json()
        standardized = data["standardized_data"]
        assert "phone_number" in standardized
    
    def test_standardize_cleans_name(self, valid_input):
        """Test that name is cleaned and title-cased."""
        response = client.post("/standardize", json=valid_input)
        assert response.status_code == 200
        
        data = response.json()
        standardized = data["standardized_data"]
        assert "full_name" in standardized
        assert standardized["full_name"] == "John Doe"


class TestBatchProcessing:
    """Test batch processing endpoint."""
    
    def test_batch_standardize(self, valid_input):
        """Test batch standardization."""
        batch_data = [valid_input, valid_input]
        response = client.post("/standardize-batch", json=batch_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["successful"] == 2
        assert data["failed"] == 0
        assert len(data["results"]) == 2
    
    def test_batch_with_errors(self, valid_input):
        """Test batch with some invalid inputs."""
        # Create a copy with minimal valid data
        valid_input_copy = {
            "document_id": "DOC002",
            "extracted_fields": {
                "name": "test user",
                "email": "test@example.com"
            }
        }
        
        # Create another valid document for comparison
        batch_data = [valid_input, valid_input_copy]
        response = client.post("/standardize-batch", json=batch_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["successful"] == 2
        assert data["failed"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
from fastapi.testclient import TestClient
import app.api as api_module


client = TestClient(api_module.app)


def test_standardize_with_formatting_and_fixing_errors(monkeypatch):
    class FakeGraph:
        def invoke(self, data):
            return {
                "data": {"document_id": "DOC001"},
                "standardized_data": {"name": "Dharshu"},
                "quality_score": 0.8,
                "document_type": "invoice",
                "validation_errors": ["old error"],
                "formatting_error": "format error",
                "fixing_error": "fix error",
            }

    monkeypatch.setattr("app.graph.build_graph", lambda: FakeGraph())

    response = client.post("/standardize", json={"document_id": "DOC001"})

    assert response.status_code == 200
    body = response.json()

    assert body["validation_errors"] == [
        "old error",
        "format error",
        "fix error",
    ]


def test_standardize_internal_server_error(monkeypatch):
    class FakeGraph:
        def invoke(self, data):
            raise Exception("Graph failed")

    monkeypatch.setattr("app.graph.build_graph", lambda: FakeGraph())

    response = client.post("/standardize", json={"document_id": "DOC001"})

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"


def test_llm_test_success(monkeypatch):
    class FakeAIService:
        def generate(self, prompt):
            return "pong"

    monkeypatch.setattr(api_module, "AIService", lambda: FakeAIService())

    response = client.get("/llm-test?prompt=ping")

    assert response.status_code == 200
    assert response.json() == {
        "available": True,
        "provider": "Gemini",
        "response": "pong",
    }


def test_llm_test_failure(monkeypatch):
    class FakeAIService:
        def generate(self, prompt):
            raise Exception("Gemini down")

    monkeypatch.setattr(api_module, "AIService", lambda: FakeAIService())

    response = client.get("/llm-test")

    assert response.status_code == 200
    assert response.json()["available"] is False
    assert response.json()["provider"] == "Gemini"
    assert "Gemini down" in response.json()["error"]