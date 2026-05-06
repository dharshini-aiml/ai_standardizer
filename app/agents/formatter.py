"""Formatter agent for data formatting and normalization."""
from typing import Dict, Any, List
from app.utils.logger import logger
from app.utils.data_cleaner import DataCleaner
from app.exceptions import FormattingError


class Formatter:
    """Format and normalize extracted data."""
    
    # Field type mappings for known patterns
    COMMON_FIELD_PATTERNS = {
        "email": ["email", "email_address", "email_addr", "mail", "contact_email"],
        "phone": ["phone", "phone_number", "mobile", "telephone", "contact_number"],
        "name": ["name", "full_name", "person_name", "contact_name"],
        "address": ["address", "street_address", "location", "residence"],
        "date": ["date", "created_date", "birth_date", "dob", "date_of_birth"],
    }
    
    @staticmethod
    def detect_and_format_field(key: str, value: str) -> tuple[str, Any]:
        """
        Detect field type and apply appropriate formatting.
        
        Args:
            key: Field key/name
            value: Field value
            
        Returns:
            Tuple of (formatted_key, formatted_value)
        """
        key_lower = key.lower()
        
        # Check against common patterns
        for field_type, patterns in Formatter.COMMON_FIELD_PATTERNS.items():
            if any(pattern in key_lower for pattern in patterns):
                if field_type == "email":
                    return key_lower, DataCleaner.clean_email(value)
                elif field_type == "phone":
                    return key_lower, DataCleaner.clean_phone(value)
                elif field_type == "name":
                    return key_lower, DataCleaner.clean_name(value)
        
        # Default formatting
        return key_lower, value
    
    @staticmethod
    def format_extracted_fields(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format extracted fields with intelligent field type detection.
        
        Args:
            extracted_fields: Raw extracted fields
            
        Returns:
            Formatted fields dictionary
        """
        formatted = {}
        
        for key, value in extracted_fields.items():
            if value is None or value == "":
                continue
            
            # Skip non-string values for now
            if not isinstance(value, str):
                formatted_key, formatted_value = key.lower(), value
            else:
                formatted_key, formatted_value = Formatter.detect_and_format_field(key, value)
            
            formatted[formatted_key] = formatted_value
        
        return formatted
    
    @staticmethod
    def normalize_field_names(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize field names to consistent format.
        
        Args:
            data: Input data
            
        Returns:
            Data with normalized field names
        """
        return DataCleaner.normalize_keys(data)
    
    @staticmethod
    def remove_duplicates(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove duplicate or near-duplicate fields.
        
        Args:
            data: Input data
            
        Returns:
            Data with duplicates removed
        """
        # Simple approach: if we have similar keys, keep the cleanest one
        seen_prefixes = {}
        result = {}
        
        for key in sorted(data.keys()):
            prefix = key.split("_")[0]
            
            if prefix not in seen_prefixes:
                seen_prefixes[prefix] = key
                result[key] = data[key]
            else:
                # If we find a duplicate, keep the longer/more complete key
                existing_key = seen_prefixes[prefix]
                if len(key) > len(existing_key):
                    del result[existing_key]
                    result[key] = data[key]
                    seen_prefixes[prefix] = key
        
        return result
    
    @staticmethod
    def format_json(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main formatting function for the agent pipeline.
        
        Args:
            state: Current pipeline state
            
        Returns:
            Updated state with formatted data
        """
        try:
            data = state.get("data", {})
            
            if not state.get("is_valid", False):
                logger.warning("Skipping formatting: data not validated")
                return state
            
            extracted_fields = data.get("extracted_fields", {})
            
            # Apply formatting steps
            formatted_fields = Formatter.format_extracted_fields(extracted_fields)
            formatted_fields = Formatter.normalize_field_names(formatted_fields)
            formatted_fields = Formatter.remove_duplicates(formatted_fields)
            
            logger.info(f"Formatted {len(formatted_fields)} fields")
            
            return {
                **state,
                "formatted_data": formatted_fields
            }
            
        except Exception as e:
            logger.error(f"Formatting failed: {str(e)}")
            return {
                **state,
                "formatting_error": str(e)
            }


def format_json(state: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper function for pipeline compatibility."""
    return Formatter.format_json(state)
