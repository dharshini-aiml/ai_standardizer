# Architecture

This document provides a brief overview of the project's architecture.

## Processing Pipeline

Input JSON -> Validation Agent -> Formatting Agent -> Fixer Agent -> Output JSON

- Validation Agent: verifies required fields and types
- Formatting Agent: normalizes keys, formats emails/phones/names
- Fixer Agent: cleans text, handles missing values, computes quality score

## Services

- `AIService` (app/services/ai_service.py): wrapper for Google Gemini LLM provider
- `DataService` (app/services/data_service.py): filesystem helpers for inputs/outputs

## Deployment

- `Dockerfile` provided for containerization
- `Makefile` contains common developer targets
