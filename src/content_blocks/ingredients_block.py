"""
Ingredients content block
"""
from typing import Dict, Any
from .base_block import ContentBlock
from ..models.product import Product


class IngredientsBlock(ContentBlock):
    """
    Content block for generating ingredients section.
    Enriches ingredient lists with descriptions and benefits.
    """
    
    def __init__(self):
        super().__init__("IngredientsBlock")
        
        # Knowledge base for ingredient descriptions
        self.ingredient_data = {
            "Vitamin C": {
                "scientific_name": "Ascorbic Acid",
                "description": "A powerful antioxidant that brightens skin and boosts collagen production",
                "benefits": ["Brightening", "Anti-aging", "Antioxidant protection"]
            },
            "Hyaluronic Acid": {
                "scientific_name": "Sodium Hyaluronate",
                "description": "A moisture-binding ingredient that hydrates and plumps skin",
                "benefits": ["Deep hydration", "Plumping", "Moisture retention"]
            }
        }
    
    def generate(self, data: Product) -> Dict[str, Any]:
        """
        Generate ingredients section from product data.
        
        Args:
            data: Product model
            
        Returns:
            Dict with structured ingredients content
        """
        ingredients_details = []
        
        for ingredient in data.key_ingredients:
            ingredient_info = self.ingredient_data.get(ingredient, {
                "scientific_name": ingredient,
                "description": f"A key active ingredient in this formulation",
                "benefits": ["Skin enhancement"]
            })
            
            ingredients_details.append({
                "name": ingredient,
                "scientific_name": ingredient_info["scientific_name"],
                "description": ingredient_info["description"],
                "benefits": ingredient_info["benefits"]
            })
        
        return {
            "title": "Star Ingredients",
            "subtitle": "Science-Backed Actives That Work",
            "concentration": data.concentration,
            "ingredients": ingredients_details,
            "formula_type": self._determine_formula_type(data)
        }
    
    def _determine_formula_type(self, product: Product) -> str:
        """Determine formula type based on ingredients"""
        if "Vitamin C" in product.key_ingredients and "Hyaluronic Acid" in product.key_ingredients:
            return "Brightening + Hydrating Formula"
        return "Active Serum Formula"
