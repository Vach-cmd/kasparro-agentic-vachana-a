"""
Logging utilities for the content generation system.
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


class AgentLogger:
    """Custom logger for agent activities"""
    
    _instances = {}
    
    def __init__(self, name, log_to_file=False):
        self.name = name
        self.logger = logging.getLogger(name)
        
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(f'[{name}] %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # File handler (optional)
            if log_to_file:
                log_dir = Path(__file__).parent.parent / "logs"
                log_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_file = log_dir / f"{name}_{timestamp}.log"
                
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.DEBUG)
                detailed_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                file_handler.setFormatter(detailed_formatter)
                self.logger.addHandler(file_handler)
    
    @classmethod
    def get_logger(cls, name, log_to_file=False):
        """Get or create logger instance"""
        if name not in cls._instances:
            cls._instances[name] = AgentLogger(name, log_to_file)
        return cls._instances[name]
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
