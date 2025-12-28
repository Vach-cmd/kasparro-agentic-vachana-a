"""
Configuration settings for the content generation system.
Centralizes all configurable parameters.
"""
import os
from pathlib import Path


class Config:
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    
    # Input/Output files
    PRODUCT_DATA_FILE = DATA_DIR / "product_data.json"
    FAQ_OUTPUT_FILE = OUTPUT_DIR / "faq.json"
    PRODUCT_PAGE_OUTPUT_FILE = OUTPUT_DIR / "product_page.json"
    COMPARISON_OUTPUT_FILE = OUTPUT_DIR / "comparison_page.json"
    
    # Content generation settings
    MIN_QUESTIONS = 15
    MIN_FAQ_QUESTIONS = 5
    QUESTION_CATEGORIES = [
        "Informational",
        "Safety", 
        "Usage",
        "Purchase",
        "Comparison",
        "Ingredients",
        "Benefits"
    ]
    
    # Agent settings
    ENABLE_LOGGING = True
    LOG_LEVEL = "INFO"
    
    # Template settings
    TEMPLATE_VERSION = "1.0"
    
    # Validation
    VALIDATE_OUTPUT = True
    STRICT_MODE = False  # Fail on warnings
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_setting(cls, key, default=None):
        """Get config value with fallback to environment variable"""
        return os.getenv(key, getattr(cls, key, default))


# Initialize on import
Config.ensure_directories()
