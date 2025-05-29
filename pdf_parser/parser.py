from typing import Dict, Any, List, Optional
import PyPDF2
import spacy
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_together import Together
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
import os
import re
from dotenv import load_dotenv

class PDFParser:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize PDFParser with optional API key.
        
        Args:
            api_key (Optional[str]): Together API key. If not provided, will try to get from environment.
            
        Raises:
            ValueError: If no API key is found or if the key is invalid.
        """
        # Load environment variables from .env file if it exists
        load_dotenv()
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        
        # Validate API key
        if not self.api_key:
            raise ValueError(
                "Together API key is required. Either pass it to the constructor or "
                "set TOGETHER_API_KEY environment variable."
            )
        
        if not self._validate_api_key(self.api_key):
            raise ValueError("Invalid Together API key format.")
            
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy model 'en_core_web_sm' not found. "
                "Please install it using: python -m spacy download en_core_web_sm"
            )
            
        try:
            self.llm = Together(
                model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
                temperature=0.7,
                max_tokens=1000,
                together_api_key=self.api_key
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Together LLM: {str(e)}")
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False
        )
        
        # Initialize prompts
        self.extraction_prompt = PromptTemplate.from_template(
            """Extract medical information from the following text. Focus on:
            - Patient demographics (age, gender)
            - Medical conditions
            - Medications
            - Allergies
            - Vital signs
            - Lab results
            - Treatment history
            
            Text: {text}
            
            Provide the information in a structured format."""
        )
        
        self.treatment_prompt = PromptTemplate.from_template(
            """Based on the following medical information, provide treatment recommendations:
            {medical_info}
            
            Consider:
            1. Current medications and their interactions
            2. Patient's medical history
            3. Allergies and contraindications
            4. Best practices for the conditions
            
            Provide structured recommendations."""
        )
        
        # Initialize chains
        self.extraction_chain = (
            {"text": RunnablePassthrough()}
            | self.extraction_prompt
            | self.llm
            | StrOutputParser()
        )
        
        self.treatment_chain = (
            {"medical_info": RunnablePassthrough()}
            | self.treatment_prompt
            | self.llm
            | StrOutputParser()
        )

    def _validate_api_key(self, api_key: str) -> bool:
        """Validate the format of the Together API key.
        
        Args:
            api_key (str): The API key to validate
            
        Returns:
            bool: True if the key format is valid, False otherwise
        """
        # Together API keys typically start with 'tgp_v1_' and are followed by a long string
        return bool(re.match(r'^tgp_v1_[A-Za-z0-9_-]{40,}$', api_key))

    def update_api_key(self, new_api_key: str) -> None:
        """Update the API key and reinitialize the LLM.
        
        Args:
            new_api_key (str): The new API key to use
            
        Raises:
            ValueError: If the new API key is invalid
        """
        if not self._validate_api_key(new_api_key):
            raise ValueError("Invalid Together API key format.")
            
        self.api_key = new_api_key
        try:
            self.llm = Together(
                model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
                temperature=0.7,
                max_tokens=1000,
                together_api_key=self.api_key
            )
        except Exception as e:
            raise RuntimeError(f"Failed to update Together LLM with new API key: {str(e)}")

    def parse_pdf(self, file_path: str) -> Dict:
        """Parse PDF and extract medical information"""
        try:
            # Load and split PDF
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            texts = self.text_splitter.split_documents(pages)
            
            # Extract information from each chunk
            medical_info = []
            for text in texts:
                result = self.extraction_chain.invoke(text.page_content)
                medical_info.append(result)
            
            # Combine and process results
            combined_info = "\n".join(medical_info)
            
            # Get treatment recommendations
            treatment_recs = self.treatment_chain.invoke(combined_info)
            
            # Process with spaCy for additional validation
            doc = self.nlp(combined_info)
            
            # Extract entities
            entities = {
                "conditions": [],
                "medications": [],
                "allergies": [],
                "vitals": []
            }
            
            for ent in doc.ents:
                if ent.label_ == "DISEASE":
                    entities["conditions"].append(ent.text)
                elif ent.label_ == "CHEMICAL":
                    entities["medications"].append(ent.text)
                elif "allerg" in ent.text.lower():
                    entities["allergies"].append(ent.text)
                elif any(vital in ent.text.lower() for vital in ["blood pressure", "heart rate", "temperature"]):
                    entities["vitals"].append(ent.text)
            
            return {
                "raw_text": combined_info,
                "entities": entities,
                "treatment_recommendations": treatment_recs,
                "metadata": {
                    "pages": len(pages),
                    "chunks": len(texts)
                }
            }
            
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")

    def extract_medical_info(self, text: str) -> Dict:
        """Extract medical information from text"""
        try:
            result = self.extraction_chain.invoke(text)
            return {"extracted_info": result}
        except Exception as e:
            raise Exception(f"Error extracting medical information: {str(e)}")

    def get_treatment_recommendations(self, medical_info: str) -> Dict:
        """Get treatment recommendations based on medical information"""
        try:
            result = self.treatment_chain.invoke(medical_info)
            return {"recommendations": result}
        except Exception as e:
            raise Exception(f"Error getting treatment recommendations: {str(e)}")

    def generate_treatment_recommendations(self, structured_data: Dict[str, Any]) -> str:
        """Generate treatment recommendations using LangChain"""
        try:
            # Use the existing treatment chain
            recommendations = self.treatment_chain.invoke(str(structured_data))
            return recommendations  # Return the string directly
            
        except Exception as e:
            raise Exception(f"Error generating recommendations: {str(e)}")

    def extract_tables(self, file_path: str) -> Dict[str, Any]:
        """Extract tables from PDF using LangChain's table extraction capabilities"""
        # TODO: Implement table extraction using LangChain's table extraction tools
        return {"tables": []}

    def extract_images(self, file_path: str) -> Dict[str, Any]:
        """Extract images from PDF using LangChain's image extraction capabilities"""
        # TODO: Implement image extraction using LangChain's image extraction tools
        return {"images": []}

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF with better formatting preservation"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page in pdf_reader.pages:
                    # Extract text with layout preservation
                    page_text = page.extract_text()
                    
                    # Clean and normalize text
                    page_text = self._clean_text(page_text)
                    text += page_text + "\n"
                    
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
            
        return text

    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important medical symbols
        text = re.sub(r'[^\w\s.,;:()\-/]', '', text)
        
        # Normalize spacing around punctuation
        text = re.sub(r'\s+([.,;:])', r'\1', text)
        
        return text.strip()

    def _extract_section(self, text: str, pattern: str) -> List[str]:
        """Extract relevant sections based on patterns"""
        matches = re.finditer(pattern, text, re.IGNORECASE)
        sections = []
        
        for match in matches:
            # Get context around the match (100 characters before and after)
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            context = text[start:end]
            
            # Clean and add to sections
            cleaned_context = self._clean_text(context)
            if cleaned_context:
                sections.append(cleaned_context)
                
        return sections

    def _extract_structured_data(self, text: str) -> Dict[str, Any]:
        """Extract structured data using NLP and pattern matching"""
        doc = self.nlp(text)
        
        # Initialize structured data
        structured_data = {
            'patient_info': {},
            'medical_history': [],
            'current_symptoms': [],
            'medications': [],
            'vitals': {},
            'allergies': [],
            'diagnosis': [],
            'treatment_plan': []
        }
        
        # Extract patient information
        patient_patterns = {
            'name': r'patient(?:[\'s]|\s+name)?[:]\s*([A-Za-z\s]+)',
            'age': r'age[:]\s*(\d+)',
            'gender': r'(?:gender|sex)[:]\s*([A-Za-z]+)',
            'dob': r'(?:date of birth|dob)[:]\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        }
        
        for key, pattern in patient_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                structured_data['patient_info'][key] = match.group(1).strip()

        # Extract medical sections
        for section, pattern in self.medical_patterns.items():
            sections = self._extract_section(text, pattern)
            
            if section == 'vitals':
                # Parse vital signs into structured format
                for section_text in sections:
                    vitals = self._parse_vitals(section_text)
                    structured_data['vitals'].update(vitals)
            elif section == 'medications':
                structured_data['medications'].extend(self._parse_medications(sections))
            elif section == 'allergies':
                structured_data['allergies'].extend(self._parse_allergies(sections))
            elif section == 'symptoms':
                structured_data['current_symptoms'].extend(self._parse_symptoms(sections))
            elif section == 'diagnosis':
                structured_data['diagnosis'].extend(self._parse_diagnosis(sections))
            elif section == 'treatment':
                structured_data['treatment_plan'].extend(self._parse_treatment(sections))

        return structured_data

    def _parse_vitals(self, text: str) -> Dict[str, str]:
        """Parse vital signs from text"""
        vitals = {}
        patterns = {
            'blood_pressure': r'(\d{2,3}/\d{2,3})\s*(?:mmHg|BP)',
            'heart_rate': r'(\d{2,3})\s*(?:bpm|HR)',
            'temperature': r'(\d{2,3}\.\d{1,2})\s*(?:°F|°C|temp)',
            'respiratory_rate': r'(\d{1,2})\s*(?:breaths/min|RR)',
            'oxygen_saturation': r'(\d{2,3})\s*(?:%|SpO2)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                vitals[key] = match.group(1)
                
        return vitals

    def _parse_medications(self, sections: List[str]) -> List[str]:
        """Parse medications from text"""
        medications = []
        for section in sections:
            # Look for medication patterns
            med_matches = re.finditer(r'([A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(\d+(?:\.\d+)?\s*(?:mg|ml|g|tablet|capsule))', section)
            for match in med_matches:
                med_name = match.group(1).strip()
                dosage = match.group(2).strip()
                medications.append(f"{med_name} - {dosage}")
                
        return medications

    def _parse_allergies(self, sections: List[str]) -> List[str]:
        """Parse allergies from text"""
        allergies = []
        for section in sections:
            # Look for allergy patterns
            allergy_matches = re.finditer(r'(?:allergic|allergy|reaction)\s+to\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)', section)
            for match in allergy_matches:
                allergies.append(match.group(1).strip())
                
        return allergies

    def _parse_symptoms(self, sections: List[str]) -> List[str]:
        """Parse symptoms from text"""
        symptoms = []
        for section in sections:
            # Look for symptom patterns
            symptom_matches = re.finditer(r'(?:symptom|complaint|pain|discomfort)[:]\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)', section)
            for match in symptom_matches:
                symptoms.append(match.group(1).strip())
                
        return symptoms

    def _parse_diagnosis(self, sections: List[str]) -> List[str]:
        """Parse diagnosis from text"""
        diagnoses = []
        for section in sections:
            # Look for diagnosis patterns
            diagnosis_matches = re.finditer(r'(?:diagnosis|condition|disease)[:]\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)', section)
            for match in diagnosis_matches:
                diagnoses.append(match.group(1).strip())
                
        return diagnoses

    def _parse_treatment(self, sections: List[str]) -> List[str]:
        """Parse treatment plan from text"""
        treatments = []
        for section in sections:
            # Look for treatment patterns
            treatment_matches = re.finditer(r'(?:treatment|therapy|procedure)[:]\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)', section)
            for match in treatment_matches:
                treatments.append(match.group(1).strip())
                
        return treatments 