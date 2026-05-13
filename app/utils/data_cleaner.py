"""Data cleaning utilities using Pandas."""
import pandas as pd
import re
from typing import Dict, Any, Optional, List
from app.utils.logger import logger


class DataCleaner:
    """Utility class for data cleaning and normalization."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing extra whitespace and special characters.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            return text
            
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def clean_email(email: str) -> str:
        """
        Clean and validate email addresses.
        
        Args:
            email: Input email
            
        Returns:
            Cleaned email (lowercased)
        """
        if not isinstance(email, str):
            return email
            
        email = DataCleaner.clean_text(email).lower()
        
        # Basic email validation pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            return email
        
        logger.warning(f"Invalid email format: {email}")
        return email
    
    @staticmethod
    def clean_amount(amount: str) -> Optional[float]:
        """
        Clean and standardize monetary amounts.
        
        Args:
            amount: Input amount string
            
        Returns:
            Cleaned amount as float, or None if invalid
        """
        if not isinstance(amount, str):
            if isinstance(amount, (int, float)):
                return float(amount)
            return None
            
        # Remove currency symbols and unwanted characters
        amount = re.sub(r'[^\d.,\-]', '', amount)
        
        # Handle different decimal separators
        if ',' in amount and '.' in amount:
            # European format: 1.234,56
            if amount.rfind(',') > amount.rfind('.'):
                amount = amount.replace('.', '').replace(',', '.')
            else:
                # US format: 1,234.56
                amount = amount.replace(',', '')
        elif ',' in amount:
            # Could be decimal or thousand separator
            if amount.count(',') == 1 and len(amount.split(',')[1]) <= 2:
                amount = amount.replace(',', '.')
            else:
                amount = amount.replace(',', '')
        
        try:
            return float(amount)
        except ValueError:
            logger.warning(f"Could not parse amount: {amount}")
            return None
    
    @staticmethod
    def clean_date(date_str: str) -> Optional[str]:
        """
        Clean and standardize dates to ISO format.
        
        Args:
            date_str: Input date string
            
        Returns:
            ISO formatted date string (YYYY-MM-DD), or None if invalid
        """
        if not isinstance(date_str, str):
            return None
            
        date_str = DataCleaner.clean_text(date_str)
        
        # Common date patterns
        patterns = [
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', lambda m: f"{m.group(3)}-{m.group(1):0>2}-{m.group(2):0>2}"),
            (r'(\d{1,2})-(\d{1,2})-(\d{4})', lambda m: f"{m.group(3)}-{m.group(1):0>2}-{m.group(2):0>2}"),
            (r'(\d{4})/(\d{1,2})/(\d{1,2})', lambda m: f"{m.group(1)}-{m.group(2):0>2}-{m.group(3):0>2}"),
            (r'(\d{4})-(\d{1,2})-(\d{1,2})', lambda m: f"{m.group(1)}-{m.group(2):0>2}-{m.group(3):0>2}"),
            (r'(\d{1,2})\s+(\w{3})\s+(\d{4})', None),
        ]
        
        for pattern, formatter in patterns:
            match = re.search(pattern, date_str)
            if match:
                if formatter:
                    return formatter(match)

                day, month_name, year = match.groups()
                month_names = {
                    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                    'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                    'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
                }

                month = month_names.get(month_name.lower()[:3], '01')
                return f"{year}-{month}-{day:0>2}"
        
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    @staticmethod
    def clean_invoice_number(inv_num: str) -> str:
        """
        Clean invoice numbers by removing unwanted symbols.
        
        Args:
            inv_num: Input invoice number
            
        Returns:
            Cleaned invoice number
        """
        if not isinstance(inv_num, str):
            return str(inv_num) if inv_num else ""
            
        inv_num = re.sub(
            r'^(inv|invoice|no|#)\s*[:\-]?\s*',
            '',
            inv_num,
            flags=re.IGNORECASE
        )

        inv_num = re.sub(r'[^\w\-]', '', inv_num)
        
        return DataCleaner.clean_text(inv_num)
    
    @staticmethod
    def clean_symbols(text: str) -> str:
        """
        Remove unwanted symbols and normalize text.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            return text
            
        text = re.sub(r'[^\w\s\.\-\,\(\)\&\']', '', text)
        text = " ".join(text.split())
        
        return text.strip()
    
    @staticmethod
    def clean_phone(phone: str) -> str:
        """
        Clean and standardize phone numbers.

        Args:
            phone: Input phone number

        Returns:
            Cleaned phone number
        """
        if not isinstance(phone, str):
            return phone

        # Remove extra spaces
        phone = phone.strip()

        # Keep + if present at beginning
        if phone.startswith("+"):
            digits = re.sub(r"[^\d]", "", phone)
            return "+" + digits

        # Otherwise keep only digits
        digits = re.sub(r"[^\d]", "", phone)

        return digits
    
    @staticmethod
    def clean_name(name: str) -> str:
        """
        Clean and standardize names.
        
        Args:
            name: Input name
            
        Returns:
            Standardized name
        """
        if not isinstance(name, str):
            return name
            
        name = DataCleaner.clean_text(name)
        name = " ".join(word.capitalize() for word in name.split())
        
        return name
    
    @staticmethod
    def normalize_keys(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize dictionary keys to snake_case.
        
        Args:
            data: Input dictionary
            
        Returns:
            Dictionary with normalized keys
        """
        normalized = {}
        
        for key, value in data.items():
            normalized_key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            normalized_key = re.sub(r'[-\s]+', '_', normalized_key)
            normalized_key = re.sub(r'_+', '_', normalized_key).strip('_')
            
            normalized[normalized_key] = value
        
        return normalized
    
    @staticmethod
    def remove_null_values(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove null, None, and empty string values.
        
        Args:
            data: Input dictionary
            
        Returns:
            Dictionary without null values
        """
        return {
            k: v for k, v in data.items()
            if v is not None and v != "" and v != "null"
        }
    
    @staticmethod
    def clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply comprehensive cleaning to data.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Cleaned data dictionary
        """
        data = DataCleaner.normalize_keys(data)
        data = DataCleaner.remove_null_values(data)
        
        cleaned_data = {}

        for key, value in data.items():
            if isinstance(value, str):
                cleaned_data[key] = DataCleaner.clean_text(value)

            elif isinstance(value, dict):
                cleaned_data[key] = DataCleaner.clean_data(value)

            elif isinstance(value, list):
                cleaned_data[key] = [
                    DataCleaner.clean_data(item) if isinstance(item, dict)
                    else DataCleaner.clean_text(item) if isinstance(item, str)
                    else item
                    for item in value
                ]

            else:
                cleaned_data[key] = value
        
        return cleaned_data
    
    @staticmethod
    def detect_data_types(data: Dict[str, Any]) -> Dict[str, str]:
        """
        Detect and return inferred data types for fields.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Dictionary mapping field names to detected types
        """
        type_map = {}
        
        for key, value in data.items():
            if value is None:
                type_map[key] = "null"

            elif isinstance(value, bool):
                type_map[key] = "boolean"

            elif isinstance(value, int):
                type_map[key] = "integer"

            elif isinstance(value, float):
                type_map[key] = "float"

            elif isinstance(value, str):
                type_map[key] = "string"

            elif isinstance(value, dict):
                type_map[key] = "object"

            elif isinstance(value, list):
                type_map[key] = "array"

            else:
                type_map[key] = "unknown"
        
        return type_map
    
    @staticmethod
    def calculate_completeness_score(data: Dict[str, Any]) -> float:
        """
        Calculate data completeness score (0-1).
        
        Args:
            data: Input data dictionary
            
        Returns:
            Completeness score
        """
        if not data:
            return 0.0
        
        total_fields = len(data)

        non_null_fields = len([
            v for v in data.values()
            if v is not None and v != ""
        ])
        
        return round(non_null_fields / total_fields, 2)