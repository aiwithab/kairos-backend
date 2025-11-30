import json
import logging
import ollama
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from app.core.config import settings
import re
import traceback

logger = logging.getLogger(__name__)

def get_prompt(category: str, job_description: str, timeline: str) -> str:
    try:
        with open(settings.PROMPT_TEMPLATE_PATH, 'r') as f:
            template = f.read()
        return template.replace('{category}', category).replace('{job_description}', job_description).replace('{timeline}', timeline)
    except FileNotFoundError:
        logger.error(f"Prompt template file '{settings.PROMPT_TEMPLATE_PATH}' not found")
        raise HTTPException(status_code=500, detail="Prompt template not found")
    except Exception as e:
        logger.error(f"Error reading prompt template: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def generate_career_plan_logic(category: str, job_description: str, timeline: str):
    prompt = get_prompt(category, job_description, timeline)
    logger.info("Prompt generated successfully")
    
    try:
        logger.info(f"Sending request to Ollama model '{settings.OLLAMA_MODEL}'")
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        logger.info("Received response from Ollama")
        
        content = response['message']['content']
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
             content = content.split("```")[1].split("```")[0].strip()
        
        parsed_content = json.loads(content)
        logger.info("Successfully parsed JSON response")
        return JSONResponse(content=parsed_content,status_code=status.HTTP_200_OK)

    except json.JSONDecodeError:
        logger.error("Failed to parse JSON from model response")
        logger.error(f"Raw response content: {response['message']['content']}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to parse JSON from model response")
    except Exception as e:
        logger.error(f"An error occurred during processing: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
