"""
Benefits content block
"""
from typing import Dict, Any, List
from .base_block import ContentBlock
from ..models.product import Product


class BenefitsBlock(ContentBlock):
    """
    Content block for generating benefits section.
    Transforms product benefits into structured, engaging copy.
    """
    
    def __init__(self):
        super().__init__("BenefitsBlock")
    
    def generate(self, data: Product) -> Dict[str, Any]:
        """
        Generate benefits section from product data.
        
        Args:
            data: Product model
            
        Returns:
            Dict with structured benefits content
        """
        benefits_list = []
        
        for benefit in data.benefits:
            benefits_list.append({
                "benefit": benefit,
                "description": self._generate_benefit_description(benefit, data),
                "icon": self._get_benefit_icon(benefit)
            })
        
        return {
            "title": "Key Benefits",
            "subtitle": f"What {data.product_name} Does For Your Skin",
            "benefits": benefits_list,
            "summary": self._generate_summary(data.benefits)
        }
    
    def _generate_benefit_description(self, benefit: str, product: Product) -> str:
        """Generate detailed description for a benefit"""
        descriptions = {
            "Brightening": f"Powered by {product.concentration}, this serum helps reveal a more radiant and even-toned complexion.",
            "Fades dark spots": "Targets hyperpigmentation and dark spots, promoting a clearer, more uniform skin tone over time."
        }
        return descriptions.get(benefit, f"Experience the transformative effects of {benefit.lower()}.")
    
    def _get_benefit_icon(self, benefit: str) -> str:
        """Map benefit to icon identifier"""
        icons = {
            "Brightening": "✨",
            "Fades dark spots": "🎯"
        }
        return icons.get(benefit, "⭐")
    
    def _generate_summary(self, benefits: List[str]) -> str:
        """Generate overall benefits summary"""
        return f"Experience {' and '.join([b.lower() for b in benefits])} with consistent use."
