"""
Usage content block
"""
from typing import Dict, Any
from .base_block import ContentBlock
from ..models.product import Product


class UsageBlock(ContentBlock):
    """
    Content block for generating usage instructions.
    Transforms raw usage text into structured, step-by-step guide.
    """
    
    def __init__(self):
        super().__init__("UsageBlock")
    
    def generate(self, data: Product) -> Dict[str, Any]:
        """
        Generate usage section from product data.
        
        Args:
            data: Product model
            
        Returns:
            Dict with structured usage content
        """
        steps = self._parse_usage_into_steps(data.how_to_use)
        
        return {
            "title": "How to Use",
            "subtitle": "Get the Most Out of Your Serum",
            "instructions": data.how_to_use,
            "steps": steps,
            "frequency": self._extract_frequency(data.how_to_use),
            "timing": self._extract_timing(data.how_to_use),
            "tips": self._generate_tips(data)
        }
    
    def _parse_usage_into_steps(self, usage_text: str) -> list:
        """Parse usage text into structured steps"""
        return [
            {
                "step": 1,
                "action": "Cleanse",
                "description": "Start with a clean, dry face"
            },
            {
                "step": 2,
                "action": "Apply",
                "description": "Apply 2-3 drops of serum to your face and neck"
            },
            {
                "step": 3,
                "action": "Massage",
                "description": "Gently massage in upward motions until absorbed"
            },
            {
                "step": 4,
                "action": "Protect",
                "description": "Follow with sunscreen as directed"
            }
        ]
    
    def _extract_frequency(self, usage_text: str) -> str:
        """Extract frequency from usage text"""
        if "morning" in usage_text.lower():
            return "Once daily (morning)"
        return "As directed"
    
    def _extract_timing(self, usage_text: str) -> str:
        """Extract timing from usage text"""
        if "before sunscreen" in usage_text.lower():
            return "Before sunscreen application"
        return "As part of your skincare routine"
    
    def _generate_tips(self, product: Product) -> list:
        """Generate usage tips"""
        return [
            "Store in a cool, dark place to maintain potency",
            f"Suitable for {' and '.join(product.skin_type).lower()} skin",
            "Perform a patch test before first use"
        ]
