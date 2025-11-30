## Testing

The project includes a comprehensive test suite using pytest.

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=app --cov-report=html
```

Run only unit tests:
```bash
pytest -m unit
```

Run only integration tests:
```bash
pytest -m integration
```

Run tests with verbose output:
```bash
pytest -v
```

### Test Structure

- `tests/test_career_service.py` - Unit tests for career service logic
- `tests/test_api_endpoints.py` - Unit tests for API endpoints
- `tests/test_schemas.py` - Unit tests for Pydantic schemas
- `tests/test_integration.py` - Integration tests for end-to-end flows
- `tests/conftest.py` - Shared fixtures and test configuration

### Test Coverage

The test suite covers:
- Prompt template loading and formatting
- Ollama integration and response parsing
- API endpoint validation and error handling
- Schema validation
- End-to-end request/response flow
