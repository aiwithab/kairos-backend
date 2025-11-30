from fastapi import APIRouter, Depends
from app.schemas.job import JobRequest
from app.services.career_service import generate_career_plan_logic

router = APIRouter()

@router.post("/career-plan")
async def generate_career_plan(request: JobRequest):
    return generate_career_plan_logic(request.category, request.job_description, request.timeline)
