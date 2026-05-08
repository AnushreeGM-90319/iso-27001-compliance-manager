import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch
from app import app


# -----------------------------------
# SETUP TEST CLIENT
# -----------------------------------
@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


# -----------------------------------
# 1. TEST HOME ROUTE
# -----------------------------------
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


# -----------------------------------
# 2. TEST /describe SUCCESS
# -----------------------------------
@patch('app.get_groq_response')
def test_describe_success(mock_groq, client):
    mock_groq.return_value = "AI response"

    response = client.post('/describe', json={
        "text": "AI"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "generated_at" in data


# -----------------------------------
# 3. TEST /describe MISSING TEXT
# -----------------------------------
def test_describe_missing_text(client):
    response = client.post('/describe', json={})

    assert response.status_code == 400


# -----------------------------------
# 4. TEST /describe EMPTY TEXT
# -----------------------------------
def test_describe_empty_text(client):
    response = client.post('/describe', json={
        "text": ""
    })

    assert response.status_code == 400


# -----------------------------------
# 5. TEST /generate-report SUCCESS
# -----------------------------------
@patch('app.get_groq_response')
def test_generate_report_success(mock_groq, client):
    mock_groq.return_value = '''
    {
      "title": "AI Report",
      "executive_summary": "summary",
      "overview": "overview",
      "top_items": [],
      "recommendations": []
    }
    '''

    response = client.post('/generate-report', json={
        "text": "AI"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"


# -----------------------------------
# 6. TEST /generate-report NO JSON
# -----------------------------------
def test_generate_report_no_json(client):
    response = client.post('/generate-report')

    assert response.status_code == 400


# -----------------------------------
# 7. TEST /analyse-document SUCCESS
# -----------------------------------
@patch('app.get_groq_response')
def test_analyse_document_success(mock_groq, client):
    mock_groq.return_value = '''
    {
      "findings": [
        {
          "type": "risk",
          "description": "Password issue",
          "severity": "high"
        }
      ]
    }
    '''

    response = client.post('/analyse-document', json={
        "text": "Passwords stored in plain text"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert len(data["findings"]) > 0


# -----------------------------------
# 8. TEST /analyse-document EMPTY
# -----------------------------------
def test_analyse_document_empty(client):
    response = client.post('/analyse-document', json={
        "text": ""
    })

    assert response.status_code == 400


# -----------------------------------
# 9. TEST INVALID ROUTE
# -----------------------------------
def test_invalid_route(client):
    response = client.get('/invalid')

    assert response.status_code == 404


# -----------------------------------
# 10. TEST GROQ FAILURE
# -----------------------------------
@patch('app.get_groq_response')
def test_groq_failure(mock_groq, client):
    mock_groq.side_effect = Exception("Groq error")

    response = client.post('/describe', json={
        "text": "AI"
    })

    assert response.status_code == 500