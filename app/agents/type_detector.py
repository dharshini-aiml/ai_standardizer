"""Type detector agent for document type identification."""
from typing import Dict, Any
from app.utils.logger import logger


class TypeDetector:
    """Detect document type based on extracted fields."""

    INVOICE_INDICATORS = {
        "sales_invoice": [
            "invoice_number",
            "invoice_no",
            "customer",
            "customer_name",
            "client_name",
            "total_amount",
            "invoice_date",
            "gst_number",
            "line_items",
            "items",
        ],
        "purchase_invoice": [
            "invoice_number",
            "invoice_no",
            "vendor",
            "vendor_name",
            "supplier",
            "supplier_name",
            "total_amount",
            "invoice_date",
        ],
        "receipt": [
            "receipt_number",
            "receipt_no",
            "amount_paid",
            "transaction_id",
            "payment_date",
        ],
        "bill": [
            "bill_number",
            "bill_no",
            "due_date",
            "amount_due",
            "total_amount",
        ],
    }

    @staticmethod
    def detect_document_type(extracted_fields: Dict[str, Any]) -> str:
        """Detect the document type from extracted field names."""

        if not extracted_fields:
            return "unknown"

        field_keys = {key.lower() for key in extracted_fields.keys()}

        best_match = None
        best_score = 0

        for doc_type, indicators in TypeDetector.INVOICE_INDICATORS.items():
            matches = sum(
                1 for indicator in indicators
                if indicator in field_keys
            )

            if matches > best_score:
                best_score = matches
                best_match = doc_type

        if best_match and best_score >= 2:
            logger.info(f"Detected document type: {best_match}")
            return best_match

        if any(field in field_keys for field in ["invoice_number", "invoice_no"]):
            return "sales_invoice"

        if any(field in field_keys for field in ["receipt_number", "receipt_no"]):
            return "receipt"

        if any(field in field_keys for field in ["bill_number", "bill_no"]):
            return "bill"

        if any(field in field_keys for field in ["total", "amount", "total_amount", "price", "cost", "sum"]):
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

            matches = sum(
                1 for indicator in indicators
                if indicator in field_keys
            )

            return min(matches / len(indicators), 1.0)

        return 0.5