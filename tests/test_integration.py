import pytest
from unittest.mock import patch
import json


class TestIntegration:
    """Integration tests for the complete application flow."""
    
    @pytest.mark.integration
    def test_end_to_end_career_plan_generation(self, client, sample_job_request, mock_ollama_response, temp_prompt_file):
        """Test complete flow from API request to response."""
        with patch('app.core.config.settings.PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('app.services.career_service.ollama.chat', return_value=mock_ollama_response):
                # Make request
                response = client.post("/career-plan", json=sample_job_request)
                
                # Verify response
                assert response.status_code == 200
                data = response.json()
                
                # Verify structure
                assert "skills" in data
                assert isinstance(data["skills"], list)
                assert len(data["skills"]) > 0
                
                # Verify skill structure
                skill = data["skills"][0]
                assert "skill_name" in skill
                assert "total_days" in skill
                assert "topics" in skill
                
                # Verify topic structure
                assert len(skill["topics"]) > 0
                topic = skill["topics"][0]
                assert "topic_name" in topic
                assert "study_material" in topic
                assert "timeline" in topic
                assert "priority" in topic
                assert "bonus" in topic
    
    @pytest.mark.integration
    def test_api_docs_accessible(self, client):
        """Test that API documentation is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    @pytest.mark.integration
    def test_openapi_schema_accessible(self, client):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema
        assert "/career-plan" in schema["paths"]
    
    @pytest.mark.integration
    def test_multiple_requests_handling(self, client, mock_ollama_response, temp_prompt_file):
        """Test that the API can handle multiple sequential requests."""
        requests_data = [
            {
                "user_id": f"user_{i}",
                "category": "Software Engineering",
                "timeline": "1 week",
                "job_description": f"Developer {i}"
            }
            for i in range(3)
        ]
        
        with patch('app.core.config.settings.PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('app.services.career_service.ollama.chat', return_value=mock_ollama_response):
                for request_data in requests_data:
                    response = client.post("/career-plan", json=request_data)
                    assert response.status_code == 200
                    assert "skills" in response.json()
