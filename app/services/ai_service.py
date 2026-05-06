from typing import Optional
from app.config import settings
from app.utils.logger import logger


class AIService:
    """Gemini-only AI Service"""

    def __init__(self):
        self._gemini = None

    def _ensure_gemini(self):
        if self._gemini:
            return
        try:
            import google.generativeai as genai
        except Exception as e:
            raise RuntimeError(
                "Google Generative AI not installed (pip install google-generativeai)"
            ) from e

        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY not set")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self._gemini = genai

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> str:
        """Generate response using Gemini"""

        self._ensure_gemini()

        try:
            genai = self._gemini
            model_name = model or settings.GEMINI_MODEL

            model_instance = genai.GenerativeModel(model_name)
            response = model_instance.generate_content(prompt)

            return response.text or ""

        except Exception as e:
            logger.error("Gemini generation failed: %s", e)
            raise


__all__ = ["AIService"]