"""Package-level schema exports for backward compatibility.

Re-export the Pydantic schemas from `app.models.schema` so code that imports
`models.schema` continues to work.
"""

from app.models.schema import (
	InputJSONSchema,
	OutputJSONSchema,
	ExtractedFieldsSchema,
	StandardizedDataSchema,
)

__all__ = [
	"InputJSONSchema",
	"OutputJSONSchema",
	"ExtractedFieldsSchema",
	"StandardizedDataSchema",
]
