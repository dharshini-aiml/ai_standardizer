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
├── __init__.py            # Package initialization
├── api.py                 # FastAPI application & endpoints
├── config.py              # Configuration and environment settings
├── exceptions.py          # Custom exception types
├── graph.py               # LangGraph pipeline orchestration
├── agents/                # Modular data processing agents
│   ├── __init__.py
│   ├── validator.py       # Input validation agent
│   ├── formatter.py       # Formatting/normalization agent
│   ├── fixer.py           # Data cleaning and standardization agent
│   └── type_detector.py   # Document type inference
├── models/                # Pydantic models and schemas
│   ├── __init__.py
│   └── schema.py          # Input/output schema definitions
└── utils/                 # Shared utilities
    ├── __init__.py
    ├── logger.py          # Logging configuration
    └── data_cleaner.py    # Reusable cleaning helpers
docs/
├── architecture.md        # Design and workflow documentation
data/
├── input/                 # Example input payloads
└── output/                # Example output results
test_results/
├── coverage_report.txt    # Generated coverage summary
tests/
├── test_api.py            # API contract tests
├── test_fixer_agent.py    # Fixer logic tests
├── test_formatter.py      # Formatter tests
├── test_validator.py      # Validator tests
├── test_type_detector.py  # Type detection tests
└── ...
requirements.txt           # Project dependencies
setup.py                   # Packaging metadata
README.md                  # Project documentation
```

## 🧩 New Files and Workflow Additions

This repository now includes documentation and test artifacts that support a complete delivery workflow:

- `docs/architecture.md` — design decisions, pipeline overview, and architecture notes
- `.env.example` — sample environment configuration for local development
- `.coveragerc` — coverage tool configuration
- `test_results/coverage_report.txt` — generated coverage summary for reviews and reporting
- `tests/` — expanded unit and API test coverage for core agents and endpoints

## 🧭 Processing Workflow

The standardization pipeline follows a clear, deterministic flow:

1. **Receive request**
   - Client submits a JSON payload to `/standardize`
2. **Validate input**
   - `Validator` checks required fields, types, and extracted values
3. **Format fields**
   - `Formatter` normalizes keys, trims text, and detects common field types
4. **Clean and standardize**
   - `Fixer` applies field-specific normalization, fixes encoding issues, and computes quality metrics
5. **Infer document type**
   - `TypeDetector` labels the document based on cleaned field content
6. **Return response**
   - API returns a single clean `standardized_data` object with metadata

This workflow is designed to keep the output predictable, easy to consume, and ready for downstream automation.

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

