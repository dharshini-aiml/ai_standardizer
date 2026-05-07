"""Type detector agent for document type identification."""
from typing import Dict, Any
from app.utils.logger import logger


class TypeDetector:
    """Detect document type based on extracted fields."""

    INVOICE_INDICATORS = {
        "sales_invoice": ["invoice_number", "customer", "total_amount", "line_items"],
        "purchase_invoice": ["invoice_number", "vendor", "supplier", "total_amount"],
        "receipt": ["receipt_number", "amount_paid", "transaction_id"],
        "bill": ["bill_number", "due_date", "amount_due"],
    }

    @staticmethod
    def detect_document_type(extracted_fields: Dict[str, Any]) -> str:
        """Detect the document type from extracted field names."""
        if not extracted_fields:
            return "unknown"

        field_keys = {key.lower() for key in extracted_fields.keys()}

        for doc_type, indicators in TypeDetector.INVOICE_INDICATORS.items():
            if any(indicator in field_keys for indicator in indicators):
                logger.info(f"Detected document type: {doc_type}")
                return doc_type

        if "invoice_number" in field_keys or "invoice_no" in field_keys:
            return "invoice"

        if any(field in field_keys for field in ["total", "amount", "price", "cost", "sum"]):
            return "financial_document"

        logger.info("Document type not clearly identified, defaulting to 'general'")
        return "general"

    @staticmethod
    def get_type_confidence(extracted_fields: Dict[str, Any], doc_type: str) -> float:
        """Return a confidence score for the detected document type."""
        if doc_type == "unknown":
            return 0.0

        if doc_type in TypeDetector.INVOICE_INDICATORS:
            indicators = TypeDetector.INVOICE_INDICATORS[doc_type]
            field_keys = {key.lower() for key in extracted_fields.keys()}
            matches = sum(1 for indicator in indicators if indicator in field_keys)
            return min(matches / len(indicators), 1.0)

        return 0.5
