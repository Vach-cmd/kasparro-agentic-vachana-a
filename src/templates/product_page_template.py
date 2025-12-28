"""
Product Page Template
"""
from typing import Dict, Any
from .base_template import Template
from ..content_blocks import BenefitsBlock, UsageBlock, IngredientsBlock


class ProductPageTemplate(Template):
    """
    Template for product description page generation.
    Composes multiple content blocks into comprehensive product page.
    """
    
    def __init__(self):
        super().__init__("ProductPageTemplate")
        
        # Add required content blocks
        self.add_content_block(BenefitsBlock())
        self.add_content_block(UsageBlock())
        self.add_content_block(IngredientsBlock())
    
    def get_schema(self) -> Dict[str, Any]:
        """Get product page template schema"""
        return {
            "type": "ProductPage",
            "fields": {
                "product_name": {"type": "string", "required": True},
                "tagline": {"type": "string", "required": True},
                "hero_description": {"type": "string", "required": True},
                "key_features": {"type": "array", "required": True},
                "ingredients_section": {"type": "object", "required": True},
                "benefits_section": {"type": "object", "required": True},
                "usage_section": {"type": "object", "required": True},
                "safety_section": {"type": "object", "required": True},
                "pricing_section": {"type": "object", "required": True},
                "metadata": {"type": "object", "required": True}
            },
            "dependencies": {
                "benefits_section": "BenefitsBlock",
                "usage_section": "UsageBlock",
                "ingredients_section": "IngredientsBlock"
            }
        }
    
    def render(self, data: Any) -> Dict[str, Any]:
        """
        Render product page using content blocks.
        
        Args:
            data: Product model
            
        Returns:
            Rendered product page
        """
        product = data
        
        # Generate hero section
        tagline = self._generate_tagline(product)
        hero_description = self._generate_hero_description(product)
        
        # Generate key features
        key_features = self._generate_key_features(product)
        
        # Use content blocks for complex sections
        benefits_block = next(b for b in self.content_blocks if isinstance(b, BenefitsBlock))
        usage_block = next(b for b in self.content_blocks if isinstance(b, UsageBlock))
        ingredients_block = next(b for b in self.content_blocks if isinstance(b, IngredientsBlock))
        
        benefits_section = benefits_block.generate(product)
        usage_section = usage_block.generate(product)
        ingredients_section = ingredients_block.generate(product)
        
        # Generate safety and pricing sections
        safety_section = self._generate_safety_section(product)
        pricing_section = self._generate_pricing_section(product)
        
        import datetime
        metadata = {
            "generated_at": datetime.datetime.now().isoformat(),
            "template": self.name,
            "version": "1.0",
            "content_blocks_used": [b.get_name() for b in self.content_blocks]
        }
        
        return {
            "product_name": product.product_name,
            "tagline": tagline,
            "hero_description": hero_description,
            "key_features": key_features,
            "ingredients_section": ingredients_section,
            "benefits_section": benefits_section,
            "usage_section": usage_section,
            "safety_section": safety_section,
            "pricing_section": pricing_section,
            "metadata": metadata
        }
    
    def _generate_tagline(self, product: Any) -> str:
        """Generate product tagline"""
        return f"{product.concentration} Brightening Serum for Radiant Skin"
    
    def _generate_hero_description(self, product: Any) -> str:
        """Generate hero description"""
        return (
            f"Transform your skin with {product.product_name}, "
            f"a powerful {product.concentration} serum formulated with "
            f"{' and '.join(product.key_ingredients)}. Designed specifically for "
            f"{' and '.join(product.skin_type).lower()} skin, this serum delivers "
            f"{' and '.join([b.lower() for b in product.benefits])} results."
        )
    
    def _generate_key_features(self, product: Any) -> list:
        """Generate key features list"""
        return [
            {
                "feature": f"{product.concentration} Formula",
                "description": "Clinically effective concentration for visible results",
                "icon": "🔬"
            },
            {
                "feature": "Dual-Action Ingredients",
                "description": f"Combines {' and '.join(product.key_ingredients)} for maximum efficacy",
                "icon": "⚡"
            },
            {
                "feature": "Skin Type Optimized",
                "description": f"Perfect for {' and '.join(product.skin_type).lower()} skin",
                "icon": "✓"
            }
        ]
    
    def _generate_safety_section(self, product: Any) -> Dict[str, Any]:
        """Generate safety information section"""
        return {
            "title": "Safety & Side Effects",
            "side_effects": product.side_effects,
            "precautions": [
                "Perform a patch test before first use",
                "Discontinue use if irritation occurs",
                "Consult a dermatologist if you have concerns"
            ],
            "storage": "Store in a cool, dry place away from direct sunlight"
        }
    
    def _generate_pricing_section(self, product: Any) -> Dict[str, Any]:
        """Generate pricing section"""
        return {
            "title": "Pricing",
            "price": product.price,
            "value_proposition": f"Premium {product.concentration} serum at an accessible price point",
            "includes": "Full-size 30ml bottle"
        }
