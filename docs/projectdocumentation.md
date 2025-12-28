# Project Documentation

## Problem Statement

The challenge is to design and implement a **modular agentic automation system** that transforms raw product data into multiple structured, machine-readable content pages. This system must demonstrate:

- Multi-agent workflow architecture with clear agent boundaries
- Template-based content generation with reusable logic blocks
- Automated question generation and categorization
- Structured JSON output for all generated pages

The system must operate on limited product data without external research or domain expertise, focusing purely on engineering design and automation capabilities.

## Solution Overview

This project implements a **production-grade multi-agent content generation system** using a **DAG-based orchestration pattern**. The system processes product data through a pipeline of specialized agents, each with a single well-defined responsibility.

### Key Innovations

1. **Clear Agent Separation**: Each agent has a single responsibility with defined input/output contracts
2. **Reusable Content Blocks**: Logic blocks that can be composed across different templates
3. **Template Engine**: Custom-built template system with schema validation and content block dependencies
4. **Orchestrated Workflow**: DAG-based pipeline with parallel execution support
5. **Type Safety**: Pydantic models for data validation throughout the pipeline

## Scopes & Assumptions

### In Scope
- ✅ Parsing and validating product data
- ✅ Generating 15+ categorized questions across 7 categories
- ✅ Creating 3 distinct page types (FAQ, Product, Comparison)
- ✅ Implementing reusable content logic blocks
- ✅ Custom template engine with schema definitions
- ✅ Machine-readable JSON output
- ✅ Multi-agent orchestration with clear workflow

### Out of Scope
- ❌ External API calls or research
- ❌ LLM/GPT integration (pure logic-based generation)
- ❌ UI/frontend implementation
- ❌ Database persistence
- ❌ Real-time processing or web server

### Assumptions
- Input data follows the specified product data schema
- Single product processing per execution
- File-based output (JSON files)
- Python 3.8+ runtime environment

## System Design

### Architecture Overview

The system implements a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                   Orchestrator Layer                     │
│              (DAG-based Workflow Control)                │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐   ┌──────────────┐
│ FAQ Generator│    │Product Page  │   │  Comparison  │
│    Agent     │    │   Generator  │   │   Generator  │
└──────────────┘    └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                ┌──────────────────────┐
                │   Template Layer     │
                │  (Schema + Rendering)│
                └──────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │Benefits     │ │Usage        │ │Comparison   │
    │Block        │ │Block        │ │Block        │
    └─────────────┘ └─────────────┘ └─────────────┘
                            │
                            ▼
                ┌──────────────────────┐
                │     Data Layer       │
                │  (Pydantic Models)   │
                └──────────────────────┘
```

### Agent Architecture

#### 1. **OrchestratorAgent** (Master Agent)
- **Responsibility**: Coordinates entire workflow, manages agent dependencies
- **Input**: Raw product data (Dict)
- **Output**: Complete generated content package (Dict)
- **Pattern**: DAG-based orchestration with parallel execution

**Workflow Stages**:
```
Stage 1: Data Parsing              [DataParserAgent]
         ↓
Stage 2: Question Generation       [QuestionGeneratorAgent]
         ↓
Stage 3: Parallel Page Generation
         ├→ FAQ Page                [FAQGeneratorAgent]
         ├→ Product Page            [ProductPageGeneratorAgent]
         └→ Comparison Page         [ComparisonGeneratorAgent]
         ↓
