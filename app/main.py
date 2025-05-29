from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .routers import pdf

app = FastAPI(
    title="GenMediPlan",
    description="AI-powered Healthcare Analysis and Treatment Planning System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
    expose_headers=["Content-Length"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Include routers
app.include_router(pdf.router)

# Mount static files for frontend
frontend_build_path = Path("frontend/build")
if frontend_build_path.exists():
    # Serve static files
    app.mount("/static", StaticFiles(directory=str(frontend_build_path / "static")), name="static")
    
    # Serve index.html for all other routes
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}
        return FileResponse(str(frontend_build_path / "index.html"))

@app.get("/api")
async def root():
    return {"message": "Welcome to GenMediPlan API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 