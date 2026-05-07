"""FastAPI application for data standardization service."""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any

from app.config import settings
from app.utils.logger import logger
from app.services.ai_service import AIService


# ✅ FIRST app define பண்ணணும்
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Data Standardization and Schema Mapping Agent API"
)

# ✅ Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Health
@app.get("/health")
def health_check() -> dict:
    return {
        "status": "healthy",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION
    }


# ✅ Config
@app.get("/config")
def get_config() -> dict:
    return settings.get_config()


# ✅ Standardize
@app.post("/standardize", status_code=status.HTTP_200_OK)
def standardize(input_data: Dict[str, Any]) -> dict:
    try:
        # Use the LangGraph pipeline
        from app.graph import build_graph

        graph = build_graph()
        result = graph.invoke({"data": input_data})

        # ✅ Extract results safely
        document_data = result.get("data", {})
        document_id = document_data.get("document_id")

        # ✅ Return proper validation error
        if not document_id:
            raise HTTPException(
                status_code=422,
                detail="Missing required field: document_id"
            )

        standardized_data = result.get("standardized_data", {})
        quality_score = result.get("quality_score", 0.0)
        document_type = result.get("document_type", "unknown")

        # ✅ Collect validation errors
        validation_errors = result.get("validation_errors", [])

        if result.get("formatting_error"):
            validation_errors.append(result["formatting_error"])

        if result.get("fixing_error"):
            validation_errors.append(result["fixing_error"])

        return {
            "document_id": document_id,
            "document_type": document_type,
            "standardized_data": standardized_data,
            "quality_score": quality_score,
            "validation_errors": validation_errors if validation_errors else None
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


# ✅ Batch processing
@app.post("/standardize-batch", status_code=status.HTTP_200_OK)
def standardize_batch(inputs: List[Dict[str, Any]]) -> dict:
    results = []
    errors = []

    for index, item in enumerate(inputs):
        try:
            result = standardize(item)
            results.append(result)

        except Exception as e:
            errors.append({
                "index": index,
                "document_id": item.get("document_id"),
                "error": str(e)
            })

    return {
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }


# ✅ Gemini / LLM test
@app.get("/llm-test")
def llm_test(prompt: Optional[str] = None) -> dict:
    ai = AIService()
    test_prompt = prompt or "Respond with 'pong'"

    try:
        resp = ai.generate(test_prompt)

        return {
            "available": True,
            "provider": "Gemini",
            "response": resp
        }

    except Exception as e:
        return {
            "available": False,
            "provider": "Gemini",
            "error": str(e)
        }


# ✅ Global exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# ✅ Run server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )