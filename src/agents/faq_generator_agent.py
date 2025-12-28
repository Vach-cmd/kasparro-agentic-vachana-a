"""
FAQGeneratorAgent: Generates FAQ pages
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..templates import FAQTemplate


class FAQGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating FAQ pages.
    
    Input: Dict with 'product' and 'questions' keys
    Output: Dict - Rendered FAQ page
    """
    
    def __init__(self):
        super().__init__("FAQGeneratorAgent")
        self.template = FAQTemplate()
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate FAQ page using FAQTemplate.
        
        Args:
            input_data: Dict containing product and questions
            
        Returns:
            Dict: Rendered FAQ page
        """
        self.log("Generating FAQ page...")
        
        # Render using template
        faq_page = self.template.render(input_data)
        
        self.log(f"Generated FAQ with {faq_page['metadata']['total_questions']} questions")
        
        return faq_page
