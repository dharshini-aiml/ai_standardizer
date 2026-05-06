"""Validator agent for input validation."""
from typing import Dict, Any, List
from app.utils.logger import logger
from app.exceptions import ValidationError


class Validator:
    """Validate input data against schema and business rules."""
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate required fields exist.
        
        Args:
            data: Input data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        required_fields = ["document_id", "extracted_fields"]
        errors = []
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not data[field]:
                errors.append(f"Required field '{field}' is empty")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_data_types(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate data types.
        
        Args:
            data: Input data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Validate document_id
        if "document_id" in data:
            if not isinstance(data["document_id"], str):
                errors.append("document_id must be a string")
            elif len(data["document_id"].strip()) == 0:
                errors.append("document_id cannot be empty")
        
        # Validate extracted_fields
        if "extracted_fields" in data:
            if not isinstance(data["extracted_fields"], dict):
                errors.append("extracted_fields must be a dictionary")
            elif len(data["extracted_fields"]) == 0:
                errors.append("extracted_fields cannot be empty")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_field_values(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate field values for common issues.
        
        Args:
            data: Input data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        extracted_fields = data.get("extracted_fields", {})
        
        for key, value in extracted_fields.items():
            # Check for suspicious values
            if value == "" or value == "null" or value == "undefined":
                logger.warning(f"Suspicious value for {key}: {value}")
            
            # Check for extremely long strings
            if isinstance(value, str) and len(value) > 10000:
                errors.append(f"Field '{key}' exceeds maximum length")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_json(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main validation function for the agent pipeline.
        
        Args:
            state: Current pipeline state
            
        Returns:
            Updated state with validation results
        """
        try:
            data = state.get("data", {})
            
            # Run all validations
            validations = [
                Validator.validate_required_fields(data),
                Validator.validate_data_types(data),
                Validator.validate_field_values(data),
            ]
            
            all_errors = []
            for is_valid, errors in validations:
                if not is_valid:
                    all_errors.extend(errors)
            
            if all_errors:
                logger.warning(f"Validation errors: {all_errors}")
                return {
                    **state,
                    "validation_errors": all_errors,
                    "is_valid": False
                }
            
            logger.info(f"Document {data.get('document_id')} validated successfully")
            return {
                **state,
                "is_valid": True,
                "validation_errors": None
            }
            
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            return {
                **state,
                "is_valid": False,
                "validation_errors": [f"Validation error: {str(e)}"]
            }


def validate_json(state: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper function for pipeline compatibility."""
    return Validator.validate_json(state)
