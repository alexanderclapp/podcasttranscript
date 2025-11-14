from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Podcast Transcription API",
    description="API for transcribing and summarizing podcasts",
    version="1.0.0"
)

# Configure CORS
# Allow origins from environment variable or default to localhost
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Podcast Transcription API",
        "status": "running",
        "endpoints": {
            "process_podcast": "/api/process-podcast"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}

