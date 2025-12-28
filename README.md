# Multi-Agent Content Generation System

A production-grade modular system for automated content generation using multi-agent architecture.

## Overview

This system transforms raw product data into structured, machine-readable content pages through a coordinated pipeline of specialized agents. Built with extensibility and maintainability in mind, it demonstrates production-level software engineering practices.

## Features

- **Multi-Agent Architecture**: 6 specialized agents with clear responsibilities
- **DAG-Based Orchestration**: Coordinated workflow with dependency management
- **Reusable Components**: 4 content blocks that can be composed across templates
- **Custom Template Engine**: Schema-driven rendering with validation
- **Type Safety**: Pydantic models ensure data integrity
- **CLI Support**: Command-line interface with multiple options
- **Error Handling**: Robust error handling with retry logic
- **Performance Tracking**: Built-in execution statistics

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```bash
python src/main.py
```

### Advanced Usage

```bash
# Custom input file
python src/main.py --input data/my_product.json

# Custom output directory
python src/main.py --output-dir custom_output/

# Show performance statistics
python src/main.py --stats

# Verbose error messages
python src/main.py --verbose

# Combine options
python src/main.py --input custom.json --output-dir results/ --stats
```

## System Architecture

### Agents

| Agent | Purpose |
|-------|---------|
| **OrchestratorAgent** | Coordinates entire workflow |
| **DataParserAgent** | Validates and parses input data |
| **QuestionGeneratorAgent** | Creates categorized questions |
| **FAQGeneratorAgent** | Assembles FAQ pages |
| **ProductPageGeneratorAgent** | Builds product descriptions |
| **ComparisonGeneratorAgent** | Generates product comparisons |

### Content Blocks

- **BenefitsBlock**: Transforms benefits into detailed descriptions
- **UsageBlock**: Creates step-by-step usage instructions
- **IngredientsBlock**: Enriches ingredient data with scientific information
- **ComparisonBlock**: Generates multi-criteria comparison matrices

### Templates

- **FAQTemplate**: Structures Q&A content
- **ProductPageTemplate**: Composes comprehensive product pages
- **ComparisonTemplate**: Formats product comparisons

## Project Structure

```
kasparro-agentic-vachana-a/
├── src/
│   ├── agents/          # Agent implementations
│   ├── content_blocks/  # Reusable content logic
│   ├── templates/       # Output templates
│   ├── models/          # Data models
│   ├── config.py        # Configuration
│   ├── exceptions.py    # Custom exceptions
│   ├── utils.py         # Utility functions
│   └── main.py          # Entry point
├── data/                # Input data
├── output/              # Generated files
├── tests/               # Test suite
└── docs/                # Documentation
```

## Generated Output

The system generates three JSON files:

1. **faq.json**: FAQ page with categorized questions
2. **product_page.json**: Complete product description
3. **comparison_page.json**: Product comparison analysis

## Configuration

Edit `src/config.py` to customize:

- Input/output paths
- Question categories
- Minimum question counts
- Validation settings

## Error Handling

The system includes:

- Input validation with detailed error messages
- Retry logic for robustness
- Custom exception types
- Graceful degradation

## Performance

View execution statistics with the `--stats` flag:

```bash
python src/main.py --stats
```

## Testing

Run the test suite:

```bash
python tests/test_system.py
```

## Documentation

- `README.md`: This file
- `docs/projectdocumentation.md`: Detailed system design
- `QUICKSTART.md`: Getting started guide
- `PROJECT_SUMMARY.md`: Project achievements

## Requirements

- Python 3.8+
- Pydantic 2.10.4
- typing-extensions 4.12.2


