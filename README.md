# Data Standardization & Schema Mapping Agent

A professional-grade FastAPI application for normalizing, cleaning, and standardizing extracted data using LangGraph workflows, Pydantic schemas, and intelligent data processing.

## 📋 Overview

This API provides a complete pipeline for:
- **Input Validation**: Schema validation and data type checking
- **Formatting**: Field type detection and intelligent formatting
- **Data Cleaning**: Standardization, deduplication, and quality scoring
- **Batch Processing**: Handle multiple documents efficiently

## 🏗️ Architecture

```
Input (JSON)
    ↓
[Validation Agent] - Validates schema and data types
    ↓
[Formatting Agent] - Normalizes keys and detects field types
    ↓
[Fixer Agent] - Cleans, standardizes, and calculates quality
    ↓
Output (Standardized JSON)
```

## 📦 Project Structure

```
app/
├── __init__.py
├── api.py                 # FastAPI application & endpoints
├── config.py             # Configuration management
├── exceptions.py         # Custom exceptions
├── graph.py              # LangGraph workflow definition
├── agents/               # Processing agents
│   ├── __init__.py
│   ├── validator.py      # Input validation agent
│   ├── formatter.py      # Data formatting agent
│   └── fixer.py         # Data cleaning agent
├── models/               # Pydantic schemas
│   ├── __init__.py
│   └── schema.py        # Input/output schemas
└── utils/                # Utility modules
    ├── __init__.py
    ├── logger.py        # Logging configuration
    └── data_cleaner.py  # Data cleaning utilities
tests/
├── test_api.py          # API tests
requirements.txt         # Project dependencies
README.md               # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai_standardizer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Logging
LOG_LEVEL=INFO
LOG_DIR=logs

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-flash

# Processing
MAX_RETRIES=3
TIMEOUT_SECONDS=30
QUALITY_SCORE_THRESHOLD=0.7
```

## 📡 API Endpoints

### 1. Health Check
```bash
GET /health
```

### 2. Get Configuration
```bash
GET /config
```

### 3. Standardize Document
```bash
POST /standardize

Request:
{
  "document_id": "DOC001",
  "extracted_fields": {
    "full_name": "John Doe",
    "email_address": "john@example.com",
    "phone_number": "123-456-7890"
  },
  "source": "pdf"
}
```

### 4. Batch Standardization
```bash
POST /standardize-batch
```

## 🧪 Testing

```bash
pytest tests/ -v
```

## ▶️ Running the Application

### Development
```bash
uvicorn app.api:app --reload
```

### Production
```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000 --workers 4
```

Access API docs at http://localhost:8000/docs

## 🔄 Data Processing Pipeline

### Validation Agent
- Validates required fields
- Type checking
- Field value validation

### Formatting Agent
- Key normalization (snake_case)
- Field type detection (email, phone, name)
- Duplicate removal

### Fixer Agent
- Text cleaning and encoding fixes
- Field standardization
- Quality score calculation

## 📊 Data Cleaning Features

- **Email**: Lowercase normalization
- **Phone**: Format standardization (+1 (123) 456-7890)
- **Names**: Title case formatting
- **Keys**: Snake_case conversion

## 🛠️ Development

Code quality checks:
```bash
black app/ tests/        # Format
flake8 app/ tests/       # Lint
isort app/ tests/        # Import sorting
mypy app/                # Type checking
```

## 📝 Logging

Logs stored in:
- Console output (real-time)
- `logs/app.log` (rotating, 10MB max, 5 backups)

## 📚 Quick Examples

### Single Document
```python
import requests

response = requests.post(
    "http://localhost:8000/standardize",
    json={
        "document_id": "DOC001",
        "extracted_fields": {
            "name": "john doe",
            "email": "JOHN@EXAMPLE.COM"
        }
    }
)
print(response.json())
```

### Batch Processing
```python
response = requests.post(
    "http://localhost:8000/standardize-batch",
    json=[
        {"document_id": "DOC001", "extracted_fields": {...}},
        {"document_id": "DOC002", "extracted_fields": {...}}
    ]
)
```

## 📄 License

MIT License

---

**Version**: 1.0.0  
**Status**: Production Ready
