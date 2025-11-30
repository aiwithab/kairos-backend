import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import tempfile
import os


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_job_request():
    """Sample job request data for testing."""
    return {
        "user_id": "test_user_123",
        "category": "Software Engineering",
        "timeline": "2 weeks",
        "job_description": "Backend Developer with Python and FastAPI"
    }


@pytest.fixture
def mock_ollama_response():
    """Mock response from Ollama."""
    return {
        "message": {
            "content": '''```json
{
  "skills": [
    {
      "skill_name": "Python",
      "total_days": 10,
      "topics": [
        {
          "topic_name": "FastAPI",
          "study_material": "https://fastapi.tiangolo.com/",
          "timeline": "3 days",
          "priority": "High",
          "bonus": false
        }
      ]
    }
  ]
}
```'''
        }
    }


@pytest.fixture
def temp_prompt_file():
    """Create a temporary prompt template file."""
    content = """You are an AI Career Coach.
Input: Job Category: {category}, Job Description: {job_description} with Timeline: {timeline}

Task:
1. Extract the main skills required.
2. For each topic, list priority (High/Medium/Low).

Output JSON format:
{
  "skills": [
    {
      "skill_name": "string",
      "total_days": "int",
      "topics": [
        {"topic_name": "string", "study_material": "url", "timeline":"1 week","priority": "High/Medium/Low","bonus": "bool"}
      ]
    }
  ]
}"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)
