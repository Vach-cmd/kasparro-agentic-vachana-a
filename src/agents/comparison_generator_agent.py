"""
ComparisonGeneratorAgent: Generates comparison pages
"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..templates import ComparisonTemplate
from ..models.product import Product


class ComparisonGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating product comparison pages.
    Includes logic to create fictional Product B for comparison.
    
    Input: Product - Product model
    Output: Dict - Rendered comparison page
    """
    
    def __init__(self):
        super().__init__("ComparisonGeneratorAgent")
        self.template = ComparisonTemplate()
    
    def execute(self, input_data: Product) -> Dict[str, Any]:
        """
        Generate comparison page. Creates fictional Product B for comparison.
        
        Args:
            input_data: Product model (Product A)
            
        Returns:
            Dict: Rendered comparison page
        """
        self.log("Generating comparison page...")
        
        # Create fictional Product B
        product_b = self._create_fictional_product_b()
        
        self.log(f"Comparing {input_data.product_name} vs {product_b.product_name}")
        
        # Render using template
        comparison_page = self.template.render({
            'product_a': input_data,
            'product_b': product_b
        })
        
        self.log("Comparison page generated successfully")
        
        return comparison_page
    
    def _create_fictional_product_b(self) -> Product:
        """
        Create a structured fictional product for comparison.
        Product B is intentionally different to showcase comparison logic.
        """
        return Product(
            product_name="RadiantGlow C+ Serum",
            concentration="15% Vitamin C",
            skin_type=["Dry", "Normal", "Combination"],
            key_ingredients=["Vitamin C", "Vitamin E", "Ferulic Acid"],
            benefits=["Anti-aging", "Brightening", "Firming"],
            how_to_use="Apply 3-4 drops in the evening after cleansing",
            side_effects="Possible sensitivity to sunlight",
            price="₹899"
        )
