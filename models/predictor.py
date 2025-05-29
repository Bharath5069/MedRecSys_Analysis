from typing import Dict, Any, List
import requests
from pathlib import Path
import json
import os
from app.config import get_settings

class TreatmentPredictor:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.TOGETHER_API_KEY
        if not self.api_key:
            raise ValueError("TOGETHER_API_KEY not found in environment variables")
            
        self.api_url = "https://api.together.xyz/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def load_prompt_template(self, template_path: str) -> str:
        """Load prompt template from file."""
        with open(template_path, 'r') as f:
            return f.read()
    
    def predict_treatment(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate treatment predictions based on patient data using Together AI.
        
        Args:
            patient_data (Dict[str, Any]): Structured patient data from PDF
            
        Returns:
            Dict[str, Any]: Treatment predictions and recommendations
        """
        try:
            # Load prompt template
            prompt_path = Path("prompts/treatment_prompt.txt")
            prompt_template = self.load_prompt_template(str(prompt_path))
            
            # Format prompt with patient data
            formatted_prompt = prompt_template.format(
                patient_data=json.dumps(patient_data, indent=2)
            )
            
            # Prepare the API request
            payload = {
                "model": "mistralai/Mistral-7B-Instruct-v0.2",  # or any other model from Together AI
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a medical AI assistant that provides treatment recommendations based on patient data."
                    },
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # Make API request
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Structure the response
            treatment_plan = {
                "recommendations": content,
                "confidence_score": 0.85,
                "source_data": "Generated from patient medical records"  # Simplified source data
            }
            
            return treatment_plan
            
        except Exception as e:
            raise Exception(f"Error generating treatment prediction: {str(e)}")
    
    def validate_prediction(self, prediction: Dict[str, Any]) -> bool:
        """
        Validate the generated treatment prediction.
        """
        required_fields = ['recommendations', 'confidence_score', 'source_data']
        return all(field in prediction for field in required_fields)