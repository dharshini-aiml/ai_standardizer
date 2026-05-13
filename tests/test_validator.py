import pytest
from app.agents.validator import Validator, validate_json

class TestValidator:
    
    def test_validate_required_fields(self):
        valid_data = {"document_id": "DOC001", "extracted_fields": {"name": "Muniyappan"}}
        is_valid, errors = Validator.validate_required_fields(valid_data)
        assert is_valid is True
        
        invalid_data = {"document_id": "DOC001"}
        is_valid, errors = Validator.validate_required_fields(invalid_data)
        assert is_valid is False
        assert "Missing required field: extracted_fields" in errors

    def test_validate_data_types(self):
        bad_id = {"document_id": 123, "extracted_fields": {}}
        is_valid, errors = Validator.validate_data_types(bad_id)
        assert "document_id must be a string" in errors
        
        bad_fields = {"document_id": "DOC1", "extracted_fields": ["not_a_dict"]}
        is_valid, errors = Validator.validate_data_types(bad_fields)
        assert "extracted_fields must be a dictionary" in errors

    def test_validate_field_values(self):
        suspicious = {"extracted_fields": {"status": "null"}}
        is_valid, errors = Validator.validate_field_values(suspicious)
        assert is_valid is True 
        
        long_str = "A" * 10001
        too_long = {"extracted_fields": {"bio": long_str}}
        is_valid, errors = Validator.validate_field_values(too_long)
        assert is_valid is False
        assert "Field 'bio' exceeds maximum length" in errors

    def test_validator_pipeline_success(self):
        state = {
            "data": {"document_id": "DOC123", "extracted_fields": {"amount": "100"}}
        }
        result = Validator.validate_json(state)
        assert result["is_valid"] is True

    def test_validator_pipeline_failure(self):
        state = {"data": {}}
        result = Validator.validate_json(state)
        assert result["is_valid"] is False

    def test_validator_exception_handling(self):
        # FIX: Passing a dict with None data triggers the exception 
        # while keeping 'state' as a dictionary for unpacking.
        state = {"data": None} 
        result = Validator.validate_json(state)
        assert result["is_valid"] is False
        assert "Validation error" in result["validation_errors"][0]

    def test_wrapper_function(self):
        state = {"data": {"document_id": "X", "extracted_fields": {"Y": "Z"}}}
        assert validate_json(state)["is_valid"] is True