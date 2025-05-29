from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pdf_parser.parser import PDFParser
from models.predictor import TreatmentPredictor
import os
from pathlib import Path
from datetime import datetime
from app.config import get_settings
import json

router = APIRouter(prefix="/api/v1")

# Initialize settings
settings = get_settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Create analysis history directory
ANALYSIS_HISTORY_DIR = Path("data/analysis_history")
ANALYSIS_HISTORY_DIR.mkdir(parents=True, exist_ok=True)

def save_analysis(analysis_data: dict):
    """Save analysis data to history"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analysis_{timestamp}.json"
    filepath = ANALYSIS_HISTORY_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    return filename

def get_latest_analysis():
    """Get the most recent analysis"""
    try:
        analysis_files = list(ANALYSIS_HISTORY_DIR.glob("analysis_*.json"))
        if not analysis_files:
            return None
            
        latest_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
        with open(latest_file, 'r') as f:
            return json.load(f)
    except Exception:
        return None

@router.post("/upload")
async def upload_pdf(file: UploadFile):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Create a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Save the file
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
            
        with open(file_path, "wb") as f:
            f.write(content)

        # Parse the PDF
        parser = PDFParser()
        parsed_data = parser.parse_pdf(file_path)
        
        # Generate treatment recommendations using Together API
        predictor = TreatmentPredictor()
        treatment_plan = predictor.predict_treatment(parsed_data)
        
        # Combine parsed data with treatment recommendations
        result = {
            **parsed_data,
            "treatment_plan": treatment_plan,
            "timestamp": timestamp,
            "original_filename": file.filename
        }
        
        # Save analysis to history
        save_analysis(result)

        return JSONResponse(content={
            "message": "File uploaded and processed successfully",
            "filename": filename,
            "analysis": result
        })

    except Exception as e:
        # If error occurs, clean up the file if it was saved
        if 'file_path' in locals() and os.path.exists(file_path):
            os.unlink(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis")
async def get_analysis():
    """Get the most recent analysis"""
    analysis = get_latest_analysis()
    if not analysis:
        return {
            "message": "No analysis available",
            "analysis": {
                "status": "No recent analysis available"
            }
        }
    
    return {
        "message": "Analysis retrieved successfully",
        "analysis": analysis
    } 