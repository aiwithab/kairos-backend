# AI Career Coach

AI Career Coach is a FastAPI-based application that generates personalized career study plans using a local LLM (Ollama). It takes a job category, job description, and a timeline as input, and produces a structured study schedule with prioritized skills, topics, and study materials.

## Features

- **Personalized Career Plans**: Generates study plans tailored to specific job descriptions.
- **Local LLM Integration**: Uses Ollama to run large language models locally for privacy and cost-efficiency.
- **Structured Output**: Returns a JSON response with skills, topics, priorities, and timelines.
- **FastAPI Powered**: Built with high-performance FastAPI framework.
- **Production Ready Structure**: Modular codebase organized for scalability.

## Prerequisites

- **Python 3.10+**
- **Ollama**: You need to have [Ollama](https://ollama.com/) installed and running.
- **Model**: Pull the required model (default: `gpt-oss:120b-cloud`, but you can configure this).
  ```bash
  ollama pull gpt-oss:120b-cloud
  ```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Kairos
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The application uses `pydantic-settings` for configuration. You can customize settings by creating a `.env` file in the root directory or setting environment variables.

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PROJECT_NAME` | AI Career Coach | Name of the API project |
| `OLLAMA_MODEL` | gpt-oss:120b-cloud | The Ollama model tag to use |
| `PROMPT_TEMPLATE_PATH` | resources/prompt_example.txt | Path to the prompt template file |

## Usage

1.  **Start the Ollama server:**
    Ensure Ollama is running in the background.

2.  **Run the FastAPI server:**
    ```bash
    python -m uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

3.  **Generate a Career Plan:**
    Send a POST request to `/career-plan`.

    **Example Request:**
    ```bash
    curl -X POST "http://localhost:8000/career-plan" \
         -H "Content-Type: application/json" \
         -d '{
               "user_id": "123",
               "category": "Software Engineering",
               "timeline": "1 month",
               "job_description": "Backend Developer with Python and FastAPI"
             }'
    ```

    **Example Response:**
    ```json
    {
      "skills": [
        {
          "skill_name": "Python",
          "total_days": 5,
          "topics": [
            {
              "topic_name": "FastAPI",
              "study_material": "https://fastapi.tiangolo.com/",
              "timeline": "2 days",
              "priority": "High",
              "bonus": false
            }
          ]
        }
      ]
    }
    ```

## Project Structure

```
.
├── app/
│   ├── api/            # API route handlers
│   ├── core/           # Core configuration and logging
│   ├── schemas/        # Pydantic data models
│   ├── services/       # Business logic and external integrations
│   └── main.py         # Application entry point
├── resources/          # Static resources (prompt templates)
├── tests/              # Test scripts
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Testing

You can run the included test script to verify the API:

```bash
python test_api.py
```


## Contributors
- [Saquib Ansari](https://github.com/saquibansari0101)