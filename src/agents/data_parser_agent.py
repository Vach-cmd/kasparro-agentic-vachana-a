"""
DataParserAgent: Parses and validates product data
"""
import json
from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.product import Product


class DataParserAgent(BaseAgent):
    """
    Agent responsible for parsing raw product data into structured Product model.
    
    Input: Dict[str, Any] - Raw product data
    Output: Product - Validated product model
    """
    
    def __init__(self):
        super().__init__("DataParserAgent")
    
    def execute(self, input_data: Dict[str, Any]) -> Product:
        """
        Parse and validate product data.
        
        Args:
            input_data: Raw product data dictionary
            
        Returns:
            Product: Validated product model
        """
        self.log("Parsing product data...")
        
        # Validate input
        self.validate_input(input_data)
        
        # Parse into Product model (Pydantic will validate)
        try:
            product = Product(**input_data)
            self.log(f"Successfully parsed product: {product.product_name}")
            return product
        except Exception as e:
            self.log(f"Error parsing product data: {str(e)}")
            raise
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data structure"""
        required_fields = [
            'product_name', 'concentration', 'skin_type', 
            'key_ingredients', 'benefits', 'how_to_use', 
            'side_effects', 'price'
        ]
        
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Missing required field: {field}")
        
        return True
