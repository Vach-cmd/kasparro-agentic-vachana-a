"""
Base template interface
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from ..content_blocks.base_block import ContentBlock


class Template(ABC):
    """
    Base class for output templates.
    Templates define structure, fields, rules, and dependencies on content blocks.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.content_blocks: List[ContentBlock] = []
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the template schema definition.
        
        Returns:
            Dict defining template structure and rules
        """
        pass
    
    @abstractmethod
    def render(self, data: Any) -> Dict[str, Any]:
        """
        Render template with data using content blocks.
        
        Args:
            data: Input data
            
        Returns:
            Dict with rendered content matching schema
        """
        pass
    
    def add_content_block(self, block: ContentBlock) -> None:
        """Add a content block to the template"""
        self.content_blocks.append(block)
    
    def get_name(self) -> str:
        """Get template name"""
        return self.name
