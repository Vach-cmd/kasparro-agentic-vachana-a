"""
OrchestratorAgent: Coordinates the entire workflow
"""
import json
from typing import Dict, Any
from .base_agent import BaseAgent
from .data_parser_agent import DataParserAgent
from .question_generator_agent import QuestionGeneratorAgent
from .faq_generator_agent import FAQGeneratorAgent
from .product_page_generator_agent import ProductPageGeneratorAgent
from .comparison_generator_agent import ComparisonGeneratorAgent


class OrchestratorAgent(BaseAgent):
    """
    Master agent that orchestrates the entire content generation pipeline.
    Implements a DAG-based workflow for agent coordination.
    
    Workflow:
    1. DataParserAgent: Parse raw data
    2. QuestionGeneratorAgent: Generate questions (depends on 1)
    3. Parallel execution:
       - FAQGeneratorAgent: Generate FAQ (depends on 1, 2)
       - ProductPageGeneratorAgent: Generate product page (depends on 1)
       - ComparisonGeneratorAgent: Generate comparison (depends on 1)
    4. Collect and save outputs
    """
    
    def __init__(self):
        super().__init__("OrchestratorAgent")
        
        # Initialize worker agents
        self.data_parser = DataParserAgent()
        self.question_generator = QuestionGeneratorAgent()
        self.faq_generator = FAQGeneratorAgent()
        self.product_page_generator = ProductPageGeneratorAgent()
        self.comparison_generator = ComparisonGeneratorAgent()
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete content generation pipeline.
        
        Args:
            input_data: Raw product data
            
        Returns:
            Dict with all generated outputs
        """
        self.log("Starting content generation pipeline...")
        
        # Stage 1: Parse product data
        self.log("Stage 1: Data Parsing")
        product = self.data_parser.execute(input_data)
        
        # Stage 2: Generate questions
        self.log("Stage 2: Question Generation")
        questions = self.question_generator.execute(product)
        
        # Stage 3: Parallel page generation
        self.log("Stage 3: Page Generation (Parallel)")
        
        self.log("  -> Generating FAQ page...")
        faq_page = self.faq_generator.execute({
            'product': product,
            'questions': questions
        })
        
        self.log("  -> Generating product page...")
        product_page = self.product_page_generator.execute(product)
        
        self.log("  -> Generating comparison page...")
        comparison_page = self.comparison_generator.execute(product)
        
        # Collect results
        results = {
            'faq': faq_page,
            'product_page': product_page,
            'comparison': comparison_page,
            'metadata': {
                'total_questions_generated': len(questions),
                'pages_generated': 3,
                'pipeline_status': 'success'
            }
        }
        
        self.log("Pipeline completed successfully")
        
        return results
    
    def save_outputs(self, results: Dict[str, Any], output_dir: str = "output") -> None:
        """
        Save generated pages as JSON files.
        
        Args:
            results: Generated content results
            output_dir: Output directory path
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save each page
        pages = {
            'faq.json': results['faq'],
            'product_page.json': results['product_page'],
            'comparison_page.json': results['comparison']
        }
        
        for filename, content in pages.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            self.log(f"Saved {filepath}")
