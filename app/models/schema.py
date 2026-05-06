"""Pydantic schemas for data standardization API."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional, List
from datetime import datetime


class ExtractedFieldsSchema(BaseModel):
    """Schema for extracted fields from document."""
    
    model_config = ConfigDict(extra="allow")


class InputJSONSchema(BaseModel):
    """Input schema for data standardization."""

    model_config = ConfigDict(extra="allow")

    document_id: str = Field(..., description="Unique document identifier")
    extracted_fields: Dict[str, Any] = Field(..., description="Raw extracted fields")
    source: Optional[str] = Field(None, description="Document source/type")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# 🔥 UPDATED OUTPUT SCHEMA (THIS FIXES 422)
class OutputJSONSchema(BaseModel):
    """Output schema for standardized AI response."""

    model_config = ConfigDict(extra="allow")

    document_id: str = Field(..., description="Unique document identifier")

    document_type: Optional[str] = Field(
        None,
        description="Type of document (invoice, receipt, etc.)"
    )

    extracted_fields: Dict[str, Any] = Field(
        ...,
        description="AI extracted structured fields"
    )

    missing_fields: Optional[List[str]] = Field(
        default_factory=list,
        description="Fields not found during extraction"
    )

    agent_reasoning: Optional[str] = Field(
        None,
        description="AI reasoning behind extraction"
    )

    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="AI confidence score (0 to 1)"
    )

    processing_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of processing"
    )

