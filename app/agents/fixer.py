"""Fixer agent for data cleaning and standardization."""
from typing import Dict, Any, Optional
import re
from app.utils.logger import logger
from app.utils.data_cleaner import DataCleaner
from app.exceptions import ProcessingError


class Fixer:
    """Clean, fix, and standardize data."""
    
    @staticmethod
    def fix_common_issues(value: Any) -> Any:
        """
        Fix common data issues.
        
        Args:
            value: Input value
            
        Returns:
            Fixed value
        """
        if not isinstance(value, str):
            return value
        
        # Convert 'null' string to actual None
        if value.lower() in ["null", "none", "n/a", "na", "undefined"]:
            return None
        
        # Fix multiple spaces
        value = " ".join(value.split())
        
        # Fix common encoding issues
        value = value.replace("\u2019", "'")  # Right single quote
        value = value.replace("\u2013", "-")  # En dash
        value = value.replace("\u2014", "—")  # Em dash
        
        return value
    
    @staticmethod
    def standardize_field_value(key: str, value: Any) -> Any:
        """
        Standardize individual field values.
        
        Args:
            key: Field name
            value: Field value
            
        Returns:
            Standardized value
        """
        key_lower = key.lower()
        
        # Apply field-specific standardization
        if any(x in key_lower for x in ["email", "mail"]):
            return DataCleaner.clean_email(value) if isinstance(value, str) else value
        
        elif any(x in key_lower for x in ["phone", "mobile", "telephone"]):
            return DataCleaner.clean_phone(value) if isinstance(value, str) else value
        
        elif any(x in key_lower for x in ["name", "full_name"]):
            return DataCleaner.clean_name(value) if isinstance(value, str) else value
        
        elif isinstance(value, str):
            return DataCleaner.clean_text(value)
        
        return value
    
    @staticmethod
    def handle_missing_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle and report missing data fields.
        
        Args:
            data: Input data
            
        Returns:
            Data with null values marked/handled
        """
        processed = {}
        missing_fields = []
        
        for key, value in data.items():
            if value is None or value == "":
                missing_fields.append(key)
                processed[key] = None
            else:
                processed[key] = value
        
        if missing_fields:
            logger.debug(f"Missing data in fields: {missing_fields}")
        
        return processed
    
    @staticmethod
    def validate_and_fix_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and fix data issues.
        
        Args:
            data: Input data
            
        Returns:
            Fixed data dictionary
        """
        fixed = {}
        
        for key, value in data.items():
            # Fix common issues first
            if isinstance(value, str):
                value = Fixer.fix_common_issues(value)
            
            # Apply field-specific standardization
            if value is not None:
                value = Fixer.standardize_field_value(key, value)
            
            fixed[key] = value
        
        return fixed
    
    @staticmethod
    def calculate_quality_score(
        original_data: Dict[str, Any],
        fixed_data: Dict[str, Any],
        validation_errors: Optional[list] = None
    ) -> float:
        """
        Calculate data quality score.
        
        Args:
            original_data: Original input data
            fixed_data: Fixed/cleaned data
            validation_errors: Any validation errors
            
        Returns:
            Quality score between 0 and 1
        """
        score = 1.0
        
        # Check for validation errors
        if validation_errors:
            score -= 0.1 * len(validation_errors)
        
        # Check completeness
        total_fields = len(fixed_data)
        if total_fields == 0:
            return 0.0
        
        non_null = len([v for v in fixed_data.values() if v is not None])
        completeness = non_null / total_fields
        score *= completeness
        
        # Check for suspicious values
        suspicious_count = 0
        for value in fixed_data.values():
            if isinstance(value, str):
                if len(value) == 0 or value in ["unknown", "n/a"]:
                    suspicious_count += 1
        
        if suspicious_count > 0:
            score -= (suspicious_count / total_fields) * 0.2
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, round(score, 2)))
    
    @staticmethod
    def fix_json(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main fixing and standardization function for the agent pipeline.
        
        Args:
            state: Current pipeline state
            
        Returns:
            Updated state with standardized data
        """
        try:
            data = state.get("data", {})
            formatted_data = state.get("formatted_data", {})
            validation_errors = state.get("validation_errors", [])
            
            if not state.get("is_valid", False):
                logger.warning("Skipping fixing: data not validated")
                return state
            
            # Apply comprehensive fixing
            fixed_data = Fixer.validate_and_fix_data(formatted_data)
            fixed_data = Fixer.handle_missing_data(fixed_data)
            
            # Calculate quality score
            quality_score = Fixer.calculate_quality_score(
                formatted_data,
                fixed_data,
                validation_errors
            )
            
            logger.info(
                f"Fixed data for {data.get('document_id')} - "
                f"Quality score: {quality_score}"
            )
            
            return {
                **state,
                "standardized_data": fixed_data,
                "quality_score": quality_score
            }
            
        except Exception as e:
            logger.error(f"Fixing failed: {str(e)}")
            return {
                **state,
                "fixing_error": str(e)
            }


def fix_json(state: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper function for pipeline compatibility."""
    return Fixer.fix_json(state)
