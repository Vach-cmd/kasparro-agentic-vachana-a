"""
ProductPageGeneratorAgent: Generates product description pages
"""
from typing import Any
from .base_agent import BaseAgent
from ..templates import ProductPageTemplate


class ProductPageGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating product description pages.
    
    Input: Product - Product model
    Output: Dict - Rendered product page
    """
    
    def __init__(self):
        super().__init__("ProductPageGeneratorAgent")
        self.template = ProductPageTemplate()
    
    def execute(self, input_data: Any) -> dict:
        """
        Generate product description page using ProductPageTemplate.
        
        Args:
            input_data: Product model
            
        Returns:
            Dict: Rendered product page
        """
        self.log("Generating product description page...")
        
        # Render using template
        product_page = self.template.render(input_data)
        
        self.log(f"Generated product page for {product_page['product_name']}")
        
        return product_page
