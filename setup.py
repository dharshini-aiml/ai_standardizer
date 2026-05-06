"""Setup configuration for Data Standardization API."""
from setuptools import setup, find_packages

setup(
    name="ai-standardizer",
    version="1.0.0",
    description="Data Standardization and Schema Mapping Agent",
    author="Data Standardization Team",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "pydantic==2.5.0",
        "python-dotenv==1.0.0",
        "langgraph==0.0.17",
        "langchain==0.1.0",
        "openai==1.3.0",
        "cohere>=4.0.0",
        "google-generative-ai>=0.2.0",
        "pandas==2.1.3",
        "numpy==1.26.2",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-asyncio==0.21.1",
            "httpx==0.25.1",
            "black==23.12.0",
            "flake8==6.1.0",
            "isort==5.13.2",
            "mypy==1.7.1",
        ],
    },
)
