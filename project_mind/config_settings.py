import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # LLM Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Mock API Configuration
    MOCK_API_HOST = os.getenv("MOCK_API_HOST", "localhost")
    MOCK_API_PORT = int(os.getenv("MOCK_API_PORT", "8000"))
    MOCK_API_BASE_URL = f"http://{MOCK_API_HOST}:{MOCK_API_PORT}"
    
    # Personas
    PERSONAS = [
        "Developer",
        "QA Engineer",
        "Project Manager",
        "Product Owner",
        "Scrum Master",
        "Business Analyst",
        "Business Data Analyst"
    ]
    
    # Projects
    PROJECTS = [
        "Payment Gateway Integration",
        "Mobile App Rewrite",
        "Customer Dashboard v2.0",
        "API Migration Project"
    ]
    
    # Intent Categories
    INTENT_CATEGORIES = [
        "Get Information",
        "Generate Report",
        "Track Progress",
        "Identify Risks",
        "Get Recommendations",
        "Understand Requirements",
        "Review Quality",
        "Check Status"
    ]

settings = Settings()