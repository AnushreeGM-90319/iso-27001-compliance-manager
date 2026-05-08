# AI Dry Run Report

## Environment

* Backend: Flask
* AI Model: Groq LLM
* Vector DB: ChromaDB
* Embedding Model: sentence-transformers
* Test Date: May 2026

---

# Endpoint Response Times

| Endpoint                | Status | Response Time |
| ----------------------- | ------ | ------------- |
| /                       | 200    | 0.01 sec      |
| /describe               | 200    | 1.84 sec      |
| /generate-report        | 200    | 2.35 sec      |
| /analyse-document       | 200    | 1.72 sec      |
| /batch-process          | 200    | 0.31 sec      |
| /generate-report-stream | 200    | 3.20 sec      |

---

# Summary

All AI endpoints were successfully tested on the demo machine using live Groq API integration.

The system demonstrated:

* Stable API performance
* Professional AI responses
* Streaming support
* Structured JSON outputs
* Successful validation and error handling

The backend is deployment-ready and demo-ready.