Stage 4: Output Collection & Persistence
```

#### 2. **DataParserAgent**
- **Responsibility**: Parse and validate raw product data
- **Input**: Dict[str, Any] - Raw product data
- **Output**: Product model (validated)
- **Validation**: Uses Pydantic for schema validation

#### 3. **QuestionGeneratorAgent**
- **Responsibility**: Generate categorized user questions
- **Input**: Product model
- **Output**: List[Question] - 15+ questions across 7 categories
- **Categories**:
  - Informational (3 questions)
  - Safety (2 questions)
  - Usage (3 questions)
  - Purchase (2 questions)
  - Comparison (1 question)
  - Ingredients (2 questions)
  - Benefits (2 questions)

#### 4. **FAQGeneratorAgent**
- **Responsibility**: Generate FAQ page from questions
- **Input**: Dict with 'product' and 'questions'
- **Output**: Rendered FAQ page (Dict)
- **Template**: FAQTemplate

#### 5. **ProductPageGeneratorAgent**
- **Responsibility**: Generate product description page
- **Input**: Product model
- **Output**: Rendered product page (Dict)
- **Template**: ProductPageTemplate
- **Content Blocks**: BenefitsBlock, UsageBlock, IngredientsBlock

#### 6. **ComparisonGeneratorAgent**
- **Responsibility**: Generate product comparison page
- **Input**: Product model
- **Output**: Rendered comparison page (Dict)
- **Template**: ComparisonTemplate
- **Content Blocks**: ComparisonBlock
- **Special**: Creates fictional Product B for comparison

### Content Block System

Content blocks are **reusable transformation units** that apply domain-specific rules to convert product data into structured content.

#### **BenefitsBlock**
- Transforms product benefits into enriched benefit descriptions
- Adds benefit categorization and iconography
- Generates benefit summaries

#### **UsageBlock**
- Parses usage text into step-by-step instructions
- Extracts frequency and timing information
- Generates usage tips and best practices

#### **IngredientsBlock**
- Enriches ingredient lists with scientific names
- Adds ingredient descriptions and benefits
- Determines formula type classification

#### **ComparisonBlock**
- Generates multi-dimensional comparison matrices
- Compares products across 5 criteria:
  - Vitamin C concentration
  - Key ingredients
  - Skin type compatibility
  - Primary benefits
  - Price/value
- Determines overall winner with reasoning

### Template Engine

Templates define the **structure, schema, and rendering rules** for output pages.

#### Template Interface
Each template must implement:
- `get_schema()`: Returns schema definition with fields, types, and rules
- `render(data)`: Renders content using content blocks and data

#### FAQTemplate
- **Schema**: title, product_name, questions[], metadata
- **Rules**: Min 5 questions, diverse category representation
- **Logic**: Round-robin category selection for diversity

#### ProductPageTemplate
- **Schema**: 9 major sections (hero, features, ingredients, benefits, usage, safety, pricing, metadata)
- **Content Blocks**: Composes BenefitsBlock, UsageBlock, IngredientsBlock
- **Dependencies**: Requires all 3 content blocks for complete rendering

#### ComparisonTemplate
- **Schema**: title, product_a, product_b, comparison_matrix[], recommendation
- **Content Blocks**: Uses ComparisonBlock for matrix generation
- **Logic**: Determines winner and generates recommendation

### Data Models

All data structures use **Pydantic** for validation and type safety:

```python
Product          # Core product data model
Question         # Question with category  and answer
FAQ              # Complete FAQ page structure
ProductPage      # Complete product page structure
ComparisonPage   # Complete comparison page structure
```

### Workflow Execution Flow

```
1. Load product_data.json
   ↓
2. OrchestratorAgent.execute(data)
   ↓
3. DataParserAgent validates → Product model
   ↓
4. QuestionGeneratorAgent generates → 15+ Questions
   ↓
5. Parallel execution:
   ├─ FAQGeneratorAgent → faq.json
   ├─ ProductPageGeneratorAgent → product_page.json
   └─ ComparisonGeneratorAgent → comparison_page.json
   ↓
6. Save JSON outputs to /output directory
```

### Design Patterns Used

1. **Abstract Factory Pattern**: BaseAgent, ContentBlock, Template
2. **Template Method Pattern**: Template rendering with content blocks
3. **Strategy Pattern**: Content blocks as interchangeable strategies
4. **Orchestrator Pattern**: Central coordination of agent workflow
5. **Dependency Injection**: Templates receive content blocks

### Extensibility Points

The system is designed for easy extension:

1. **New Agents**: Extend BaseAgent, implement execute()
2. **New Content Blocks**: Extend ContentBlock, implement generate()
3. **New Templates**: Extend Template, implement get_schema() and render()
4. **New Question Categories**: Add to QuestionGeneratorAgent.CATEGORIES
5. **New Output Formats**: Add serialization logic to OrchestratorAgent

### Quality Attributes

- **Modularity**: Clear separation between agents, blocks, and templates
- **Reusability**: Content blocks used across multiple templates
- **Testability**: Each component has defined input/output contracts
- **Maintainability**: Single Responsibility Principle throughout
- **Type Safety**: Pydantic models enforce contracts
- **Extensibility**: Open-Closed Principle for new agents/blocks/templates

---

**System Version**: 1.0  
**Architecture Pattern**: Multi-Agent DAG-based Orchestration  
**Language**: Python 3.8+  
**Dependencies**: Pydantic, typing-extensions
