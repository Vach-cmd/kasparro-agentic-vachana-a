# Quick Start Guide

## Getting Started in 3 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the System
```bash
python src/main.py
```

### 3. View Generated Output
Check the `output/` directory for three JSON files:
- `faq.json` - Frequently Asked Questions page
- `product_page.json` - Complete product description
- `comparison_page.json` - Product comparison analysis

---

## What Happens When You Run?

The system executes a **4-stage pipeline**:

### Stage 1: Data Parsing
- Loads `data/product_data.json`
- Validates using Pydantic models
- Creates structured Product object

### Stage 2: Question Generation
- Generates 15+ questions across 7 categories:
  - Informational (product details)
  - Safety (side effects, precautions)
  - Usage (how to use)
  - Purchase (pricing, value)
  - Comparison (vs other products)
  - Ingredients (what's inside)
  - Benefits (what it does)

### Stage 3: Page Generation (Parallel)
Three agents work simultaneously:
- **FAQGeneratorAgent** → Creates FAQ page
- **ProductPageGeneratorAgent** → Creates product description
- **ComparisonGeneratorAgent** → Creates comparison page

### Stage 4: Output Persistence
- Saves all pages as JSON files
- Includes metadata for each page
- Ready for consumption by frontend/API

---

## Understanding the Output

### FAQ Page Structure
```json
{
  "title": "Frequently Asked Questions - ...",
  "product_name": "...",
  "questions": [
    {
      "category": "Informational",
      "question": "What is ...?",
      "answer": "..."
    }
  ],
  "metadata": { ... }
}
```

### Product Page Structure
Contains 9 sections:
1. Hero (tagline, description)
2. Key Features (highlighted features)
3. Ingredients (detailed ingredient info)
4. Benefits (what it does)
5. Usage (how to use)
6. Safety (precautions)
7. Pricing (cost and value)
8. Metadata (generation info)

### Comparison Page Structure
```json
{
  "title": "Product A vs Product B",
  "product_a": { ... },
  "product_b": { ... },
  "comparison_matrix": [
    {
      "criterion": "...",
      "product_a_value": "...",
      "product_b_value": "...",
      "winner": "product_a|product_b|tie"
    }
  ],
  "recommendation": { ... }
}
```

---

## Running Tests

Validate the entire system:

```bash
python tests/test_system.py
```

This tests:
- ✓ Data parsing and validation
- ✓ Question generation (15+ questions)
- ✓ Content blocks (4 blocks)
- ✓ Templates (3 templates)
- ✓ Full pipeline execution

---

## Customization

### Add Your Own Product

Edit `data/product_data.json`:

```json
{
  "product_name": "Your Product Name",
  "concentration": "Active ingredient %",
  "skin_type": ["Type1", "Type2"],
  "key_ingredients": ["Ingredient1", "Ingredient2"],
  "benefits": ["Benefit1", "Benefit2"],
  "how_to_use": "Usage instructions",
  "side_effects": "Any side effects",
  "price": "₹XXX"
}
```

Then run:
```bash
python src/main.py
```

---

## Project Structure

```
kasparro-agentic-vachana-a/
│
├── data/                    # Input data
│   └── product_data.json
│
├── src/                     # Source code
│   ├── agents/             # Agent implementations
│   ├── content_blocks/     # Reusable content logic
│   ├── templates/          # Output templates
│   ├── models/             # Data models
│   └── main.py             # Entry point
│
├── output/                  # Generated JSON files
│   ├── faq.json
│   ├── product_page.json
│   └── comparison_page.json
│
├── tests/                   # Test suite
│   └── test_system.py
│
└── docs/                    # Documentation
    └── projectdocumentation.md
```

---

## Need Help?

1. **Read the Documentation**: `docs/projectdocumentation.md`
2. **Check the README**: `README.md`
3. **Review the Code**: All files are well-documented
4. **Run Tests**: `python tests/test_system.py`

---

## What's Next?

This system is designed to be **extensible**:

- **Add new agents**: Create new agent classes
- **Add content blocks**: Create reusable transformations
- **Add templates**: Define new output formats
- **Add question categories**: Extend question generation

See the main documentation for detailed extension guides.

---

**Enjoy generating content with AI agents! 🚀**
