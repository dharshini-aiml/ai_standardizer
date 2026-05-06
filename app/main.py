"""Application entrypoint for running the Data Standardization API."""

def main():
	"""
	Start the FastAPI application using Uvicorn.
	This function is suitable for simple local runs or container entrypoints.
	"""
	try:
		import uvicorn
	except Exception as e:
		raise RuntimeError("uvicorn is required to run the application") from e

	from app.config import settings

	uvicorn.run("app.api:app", host="0.0.0.0", port=8000, log_level=settings.LOG_LEVEL.lower())


if __name__ == "__main__":
	main()
