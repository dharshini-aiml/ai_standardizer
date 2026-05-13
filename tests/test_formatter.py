from app.agents.formatter import Formatter


def test_detect_and_format_field_email():
    key, value = Formatter.detect_and_format_field(
        "email_address",
        " TEST@MAIL.COM "
    )

    assert key == "email_address"
    assert value == "test@mail.com"


def test_detect_and_format_field_phone():
    key, value = Formatter.detect_and_format_field(
        "phone_number",
        "+91 98765 43210"
    )

    assert key == "phone_number"
    assert value == "+919876543210"


def test_detect_and_format_field_name():
    key, value = Formatter.detect_and_format_field(
        "full_name",
        "  dharshu kumar  "
    )

    assert key == "full_name"
    assert value == "Dharshu Kumar"


def test_detect_and_format_field_unknown():
    key, value = Formatter.detect_and_format_field(
        "company",
        "OpenAI"
    )

    assert key == "company"
    assert value == "OpenAI"


def test_format_extracted_fields():
    data = {
        "EMAIL": " TEST@MAIL.COM ",
        "PHONE_NUMBER": "+91 98765 43210",
        "FULL_NAME": "  dharshu kumar  ",
        "AGE": 21,
        "EMPTY": "",
        "NONE": None
    }

    result = Formatter.format_extracted_fields(data)

    assert result["email"] == "test@mail.com"
    assert result["phone_number"] == "+919876543210"
    assert result["full_name"] == "Dharshu Kumar"
    assert result["age"] == 21

    assert "empty" not in result
    assert "none" not in result


def test_normalize_field_names():
    data = {
        "Full Name": "Dharshu",
        "Phone Number": "9876543210"
    }

    result = Formatter.normalize_field_names(data)

    assert "full_name" in result
    assert "phone_number" in result


def test_remove_duplicates_keeps_longer_key():
    data = {
        "phone": "123",
        "phone_number": "9876543210"
    }

    result = Formatter.remove_duplicates(data)

    assert "phone" not in result
    assert "phone_number" in result


def test_remove_duplicates_keeps_original_when_shorter():
    data = {
        "email_address": "test@mail.com",
        "email": "short@mail.com"
    }

    result = Formatter.remove_duplicates(data)

    assert "email_address" in result
    assert "email" not in result


def test_format_json_success():
    state = {
        "is_valid": True,
        "data": {
            "extracted_fields": {
                "EMAIL": " TEST@MAIL.COM "
            }
        }
    }

    result = Formatter.format_json(state)

    assert "formatted_data" in result
    assert result["formatted_data"]["email"] == "test@mail.com"


def test_format_json_invalid_state():
    state = {
        "is_valid": False,
        "data": {}
    }

    result = Formatter.format_json(state)

    assert result == state