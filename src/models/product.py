from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator


class Product(BaseModel):
    """
    Core product data model with validation.
    Represents a skincare product with all essential attributes.
    """
    product_name: str = Field(..., min_length=1, max_length=200, description="Product name")
    concentration: str = Field(..., min_length=1, description="Active ingredient concentration")
    skin_type: List[str] = Field(..., min_items=1, description="Compatible skin types")
    key_ingredients: List[str] = Field(..., min_items=1, description="Key active ingredients")
    benefits: List[str] = Field(..., min_items=1, description="Product benefits")
    how_to_use: str = Field(..., min_length=5, description="Usage instructions")
    side_effects: str = Field(..., description="Potential side effects")
    price: str = Field(..., description="Product price")
    
    @validator('product_name')
    def validate_product_name(cls, v):
        if not v.strip():
            raise ValueError('Product name cannot be empty or whitespace')
        return v.strip()
    
    @validator('skin_type', 'key_ingredients', 'benefits')
    def validate_lists_not_empty(cls, v):
        if not v:
            raise ValueError('List cannot be empty')
        return [item.strip() for item in v if item.strip()]
    
    class Config:
        frozen = False
        str_strip_whitespace = True


class Question(BaseModel):
    """Represents a single Q&A pair with category"""
    category: str = Field(..., min_length=1, description="Question category")
    question: str = Field(..., min_length=2, description="Question text")
    answer: str = Field(..., min_length=2, description="Answer text")
    
    @validator('question', 'answer')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()


class FAQ(BaseModel):
    """FAQ page output structure"""
    title: str = Field(..., min_length=1)
    product_name: str = Field(..., min_length=1)
    questions: List[Question] = Field(..., min_items=1)
    metadata: Dict[str, Any]


class ProductPage(BaseModel):
    """Product description page output structure"""
    product_name: str
    tagline: str
    hero_description: str
    key_features: List[Dict[str, Any]]
    ingredients_section: Dict[str, Any]
    benefits_section: Dict[str, Any]
    usage_section: Dict[str, Any]
    safety_section: Dict[str, Any]
    pricing_section: Dict[str, Any]
    metadata: Dict[str, Any]


class ComparisonPage(BaseModel):
    """Product comparison page output structure"""
    title: str
    product_a: Dict[str, Any]
    product_b: Dict[str, Any]
    comparison_matrix: List[Dict[str, Any]]
    recommendation: Dict[str, Any]
    metadata: Dict[str, Any]
