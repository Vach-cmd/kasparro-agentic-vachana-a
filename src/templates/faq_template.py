"""
FAQ Page Template
"""
from typing import Dict, Any, List
from .base_template import Template
from ..models.product import Question


class FAQTemplate(Template):
    """
    Template for FAQ page generation.
    Defines structure for question-answer pairs with categorization.
    """
    
    def __init__(self):
        super().__init__("FAQTemplate")
    
    def get_schema(self) -> Dict[str, Any]:
        """Get FAQ template schema"""
        return {
            "type": "FAQ",
            "fields": {
                "title": {"type": "string", "required": True},
                "product_name": {"type": "string", "required": True},
                "questions": {
                    "type": "array",
                    "required": True,
                    "min_items": 5,
                    "items": {
                        "category": {"type": "string", "required": True},
                        "question": {"type": "string", "required": True},
                        "answer": {"type": "string", "required": True}
                    }
                },
                "metadata": {
                    "type": "object",
                    "required": True,
                    "fields": {
                        "total_questions": {"type": "integer"},
                        "categories": {"type": "array"},
                        "generated_at": {"type": "string"}
                    }
                }
            },
            "rules": {
                "min_questions": 5,
                "max_questions_per_category": 5,
                "answer_min_length": 10
            }
        }
    
    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render FAQ page from questions.
        
        Args:
            data: Dict with 'product' and 'questions' keys
            
        Returns:
            Rendered FAQ page
        """
        product = data['product']
        questions = data['questions']
        
        # Select top questions for FAQ (at least 5)
        selected_questions = self._select_questions_for_faq(questions, min_count=5)
        
        # Format questions
        formatted_questions = [
            {
                "category": q.category,
                "question": q.question,
                "answer": q.answer
            }
            for q in selected_questions
        ]
        
        # Generate metadata
        categories = list(set(q.category for q in selected_questions))
        
        import datetime
        metadata = {
            "total_questions": len(formatted_questions),
            "categories": categories,
            "generated_at": datetime.datetime.now().isoformat(),
            "template": self.name,
            "version": "1.0"
        }
        
        return {
            "title": f"Frequently Asked Questions - {product.product_name}",
            "product_name": product.product_name,
            "questions": formatted_questions,
            "metadata": metadata
        }
    
    def _select_questions_for_faq(self, questions: List[Question], min_count: int = 5) -> List[Question]:
        """
        Select diverse questions for FAQ page.
        Ensures representation from multiple categories.
        """
        # Group by category
        by_category = {}
        for q in questions:
            if q.category not in by_category:
                by_category[q.category] = []
            by_category[q.category].append(q)
        
        # Select questions ensuring diversity
        selected = []
        categories = list(by_category.keys())
        
        # Round-robin selection from categories
        while len(selected) < len(questions) and len(selected) < min_count * 2:
            for cat in categories:
                if by_category[cat]:
                    selected.append(by_category[cat].pop(0))
                if len(selected) >= len(questions):
                    break
        
        return selected[:max(min_count, len(selected))]
