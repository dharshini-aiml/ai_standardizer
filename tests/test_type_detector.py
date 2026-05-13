from app.agents.type_detector import TypeDetector


def test_detect_document_type_unknown():
    result = TypeDetector.detect_document_type({})

    assert result == "unknown"


def test_detect_sales_invoice():
    data = {
        "invoice_number": "INV001",
        "customer": "Dharshu",
        "total_amount": "5000"
    }

    result = TypeDetector.detect_document_type(data)

    assert result == "sales_invoice"


def test_detect_purchase_invoice():
    data = {
        "invoice_number": "INV002",
        "vendor": "ABC Traders",
        "supplier": "XYZ Supplier"
    }

    result = TypeDetector.detect_document_type(data)

    assert result == "purchase_invoice"


def test_detect_receipt():
    data = {
        "receipt_number": "RC001",
        "amount_paid": "1000"
    }

    result = TypeDetector.detect_document_type(data)

    assert result == "receipt"


def test_detect_bill():
    data = {
        "bill_number": "B001",
        "amount_due": "2500"
    }

    result = TypeDetector.detect_document_type(data)

    assert result == "bill"


def test_detect_invoice_fallback():
    data = {
        "invoice_no": "INV123"
    }

    result = TypeDetector.detect_document_type(data)

    assert result == "sales_invoice"


def test_detect_financial_document():
    data = {
        "amount": "1000"
    }

    result = TypeDetector.detect_document_type(data)

    assert result == "financial_document"


def test_detect_general_document():
    data = {
        "name": "test"
    }

    result = TypeDetector.detect_document_type(data)

    assert result == "general"


def test_get_type_confidence_unknown():
    result = TypeDetector.get_type_confidence({}, "unknown")

    assert result == 0.0


def test_get_type_confidence_sales_invoice():
    data = {
        "invoice_number": "INV001",
        "customer": "Dharshu",
        "total_amount": "5000",
        "line_items": []
    }

    result = TypeDetector.get_type_confidence(data, "sales_invoice")

    assert result == 0.4


def test_get_type_confidence_partial_match():
    data = {
        "invoice_number": "INV001",
        "customer": "Dharshu"
    }

    result = TypeDetector.get_type_confidence(data, "sales_invoice")

    assert result == 0.2


def test_get_type_confidence_default():
    data = {
        "name": "test"
    }

    result = TypeDetector.get_type_confidence(data, "general")

    assert result == 0.5