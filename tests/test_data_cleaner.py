from app.utils.data_cleaner import DataCleaner


class TestDataCleaner:

    def test_clean_text(self):
        assert DataCleaner.clean_text("  hello   world  ") == "hello world"
        assert DataCleaner.clean_text(123) == 123

    def test_clean_email(self):
        assert DataCleaner.clean_email(" TEST@MAIL.COM ") == "test@mail.com"
        assert DataCleaner.clean_email("bad-email") == "bad-email"

    def test_clean_amount(self):
        assert DataCleaner.clean_amount("$1,234.56") == 1234.56
        assert DataCleaner.clean_amount("1.234,56") == 1234.56
        assert DataCleaner.clean_amount(100) == 100.0
        assert DataCleaner.clean_amount("abc") is None

    def test_clean_date(self):
        assert DataCleaner.clean_date("12/25/2024") == "2024-12-25"
        assert DataCleaner.clean_date("2024-01-15") == "2024-01-15"
        assert DataCleaner.clean_date("15 Jan 2024") == "2024-01-15"
        assert DataCleaner.clean_date("wrong-date") is None

    def test_clean_invoice_number(self):
        assert DataCleaner.clean_invoice_number("INV: 123") == "123"
        assert DataCleaner.clean_invoice_number("#INV-001") == "INV-001"

    def test_clean_symbols(self):
        assert DataCleaner.clean_symbols("Hello@#$ World!") == "Hello World"

    def test_clean_phone(self):
        assert DataCleaner.clean_phone("9876543210") == "9876543210"
        assert DataCleaner.clean_phone("+91 98765 43210") == "+919876543210"

    def test_clean_name(self):
        assert DataCleaner.clean_name("dHaRsHiNi kumar") == "Dharshini Kumar"

    def test_normalize_keys(self):
        data = {
            "FullName": "Dharshini",
            "phone-number": "123"
        }

        result = DataCleaner.normalize_keys(data)

        assert "full_name" in result
        assert "phone_number" in result

    def test_remove_null_values(self):
        data = {
            "a": 1,
            "b": None,
            "c": "",
            "d": "null"
        }

        result = DataCleaner.remove_null_values(data)

        assert result == {"a": 1}

    def test_clean_data(self):
        data = {
            "FullName": "  Dharshini  ",
            "details": {
                "city": "  Chennai "
            }
        }

        result = DataCleaner.clean_data(data)

        assert result["full_name"] == "Dharshini"
        assert result["details"]["city"] == "Chennai"

    def test_detect_data_types(self):
        data = {
            "name": "Dharshini",
            "age": 20,
            "marks": 90.5,
            "active": True,
            "items": [],
            "obj": {},
            "none": None
        }

        result = DataCleaner.detect_data_types(data)

        assert result["name"] == "string"
        assert result["age"] == "integer"
        assert result["marks"] == "float"
        assert result["active"] == "boolean"
        assert result["items"] == "array"
        assert result["obj"] == "object"
        assert result["none"] == "null"

    def test_calculate_completeness_score(self):
        data = {
            "a": 1,
            "b": None,
            "c": ""
        }

        assert DataCleaner.calculate_completeness_score(data) == 0.33
        assert DataCleaner.calculate_completeness_score({}) == 0.0