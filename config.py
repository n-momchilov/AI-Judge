#!/usr/bin/env python3
"""
Configuration file for AI GDPR Judge
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for AI GDPR Judge"""
    
    # Ollama Configuration
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    
    # Streamlit Configuration
    STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")
    
    # Legal Analysis Configuration
    DEFAULT_CONFIDENCE_THRESHOLD = float(os.getenv("DEFAULT_CONFIDENCE_THRESHOLD", "0.7"))
    MAX_PRECEDENTS = int(os.getenv("MAX_PRECEDENTS", "5"))
    ANALYSIS_TIMEOUT = int(os.getenv("ANALYSIS_TIMEOUT", "30"))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "gdpr_judge.log")
    
    # Model Options
    AVAILABLE_MODELS = [
        "llama3.1:8b",
        "llama3.1:70b", 
        "mistral:7b",
        "codellama:7b"
    ]
    
    # Legal Analysis Settings
    LEGAL_ANALYSIS_SETTINGS = {
        "temperature": 0.1,  # Low temperature for legal accuracy
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 2048
    }
    
    # GDPR Article Categories
    ARTICLE_CATEGORIES = {
        "principles": ["Article 5"],
        "lawfulness": ["Article 6", "Article 7", "Article 8", "Article 9"],
        "rights": ["Article 12", "Article 13", "Article 14", "Article 15", 
                  "Article 16", "Article 17", "Article 18", "Article 19", 
                  "Article 20", "Article 21", "Article 22"],
        "security": ["Article 25", "Article 32"],
        "breaches": ["Article 33", "Article 34"],
        "dpa": ["Article 35"],
        "transfers": ["Article 44", "Article 45", "Article 46", "Article 47", 
                     "Article 48", "Article 49"],
        "remedies": ["Article 77", "Article 78", "Article 79", "Article 80", 
                    "Article 82"],
        "penalties": ["Article 83", "Article 84"]
    }
    
    # Risk Assessment Thresholds
    RISK_THRESHOLDS = {
        "low": 0.3,
        "medium": 0.6,
        "high": 0.8
    }
    
    # Compliance Checklist Templates
    COMPLIANCE_TEMPLATES = {
        "data_collection": [
            "Identify lawful basis for processing",
            "Implement data minimization",
            "Provide clear privacy notice",
            "Obtain valid consent if required",
            "Implement data subject rights procedures"
        ],
        "data_processing": [
            "Document processing activities",
            "Implement security measures",
            "Conduct data protection impact assessment if required",
            "Ensure data accuracy and up-to-date",
            "Implement retention policies"
        ],
        "data_sharing": [
            "Verify lawful basis for sharing",
            "Implement data processing agreements",
            "Ensure adequate protection for international transfers",
            "Document sharing purposes and legal basis",
            "Implement data subject notification procedures"
        ],
        "data_breach": [
            "Implement breach detection procedures",
            "Assess risk to data subjects",
            "Notify supervisory authority within 72 hours if required",
            "Notify data subjects without undue delay if high risk",
            "Document breach and response measures"
        ]
    }

# Global configuration instance
config = Config()

def get_config() -> Config:
    """Get the global configuration instance"""
    return config

def update_config(updates: Dict[str, Any]) -> None:
    """Update configuration with new values"""
    for key, value in updates.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            print(f"Warning: Unknown configuration key: {key}")

def validate_config() -> bool:
    """Validate configuration settings"""
    try:
        # Validate Ollama host
        if not config.OLLAMA_HOST.startswith(('http://', 'https://')):
            print("Error: OLLAMA_HOST must start with http:// or https://")
            return False
        
        # Validate model
        if config.OLLAMA_MODEL not in config.AVAILABLE_MODELS:
            print(f"Warning: Model {config.OLLAMA_MODEL} not in recommended list")
        
        # Validate confidence threshold
        if not 0.0 <= config.DEFAULT_CONFIDENCE_THRESHOLD <= 1.0:
            print("Error: DEFAULT_CONFIDENCE_THRESHOLD must be between 0.0 and 1.0")
            return False
        
        # Validate timeout
        if config.ANALYSIS_TIMEOUT <= 0:
            print("Error: ANALYSIS_TIMEOUT must be positive")
            return False
        
        return True
        
    except Exception as e:
        print(f"Configuration validation error: {e}")
        return False

if __name__ == "__main__":
    # Test configuration
    if validate_config():
        print("✅ Configuration is valid")
        print(f"Ollama Host: {config.OLLAMA_HOST}")
        print(f"Model: {config.OLLAMA_MODEL}")
        print(f"Confidence Threshold: {config.DEFAULT_CONFIDENCE_THRESHOLD}")
    else:
        print("❌ Configuration validation failed")
