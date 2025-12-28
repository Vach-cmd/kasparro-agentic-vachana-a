"""
QuestionGeneratorAgent: Generates categorized user questions
"""
from typing import List, Dict
from .base_agent import BaseAgent
from ..models.product import Product, Question


class QuestionGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating categorized user questions based on product data.
    
    Input: Product - Validated product model
    Output: List[Question] - List of categorized questions with answers
    """
    
    CATEGORIES = [
        "Informational",
        "Safety", 
        "Usage",
        "Purchase",
        "Comparison",
        "Ingredients",
        "Benefits"
    ]
    
    def __init__(self):
        super().__init__("QuestionGeneratorAgent")
    
    def execute(self, input_data: Product) -> List[Question]:
        """
        Generate categorized questions based on product data.
        
        Args:
            input_data: Product model
            
        Returns:
            List[Question]: List of questions with categories and answers
        """
        self.log("Generating categorized questions...")
        
        questions = []
        
        # Informational questions
        questions.extend(self._generate_informational_questions(input_data))
        
        # Safety questions
        questions.extend(self._generate_safety_questions(input_data))
        
        # Usage questions
        questions.extend(self._generate_usage_questions(input_data))
        
        # Purchase questions
        questions.extend(self._generate_purchase_questions(input_data))
        
        # Comparison questions
        questions.extend(self._generate_comparison_questions(input_data))
        
        # Ingredients questions
        questions.extend(self._generate_ingredients_questions(input_data))
        
        # Benefits questions
        questions.extend(self._generate_benefits_questions(input_data))
        
        self.log(f"Generated {len(questions)} questions across {len(self.CATEGORIES)} categories")
        
        return questions
    
    def _generate_informational_questions(self, product: Product) -> List[Question]:
        """Generate informational questions"""
        return [
            Question(
                category="Informational",
                question=f"What is {product.product_name}?",
                answer=f"{product.product_name} is a skincare serum with {product.concentration}, designed for {' and '.join(product.skin_type)} skin types."
            ),
            Question(
                category="Informational",
                question="What concentration of Vitamin C does this serum contain?",
                answer=f"This serum contains {product.concentration}."
            ),
            Question(
                category="Informational",
                question="Which skin types is this product suitable for?",
                answer=f"This product is suitable for {' and '.join(product.skin_type)} skin types."
            )
        ]
    
    def _generate_safety_questions(self, product: Product) -> List[Question]:
        """Generate safety questions"""
        return [
            Question(
                category="Safety",
                question="Are there any side effects?",
                answer=f"{product.side_effects}."
            ),
            Question(
                category="Safety",
                question="Can I use this if I have sensitive skin?",
                answer=f"Users with sensitive skin may experience {product.side_effects.lower()}. It's recommended to perform a patch test first."
            )
        ]
    
    def _generate_usage_questions(self, product: Product) -> List[Question]:
        """Generate usage questions"""
        return [
            Question(
                category="Usage",
                question="How do I use this serum?",
                answer=product.how_to_use
            ),
            Question(
                category="Usage",
                question="When should I apply this serum in my routine?",
                answer="Apply in the morning before sunscreen, after cleansing and toning."
            ),
            Question(
                category="Usage",
                question="How many drops should I use?",
                answer="Use 2-3 drops for optimal results."
            )
        ]
    
    def _generate_purchase_questions(self, product: Product) -> List[Question]:
        """Generate purchase questions"""
        return [
            Question(
                category="Purchase",
                question="What is the price of this serum?",
                answer=f"The {product.product_name} is priced at {product.price}."
            ),
            Question(
                category="Purchase",
                question="Is this product worth the investment?",
                answer=f"At {product.price}, this serum offers {', '.join(product.benefits).lower()} benefits with quality ingredients like {' and '.join(product.key_ingredients)}."
            )
        ]
    
    def _generate_comparison_questions(self, product: Product) -> List[Question]:
        """Generate comparison questions"""
        return [
            Question(
                category="Comparison",
                question="How does this compare to other Vitamin C serums?",
                answer=f"This serum stands out with its {product.concentration} formulation combined with {' and '.join(product.key_ingredients)}."
            )
        ]
    
    def _generate_ingredients_questions(self, product: Product) -> List[Question]:
        """Generate ingredients questions"""
        return [
            Question(
                category="Ingredients",
                question="What are the key ingredients?",
                answer=f"The key ingredients are {' and '.join(product.key_ingredients)}."
            ),
            Question(
                category="Ingredients",
                question="What does Hyaluronic Acid do in this formula?",
                answer="Hyaluronic Acid provides hydration and helps the skin retain moisture."
            )
        ]
    
    def _generate_benefits_questions(self, product: Product) -> List[Question]:
        """Generate benefits questions"""
        return [
            Question(
                category="Benefits",
                question="What are the main benefits of this serum?",
                answer=f"The main benefits include {' and '.join(product.benefits).lower()}."
            ),
            Question(
                category="Benefits",
                question="How long until I see results?",
                answer="With consistent use, you may start seeing brightening effects within 2-4 weeks."
            )
        ]
