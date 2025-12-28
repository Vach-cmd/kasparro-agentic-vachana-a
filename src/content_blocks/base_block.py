"""
Base content block interface
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class ContentBlock(ABC):
    """
    Base class for reusable content logic blocks.
    Each block applies specific rules to transform data into copy.
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def generate(self, data: Any) -> Dict[str, Any]:
        """
        Generate content based on input data.
        
        Args:
            data: Input data
            
        Returns:
            Dict containing generated content
        """
        pass
    
    def get_name(self) -> str:
        """Get block name"""
        return self.name
