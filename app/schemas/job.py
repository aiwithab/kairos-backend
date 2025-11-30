from pydantic import BaseModel

class JobRequest(BaseModel):
    user_id: str
    category: str
    timeline: str
    job_description: str