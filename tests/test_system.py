"""
Test script to validate the multi-agent system
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import json
from src.agents import (
    DataParserAgent, 
    QuestionGeneratorAgent,
    FAQGeneratorAgent,
    ProductPageGeneratorAgent,
    ComparisonGeneratorAgent,
    OrchestratorAgent
)


def test_data_parser():
    """Test DataParserAgent"""
    print("Testing DataParserAgent...")
    agent = DataParserAgent()
    
    test_data = {
        "product_name": "Test Product",
        "concentration": "10% Test",
        "skin_type": ["Oily"],
        "key_ingredients": ["Ingredient A"],
        "benefits": ["Benefit A"],
        "how_to_use": "Apply daily in the morning",
        "side_effects": "None",
        "price": "₹500"
    }
    
    product = agent.execute(test_data)
    assert product.product_name == "Test Product"
    print("✓ DataParserAgent passed")


def test_question_generator():
    """Test QuestionGeneratorAgent"""
    print("Testing QuestionGeneratorAgent...")
    from src.models import Product
    
    agent = QuestionGeneratorAgent()
    product = Product(
        product_name="Test Product",
        concentration="10% Test",
        skin_type=["Oily"],
        key_ingredients=["Ingredient A"],
        benefits=["Benefit A"],
        how_to_use="Apply daily in the morning",
        side_effects="None",
        price="₹500"
    )
    
    questions = agent.execute(product)
    assert len(questions) >= 15
    print(f"✓ QuestionGeneratorAgent passed ({len(questions)} questions generated)")


def test_content_blocks():
    """Test content blocks"""
    print("Testing Content Blocks...")
    from src.models import Product
    from src.content_blocks import BenefitsBlock, UsageBlock, IngredientsBlock
    
    product = Product(
        product_name="Test Product",
        concentration="10% Test",
        skin_type=["Oily"],
        key_ingredients=["Vitamin C"],
        benefits=["Brightening"],
        how_to_use="Apply daily in the morning",
        side_effects="None",
        price="₹500"
    )
    
    # Test BenefitsBlock
    benefits_block = BenefitsBlock()
    result = benefits_block.generate(product)
    assert "benefits" in result
    
    # Test UsageBlock
    usage_block = UsageBlock()
    result = usage_block.generate(product)
    assert "steps" in result
    
    # Test IngredientsBlock
    ingredients_block = IngredientsBlock()
    result = ingredients_block.generate(product)
    assert "ingredients" in result
    
    print("✓ Content Blocks passed")


def test_templates():
    """Test templates"""
    print("Testing Templates...")
    from src.models import Product, Question
    from src.templates import FAQTemplate, ProductPageTemplate
    
    product = Product(
        product_name="Test Product",
        concentration="10% Test",
        skin_type=["Oily"],
        key_ingredients=["Vitamin C"],
        benefits=["Brightening"],
        how_to_use="Apply daily in the morning",
        side_effects="None",
        price="₹500"
    )
    
    # Test FAQTemplate
    faq_template = FAQTemplate()
    questions = [
        Question(category="Test", question="Q1?", answer="A1"),
        Question(category="Test", question="Q2?", answer="A2"),
        Question(category="Test", question="Q3?", answer="A3"),
        Question(category="Test", question="Q4?", answer="A4"),
        Question(category="Test", question="Q5?", answer="A5"),
    ]
    result = faq_template.render({'product': product, 'questions': questions})
    assert "questions" in result
    
    # Test ProductPageTemplate
    product_template = ProductPageTemplate()
    result = product_template.render(product)
    assert "product_name" in result
    
    print("✓ Templates passed")


def test_full_pipeline():
    """Test full orchestration pipeline"""
    print("Testing Full Pipeline...")
    
    test_data = {
        "product_name": "Test Product",
        "concentration": "10% Test",
        "skin_type": ["Oily"],
        "key_ingredients": ["Vitamin C"],
        "benefits": ["Brightening"],
        "how_to_use": "Apply daily in the morning",
        "side_effects": "None",
        "price": "₹500"
    }
    
    orchestrator = OrchestratorAgent()
    results = orchestrator.execute(test_data)
    
    assert 'faq' in results
    assert 'product_page' in results
    assert 'comparison' in results
    assert results['metadata']['pages_generated'] == 3
    
    print("✓ Full Pipeline passed")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Multi-Agent System Validation Tests")
    print("=" * 60)
    print()
    
    try:
        test_data_parser()
        test_question_generator()
        test_content_blocks()
        test_templates()
        test_full_pipeline()
        
        print()
        print("=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("System is ready for production use.")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
