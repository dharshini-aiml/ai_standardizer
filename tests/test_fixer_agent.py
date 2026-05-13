import pytest
from unittest.mock import MagicMock, patch
from app.agents.fixer import Fixer, fix_json

class TestFixer:
    
    # 1. Testing fix_common_issues
    @pytest.mark.parametrize("input_val, expected", [
        (123, 123),  # Non-string returns as is
        ("NULL", None),  # Null string conversion
        ("  too   many   spaces  ", "too many spaces"),  # Space fixing
        ("\u2019test\u2013case", "'test-case"),  # Encoding fixes
        ("undefined", None), # Another null string
    ])
    def test_fix_common_issues(self, input_val, expected):
        assert Fixer.fix_common_issues(input_val) == expected

    # 2. Testing standardize_field_value (Hitting all if-elif branches)
    @patch("app.agents.fixer.DataCleaner")
    def test_standardize_field_value_branches(self, mock_cleaner):
        # Mocking return values
        mock_cleaner.clean_email.return_value = "clean@mail.com"
        mock_cleaner.clean_phone.return_value = "12345"
        mock_cleaner.clean_name.return_value = "Dharshini"
        mock_cleaner.clean_amount.return_value = 100.0
        mock_cleaner.clean_date.return_value = "2024-01-01"
        mock_cleaner.clean_invoice_number.return_value = "INV-001"
        mock_cleaner.clean_symbols.return_value = "CleanSymbol"

        # Check each branch
        assert Fixer.standardize_field_value("user_email", "raw@mail.com") == "clean@mail.com"
        assert Fixer.standardize_field_value("mobile_no", "raw-phone") == "12345"
        assert Fixer.standardize_field_value("full_name", "dharshini") == "Dharshini"
        assert Fixer.standardize_field_value("total_amount", "100") == 100.0
        assert Fixer.standardize_field_value("due_date", "01/01") == "2024-01-01"
        assert Fixer.standardize_field_value("invoice_no", "inv1") == "INV-001"
        assert Fixer.standardize_field_value("random_key", "data!") == "CleanSymbol"
        assert Fixer.standardize_field_value("random_key", 500) == 500 # Non-string default

    # 3. Testing handle_missing_data
    def test_handle_missing_data(self):
        data = {"name": "Dharshini", "age": "", "city": None}
        result = Fixer.handle_missing_data(data)
        assert result["age"] is None
        assert result["city"] is None
        assert result["name"] == "Dharshini"

    # 4. Testing calculate_quality_score (All scenarios)
    def test_calculate_quality_score(self):
        # Scenario: Perfect data
        score = Fixer.calculate_quality_score({"a": 1}, {"a": 1})
        assert score == 1.0

        # Scenario: Empty data (Branch coverage for total_fields == 0)
        assert Fixer.calculate_quality_score({}, {}) == 0.0

        # Scenario: Validation errors & Missing values
        score = Fixer.calculate_quality_score(
            {"a": 1, "b": 2}, 
            {"a": 1, "b": None}, 
            validation_errors=["Error 1"]
        )
        # score = 1.0 - 0.1 (error) = 0.9. Then * 0.5 (completeness) = 0.45
        assert score == 0.45

        # Scenario: Suspicious values ("unknown", "n/a")
        score = Fixer.calculate_quality_score({"a": "unknown"}, {"a": "unknown"})
        # 1.0 (completeness) - (1/1 * 0.2) = 0.8
        assert score == 0.8

    # 5. Testing fix_json (The main pipeline function)
    def test_fix_json_success(self):
        state = {
            "data": {"document_id": "123"},
            "formatted_data": {"full_name": "  dharshini  ", "email": "test@mail.com"},
            "is_valid": True,
            "validation_errors": []
        }
        updated_state = fix_json(state)
        assert "standardized_data" in updated_state
        assert updated_state["quality_score"] > 0
        assert updated_state["standardized_data"]["full_name"] is not None

    def test_fix_json_not_valid(self):
        state = {"is_valid": False}
        result = fix_json(state)
        assert result == state # Returns as is

    def test_fix_json_exception(self):
        # Passing None to trigger an exception in .get() or processing
        result = fix_json(None) # This will trigger the except block
        assert "fixing_error" in result