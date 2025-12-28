import json
import sys
import os
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.orchestrator_agent import OrchestratorAgent
from src.config import Config
from src.exceptions import ContentGenerationError


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Multi-Agent Content Generation System'
    )
    parser.add_argument(
        '--input',
        type=str,
        default=str(Config.PRODUCT_DATA_FILE),
        help='Path to product data JSON file'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=str(Config.OUTPUT_DIR),
        help='Output directory for generated files'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show performance statistics'
    )
    
    return parser.parse_args()


def load_product_data(filepath: str) -> dict:
    """
    Load and validate product data from JSON file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        dict: Product data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"Product data file not found: {filepath}")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Basic validation
        required_fields = ['product_name', 'concentration', 'skin_type']
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        
        return data
        
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in {filepath}: {str(e)}", 
            e.doc, 
            e.pos
        )


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("Multi-Agent Content Generation System")
    print("=" * 60)
    print()


def print_stats(orchestrator):
    """Print performance statistics"""
    print("\n" + "=" * 60)
    print("Performance Statistics")
    print("=" * 60)
    
    agents = [
        orchestrator.data_parser,
        orchestrator.question_generator,
        orchestrator.faq_generator,
        orchestrator.product_page_generator,
        orchestrator.comparison_generator
    ]
    
    for agent in agents:
        stats = agent.get_stats()
        print(f"{stats['name']:.<30} {stats['executions']} exec(s), {stats['average_time']:.3f}s avg")
    
    print("=" * 60)


def main():
    """Main execution function"""
    args = parse_arguments()
    
    try:
        print_banner()
        
        # Load product data
        print(f"Loading product data from: {args.input}")
        product_data = load_product_data(args.input)
        print(f"✓ Loaded: {product_data.get('product_name', 'Unknown Product')}")
        print()
        
        # Initialize orchestrator
        orchestrator = OrchestratorAgent()
        
        # Execute pipeline
        print("Starting content generation pipeline...")
        results = orchestrator.execute(product_data)
        
        # Save outputs
        print()
        print("Saving outputs...")
        orchestrator.save_outputs(results, args.output_dir)
        
        # Success summary
        print()
        print("=" * 60)
        print("✓ Content Generation Complete!")
        print("=" * 60)
        print(f"Generated {results['metadata']['pages_generated']} pages")
        print(f"Total questions: {results['metadata']['total_questions_generated']}")
        print()
        print("Output files:")
        print(f"  - {os.path.join(args.output_dir, 'faq.json')}")
        print(f"  - {os.path.join(args.output_dir, 'product_page.json')}")
        print(f"  - {os.path.join(args.output_dir, 'comparison_page.json')}")
        
        # Show stats if requested
        if args.stats:
            print_stats(orchestrator)
        
        print()
        return 0
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1
    
    except json.JSONDecodeError as e:
        print(f"\n✗ JSON Error: {e}", file=sys.stderr)
        return 1
    
    except ContentGenerationError as e:
        print(f"\n✗ Generation Error: {e}", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
