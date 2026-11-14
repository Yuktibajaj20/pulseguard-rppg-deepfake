from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool

from pathlib import Path
import tempfile
import os

from pipeline import analyze_video


app = FastAPI(
    title="PulseGuard API",
    description="Experimental rPPG-based video signal analysis",
    version="1.0"
)


# Allow requests from any frontend (the API has no logins or cookies).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


MAX_FILE_SIZE = 100 * 1024 * 1024


@app.get("/")
def home():
    return {
        "project": "PulseGuard",
        "status": "running"
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename missing"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in [".mp4", ".mov", ".avi"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported video format"
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Video exceeds 100 MB limit"
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Empty video uploaded"
        )

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False
        ) as temp_file:

            temp_file.write(content)
            temp_path = temp_file.name
            