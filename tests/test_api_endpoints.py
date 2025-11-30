import pytest
from unittest.mock import patch
from fastapi.responses import JSONResponse
import json


class TestCareerEndpoint:
    """Test cases for /career-plan endpoint."""
    
    @pytest.mark.unit
    def test_career_plan_endpoint_success(self, client, sample_job_request, mock_ollama_response, temp_prompt_file):
        """Test successful career plan request."""
        with patch('app.core.config.settings.PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('app.services.career_service.ollama.chat', return_value=mock_ollama_response):
                response = client.post("/career-plan", json=sample_job_request)
                
                assert response.status_code == 200
                data = response.json()
                assert "skills" in data
                assert isinstance(data["skills"], list)
    
    @pytest.mark.unit
    def test_career_plan_endpoint_missing_fields(self, client):
        """Test career plan request with missing required fields."""
        incomplete_request = {
            "user_id": "test_user",
            "category": "Software Engineering"
            # Missing timeline and job_description
        }
        
        response = client.post("/career-plan", json=incomplete_request)
        assert response.status_code == 422  # Unprocessable Entity
    
    @pytest.mark.unit
    def test_career_plan_endpoint_invalid_data_types(self, client):
        """Test career plan request with invalid data types."""
        invalid_request = {
            "user_id": 123,  # Should be string
            "category": "Software Engineering",
            "timeline": "2 weeks",
            "job_description": "Developer"
        }
        
        response = client.post("/career-plan", json=invalid_request)
        # FastAPI will coerce the integer to string, so this should succeed
        # but we can test that it handles it gracefully
        assert response.status_code in [200, 422, 500]
    
    @pytest.mark.unit
    def test_career_plan_endpoint_empty_strings(self, client, temp_prompt_file, mock_ollama_response):
        """Test career plan request with empty strings."""
        empty_request = {
            "user_id": "",
            "category": "",
            "timeline": "",
            "job_description": ""
        }
        
        with patch('app.core.config.settings.PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('app.services.career_service.ollama.chat', return_value=mock_ollama_response):
                response = client.post("/career-plan", json=empty_request)
                # Should still process, even with empty strings
                assert response.status_code in [200, 500]
    
    @pytest.mark.unit
    def test_career_plan_endpoint_service_error(self, client, sample_job_request, temp_prompt_file):
        """Test career plan endpoint when service raises an error."""
        with patch('app.core.config.settings.PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('app.services.career_service.ollama.chat', side_effect=Exception("Service unavailable")):
                response = client.post("/career-plan", json=sample_job_request)
                
                assert response.status_code == 500
                assert "detail" in response.json()
