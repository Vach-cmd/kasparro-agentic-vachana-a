"""
Comparison content block
"""
from typing import Dict, Any
from .base_block import ContentBlock
from ..models.product import Product


class ComparisonBlock(ContentBlock):
    """
    Content block for generating comparison matrices.
    Compares products across multiple dimensions.
    """
    
    def __init__(self):
        super().__init__("ComparisonBlock")
    
    def generate(self, data: Dict[str, Product]) -> Dict[str, Any]:
        """
        Generate comparison matrix from two products.
        
        Args:
            data: Dict with 'product_a' and 'product_b' keys
            
        Returns:
            Dict with structured comparison content
        """
        product_a = data['product_a']
        product_b = data['product_b']
        
        comparison_criteria = [
            {
                "criterion": "Vitamin C Concentration",
                "product_a_value": product_a.concentration,
                "product_b_value": product_b.concentration,
                "winner": self._compare_concentration(product_a, product_b)
            },
            {
                "criterion": "Key Ingredients",
                "product_a_value": ", ".join(product_a.key_ingredients),
                "product_b_value": ", ".join(product_b.key_ingredients),
                "winner": self._compare_ingredients(product_a, product_b)
            },
            {
                "criterion": "Skin Type Compatibility",
                "product_a_value": ", ".join(product_a.skin_type),
                "product_b_value": ", ".join(product_b.skin_type),
                "winner": self._compare_skin_types(product_a, product_b)
            },
            {
                "criterion": "Primary Benefits",
                "product_a_value": ", ".join(product_a.benefits),
                "product_b_value": ", ".join(product_b.benefits),
                "winner": "tie"
            },
            {
                "criterion": "Price",
                "product_a_value": product_a.price,
                "product_b_value": product_b.price,
                "winner": self._compare_price(product_a, product_b)
            }
        ]
        
        return {
            "criteria": comparison_criteria,
            "overall_winner": self._determine_overall_winner(comparison_criteria),
            "summary": self._generate_comparison_summary(product_a, product_b, comparison_criteria)
        }
    
    def _compare_concentration(self, p1: Product, p2: Product) -> str:
        """Compare vitamin C concentration"""
        # Extract percentage from concentration string
        p1_pct = int(p1.concentration.split('%')[0])
        p2_pct = int(p2.concentration.split('%')[0])
        
        if p1_pct > p2_pct:
            return "product_a"
        elif p2_pct > p1_pct:
            return "product_b"
        return "tie"
    
    def _compare_ingredients(self, p1: Product, p2: Product) -> str:
        """Compare ingredient lists"""
        if len(p1.key_ingredients) > len(p2.key_ingredients):
            return "product_a"
        elif len(p2.key_ingredients) > len(p1.key_ingredients):
            return "product_b"
        return "tie"
    
    def _compare_skin_types(self, p1: Product, p2: Product) -> str:
        """Compare skin type compatibility"""
        if len(p1.skin_type) > len(p2.skin_type):
            return "product_a"
        elif len(p2.skin_type) > len(p1.skin_type):
            return "product_b"
        return "tie"
    
    def _compare_price(self, p1: Product, p2: Product) -> str:
        """Compare prices (lower is better for value)"""
        # Extract numeric value from price string
        p1_price = int(''.join(filter(str.isdigit, p1.price)))
        p2_price = int(''.join(filter(str.isdigit, p2.price)))
        
        if p1_price < p2_price:
            return "product_a"
        elif p2_price < p1_price:
            return "product_b"
        return "tie"
    
    def _determine_overall_winner(self, criteria: list) -> str:
        """Determine overall winner from comparison criteria"""
        scores = {"product_a": 0, "product_b": 0, "tie": 0}
        
        for item in criteria:
            scores[item["winner"]] += 1
        
        if scores["product_a"] > scores["product_b"]:
            return "product_a"
        elif scores["product_b"] > scores["product_a"]:
            return "product_b"
        return "tie"
    
    def _generate_comparison_summary(self, p1: Product, p2: Product, criteria: list) -> str:
        """Generate comparison summary"""
        winner = self._determine_overall_winner(criteria)
        
        if winner == "product_a":
            return f"{p1.product_name} offers better overall value with competitive pricing and proven ingredients."
        elif winner == "product_b":
            return f"{p2.product_name} stands out with superior formulation and broader benefits."
        return "Both products offer comparable benefits with different strengths."
