import pytest
from pydantic import ValidationError
from app.schemas.job import JobRequest


class TestJobRequest:
    """Test cases for JobRequest schema."""
    
    @pytest.mark.unit
    def test_job_request_valid(self):
        """Test JobRequest with valid data."""
        data = {
            "user_id": "user123",
            "category": "Software Engineering",
            "timeline": "2 weeks",
            "job_description": "Backend Developer"
        }
        
        request = JobRequest(**data)
        assert request.user_id == "user123"
        assert request.category == "Software Engineering"
        assert request.timeline == "2 weeks"
        assert request.job_description == "Backend Developer"
    
    @pytest.mark.unit
    def test_job_request_missing_field(self):
        """Test JobRequest with missing required field."""
        data = {
            "user_id": "user123",
            "category": "Software Engineering",
            "timeline": "2 weeks"
            # Missing job_description
        }
        
        with pytest.raises(ValidationError) as exc_info:
            JobRequest(**data)
        
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("job_description",) for error in errors)
    
    @pytest.mark.unit
    def test_job_request_extra_fields(self):
        """Test JobRequest with extra fields (should be ignored)."""
        data = {
            "user_id": "user123",
            "category": "Software Engineering",
            "timeline": "2 weeks",
            "job_description": "Backend Developer",
            "extra_field": "should be ignored"
        }
        
        request = JobRequest(**data)
        assert not hasattr(request, "extra_field")
    
    @pytest.mark.unit
    def test_job_request_type_coercion(self):
        """Test JobRequest with invalid type (should raise validation error)."""
        data = {
            "user_id": 123,  # Should be string, Pydantic v2 is stricter
            "category": "Software Engineering",
            "timeline": "2 weeks",
            "job_description": "Backend Developer"
        }
        
        # Pydantic v2 doesn't coerce int to str by default
        with pytest.raises(ValidationError):
            JobRequest(**data)
