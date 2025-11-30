from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.endpoints import career

# Setup logging
setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

# Include routers
app.include_router(career.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
