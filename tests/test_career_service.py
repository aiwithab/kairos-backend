import pytest
from unittest.mock import patch, mock_open, MagicMock
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import json

from app.services.career_service import get_prompt, generate_career_plan_logic
from app.core.config import settings


class TestGetPrompt:
    """Test cases for get_prompt function."""
    
    @pytest.mark.unit
    def test_get_prompt_success(self, temp_prompt_file):
        """Test successful prompt generation."""
        with patch.object(settings, 'PROMPT_TEMPLATE_PATH', temp_prompt_file):
            result = get_prompt("Software Engineering", "Python Developer", "2 weeks")
            
            assert "Software Engineering" in result
            assert "Python Developer" in result
            assert "2 weeks" in result
            assert "{category}" not in result
            assert "{job_description}" not in result
            assert "{timeline}" not in result
    
    @pytest.mark.unit
    def test_get_prompt_file_not_found(self):
        """Test prompt generation when template file is missing."""
        with patch.object(settings, 'PROMPT_TEMPLATE_PATH', 'nonexistent_file.txt'):
            with pytest.raises(HTTPException) as exc_info:
                get_prompt("Category", "Description", "Timeline")
            
            assert exc_info.value.status_code == 500
            assert "Prompt template not found" in exc_info.value.detail
    
    @pytest.mark.unit
    def test_get_prompt_read_error(self, temp_prompt_file):
        """Test prompt generation when file read fails."""
        with patch.object(settings, 'PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('builtins.open', side_effect=PermissionError("Access denied")):
                with pytest.raises(HTTPException) as exc_info:
                    get_prompt("Category", "Description", "Timeline")
                
                assert exc_info.value.status_code == 500


class TestGenerateCareerPlanLogic:
    """Test cases for generate_career_plan_logic function."""
    
    @pytest.mark.unit
    def test_generate_career_plan_success(self, temp_prompt_file, mock_ollama_response):
        """Test successful career plan generation."""
        with patch.object(settings, 'PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('app.services.career_service.ollama.chat', return_value=mock_ollama_response):
                result = generate_career_plan_logic("Software Engineering", "Python Developer", "2 weeks")
                
                assert isinstance(result, JSONResponse)
                # Parse the response body
                response_data = json.loads(result.body.decode())
                assert "skills" in response_data
                assert len(response_data["skills"]) > 0
                assert response_data["skills"][0]["skill_name"] == "Python"
    
    @pytest.mark.unit
    def test_generate_career_plan_json_decode_error(self, temp_prompt_file):
        """Test career plan generation with invalid JSON response."""
        invalid_response = {
            "message": {
                "content": "This is not valid JSON"
            }
        }
        
        with patch.object(settings, 'PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('app.services.career_service.ollama.chat', return_value=invalid_response):
                with pytest.raises(HTTPException) as exc_info:
                    generate_career_plan_logic("Category", "Description", "Timeline")
                
                assert exc_info.value.status_code == 500
                assert "Failed to parse JSON" in exc_info.value.detail
    
    @pytest.mark.unit
    def test_generate_career_plan_ollama_error(self, temp_prompt_file):
        """Test career plan generation when Ollama fails."""
        with patch.object(settings, 'PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('app.services.career_service.ollama.chat', side_effect=Exception("Ollama connection failed")):
                with pytest.raises(HTTPException) as exc_info:
                    generate_career_plan_logic("Category", "Description", "Timeline")
                
                assert exc_info.value.status_code == 500
    
    @pytest.mark.unit
    def test_generate_career_plan_with_code_blocks(self, temp_prompt_file):
        """Test career plan generation with markdown code blocks."""
        response_with_backticks = {
            "message": {
                "content": '```\n{"skills": [{"skill_name": "Test", "total_days": 5, "topics": []}]}\n```'
            }
        }
        
        with patch.object(settings, 'PROMPT_TEMPLATE_PATH', temp_prompt_file):
            with patch('app.services.career_service.ollama.chat', return_value=response_with_backticks):
                result = generate_career_plan_logic("Category", "Description", "Timeline")
                
                assert isinstance(result, JSONResponse)
                response_data = json.loads(result.body.decode())
                assert "skills" in response_data
