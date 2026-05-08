# ISO 27001 Compliance Manager
# AI Service

AI Service for ISO 27001 Compliance Manager built using Flask, Groq API, ChromaDB, and Sentence Transformers.

---

# Features

- AI-powered text description generation
- Structured report generation
- Document risk and insight analysis
- RAG (Retrieval Augmented Generation) pipeline
- SSE streaming support
- Batch processing endpoint
- Pytest unit testing

---

# Tech Stack

- Python 3.10
- Flask
- Groq API
- Sentence Transformers
- ChromaDB
- Pytest

---

# Project Structure

```bash
ai-service/
│
├── app.py
├── requirements.txt
├── README.md
├── test_client.py
├── batch_test.py
│
├── services/
│   └── groq_client.py
│
├── docs/
│   └── sample.txt
│
├── chroma_db/
│
└── tests/
    └── test_app.py
```

---

# Prerequisites

Before running the project, install:

- Python 3.10+
- pip
- Git

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository-url>
cd ai-service
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is unavailable:

```bash
pip install flask groq chromadb sentence-transformers pytest requests
```

---

# Environment Variables

Create a `.env` file or set environment variable manually.

## Windows CMD

```bash
set GROQ_API_KEY=your_api_key
```

## PowerShell

```powershell
$env:GROQ_API_KEY="your_api_key"
```

---

# Running the Application

```bash
python app.py
```

Server starts at:

```text
http://127.0.0.1:5000
```

---

# API Reference

---

# 1. Home Endpoint

## GET /

Check if API is running.

### Response

```json
{
  "message": "API is running!"
}
```

---

# 2. Describe Endpoint

## POST /describe

Generate AI response for input text.

### Request

```json
{
  "text": "What is AI?"
}
```

### Response

```json
{
  "status": "success",
  "response": "AI explanation...",
  "generated_at": "timestamp"
}
```

---

# 3. Generate Report Endpoint

## POST /generate-report

Generate structured report.

### Request

```json
{
  "text": "Cybersecurity"
}
```

### Response

```json
{
  "status": "success",
  "report": {
    "title": "Report Title",
    "executive_summary": "...",
    "overview": "...",
    "top_items": [],
    "recommendations": []
  },
  "generated_at": "timestamp"
}
```

---

# 4. Generate Report Streaming Endpoint

## GET /generate-report-stream

Streams AI-generated response using SSE.

### Example

```text
/generate-report-stream?text=AI
```

### Content Type

```text
text/event-stream
```

---

# 5. Analyse Document Endpoint

## POST /analyse-document

Analyze document for insights and risks.

### Request

```json
{
  "text": "Passwords stored in plain text"
}
```

### Response

```json
{
  "status": "success",
  "findings": [
    {
      "type": "risk",
      "description": "Passwords stored insecurely",
      "severity": "high"
    }
  ],
  "generated_at": "timestamp"
}
```

---

# 6. Batch Process Endpoint

## POST /batch-process

Process multiple items with delay.

### Request

```json
{
  "items": [
    "AI",
    "Cloud",
    "Security"
  ]
}
```

### Response

```json
{
  "status": "success",
  "results": [
    {
      "input": "AI",
      "processed_result": "Processed: AI"
    }
  ],
  "total_processed": 3
}
```

---

# RAG Pipeline

The project includes a Retrieval Augmented Generation (RAG) pipeline using:

- Sentence Transformers
- ChromaDB
- Document chunking
- Embedding storage

---

# Running Tests

Run all tests:

```bash
pytest
```

Expected output:

```text
10 passed
```

---

# Error Handling

The application handles:

- Missing JSON body
- Empty input
- Invalid routes
- AI service failures
- Invalid request formats

---

# Future Improvements

- Real-time token streaming from LLM
- Authentication and authorization
- Docker deployment
- Async processing
- Frontend integration

---

# Author

AI Developer 1[Anushree G M]
ISO 27001 Compliance Manager Project