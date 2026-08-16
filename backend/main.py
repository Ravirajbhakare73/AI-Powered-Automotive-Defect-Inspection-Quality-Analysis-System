from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.inspection import router as inspection_router
from backend.api.agent import router as agent_router


app = FastAPI(
    title="AI Automotive Defect Inspection & Quality Analysis System",
    description=(
        "YOLO11-based automotive defect detection "
        "with RAG and AI-powered quality analysis."
    ),
    version="1.0.0"
)


# ==================================================
# Serve generated inspection evidence images
# ==================================================

app.mount(
    "/reports",
    StaticFiles(directory="reports"),
    name="reports"
)


# ==================================================
# CORS Configuration
# ==================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==================================================
# API Routes
# ==================================================

app.include_router(
    inspection_router,
    prefix="/api"
)

app.include_router(
    agent_router,
    prefix="/api"
)


# ==================================================
# Root Endpoint
# ==================================================

@app.get("/")
def root():

    return {
        "application": (
            "AI Automotive Defect "
            "Inspection & Quality Analysis"
        ),
        "status": "running"
    }


# ==================================================
# Health Check
# ==================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }