"""
Comparison Page Template
"""
from typing import Dict, Any
from .base_template import Template
from ..content_blocks import ComparisonBlock


class ComparisonTemplate(Template):
    """
    Template for product comparison page generation.
    Uses ComparisonBlock to generate structured comparisons.
    """
    
    def __init__(self):
        super().__init__("ComparisonTemplate")
        self.add_content_block(ComparisonBlock())
    
    def get_schema(self) -> Dict[str, Any]:
        """Get comparison page template schema"""
        return {
            "type": "ComparisonPage",
            "fields": {
                "title": {"type": "string", "required": True},
                "product_a": {"type": "object", "required": True},
                "product_b": {"type": "object", "required": True},
                "comparison_matrix": {"type": "array", "required": True},
                "recommendation": {"type": "object", "required": True},
                "metadata": {"type": "object", "required": True}
            },
            "dependencies": {
                "comparison_matrix": "ComparisonBlock"
            }
        }
    
    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render comparison page using ComparisonBlock.
        
        Args:
            data: Dict with 'product_a' and 'product_b' keys
            
        Returns:
            Rendered comparison page
        """
        product_a = data['product_a']
        product_b = data['product_b']
        
        # Format product summaries
        product_a_summary = self._format_product_summary(product_a)
        product_b_summary = self._format_product_summary(product_b)
        
        # Use ComparisonBlock to generate comparison matrix
        comparison_block = next(b for b in self.content_blocks if isinstance(b, ComparisonBlock))
        comparison_result = comparison_block.generate({
            'product_a': product_a,
            'product_b': product_b
        })
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            product_a, 
            product_b, 
            comparison_result['overall_winner']
        )
        
        import datetime
        metadata = {
            "generated_at": datetime.datetime.now().isoformat(),
            "template": self.name,
            "version": "1.0",
            "comparison_criteria_count": len(comparison_result['criteria'])
        }
        
        return {
            "title": f"{product_a.product_name} vs {product_b.product_name}",
            "product_a": product_a_summary,
            "product_b": product_b_summary,
            "comparison_matrix": comparison_result['criteria'],
            "recommendation": recommendation,
            "metadata": metadata
        }
    
    def _format_product_summary(self, product: Any) -> Dict[str, Any]:
        """Format product summary for comparison"""
        return {
            "name": product.product_name,
            "concentration": product.concentration,
            "price": product.price,
            "skin_type": product.skin_type,
            "key_ingredients": product.key_ingredients,
            "benefits": product.benefits
        }
    
    def _generate_recommendation(self, product_a: Any, product_b: Any, winner: str) -> Dict[str, Any]:
        """Generate recommendation based on comparison"""
        if winner == "product_a":
            recommended_product = product_a
            reason = f"{product_a.product_name} offers better overall value and effectiveness."
        elif winner == "product_b":
            recommended_product = product_b
            reason = f"{product_b.product_name} provides superior benefits and formulation."
        else:
            recommended_product = product_a
            reason = "Both products have comparable benefits. Choose based on your specific needs."
        
        return {
            "recommended_product": recommended_product.product_name,
            "reason": reason,
            "best_for": self._determine_best_for(recommended_product)
        }
    
    def _determine_best_for(self, product: Any) -> str:
        """Determine what the product is best for"""
        return f"Best for {' and '.join(product.skin_type).lower()} skin seeking {' and '.join([b.lower() for b in product.benefits])}"
