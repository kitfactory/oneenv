# OneEnv Scaffolding System User Guide

## Overview

The OneEnv Scaffolding System is a powerful feature that helps developers automatically discover, organize, and generate environment configuration files from installed packages. Instead of manually creating `.env` files, the system intelligently structures templates by categories and options, making environment management more intuitive and scalable.

### What is Scaffolding?

**Scaffolding** in OneEnv refers to the automated process of:
- **Discovering** environment variable templates from installed packages
- **Organizing** them by categories (Database, VectorStore, LLM, etc.)
- **Providing** structured information for custom tool creation
- **Generating** tailored `.env` files based on user selections

### Key Benefits

✅ **Intelligent Organization**: Templates are grouped by technology categories  
✅ **Selective Generation**: Generate only the configurations you need  
✅ **Importance Hierarchy**: Variables are classified as Critical/Important/Optional  
✅ **Tool-Friendly**: APIs designed for creating custom scaffolding tools  
✅ **Extensible**: Easy to add new templates and categories  

### When to Use Scaffolding

- **New Project Setup**: Quickly configure environment variables for new projects
- **Multi-Service Applications**: Manage configurations for complex systems (RAG, microservices)
- **Tool Development**: Create custom setup wizards for your packages
- **Team Standardization**: Ensure consistent environment configurations across teams

## Basic Usage

### 1. Exploring Available Templates

#### View All Categories and Options
```bash
oneenv template --structure
```

**Output:**
```
Available template structure:
┌─────────────────┬─────────────────────────────────────┐
│ Category        │ Options                             │
├─────────────────┼─────────────────────────────────────┤
│ Database        │ postgres, sqlite, mysql             │
│ VectorStore     │ chroma, pinecone, weaviate          │
│ LLM             │ openai, anthropic, local            │
│ Cache           │ redis, memcached                    │
│ Monitoring      │ basic, advanced                     │
└─────────────────┴─────────────────────────────────────┘
```

#### Get Detailed Category Information
```bash
oneenv template --info Database
```

**Output:**
```
Database Category Information:
- Available options: postgres, sqlite, mysql
- Total variables: 8
- Critical variables: 3
- Important variables: 3
- Optional variables: 2

Description: Database connection and configuration templates
Common use cases: Web applications, data processing, analytics
```

#### Preview Specific Options
```bash
oneenv template --preview Database postgres
```

**Output:**
```
Preview: Database → postgres
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PostgreSQL connection URL
# Required | Critical
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# Connection pool size
# Optional | Important
DATABASE_POOL_SIZE=10

# SSL mode for connections
# Optional | Optional
# Choices: require, prefer, disable
DATABASE_SSL_MODE=prefer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. Understanding Template Structure

Templates are organized in a hierarchical structure:

```
Category (e.g., "Database")
├── Option (e.g., "postgres")
│   ├── Variable 1 (e.g., "DATABASE_URL")
│   ├── Variable 2 (e.g., "DATABASE_POOL_SIZE")
│   └── Variable 3 (e.g., "DATABASE_SSL_MODE")
├── Option (e.g., "sqlite")
│   ├── Variable 1 (e.g., "DATABASE_URL")
│   └── Variable 2 (e.g., "DATABASE_TIMEOUT")
└── Option (e.g., "mysql")
    ├── Variable 1 (e.g., "DATABASE_URL")
    └── Variable 2 (e.g., "DATABASE_CHARSET")
```

### 3. Basic Template Generation

#### Using the Standard Template Command
```bash
oneenv template
```

This generates a `.env.example` file with all available templates, organized by importance:

```env
# ========== CRITICAL: Essential Settings for Application Operation ==========

# ----- Database -----
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# ----- LLM -----
OPENAI_API_KEY=

# ========== IMPORTANT: Settings to Configure for Production Use ==========

# ----- Cache -----
REDIS_URL=redis://localhost:6379/0

# ========== OPTIONAL: Fine-tuning Settings (Defaults are Sufficient) ==========

# ----- Monitoring -----
LOG_LEVEL=INFO
```

## Advanced Usage

### 1. Programmatic API Usage

#### Basic Information Retrieval
```python
import oneenv

# Get all available structure
structure = oneenv.get_all_template_structure()
print(structure)
# Output: {'Database': ['postgres', 'sqlite'], 'VectorStore': ['chroma', 'pinecone']}

# Check if a category exists
if oneenv.has_category("Database"):
    print("Database templates are available")

# Get options for a specific category
options = oneenv.get_options("Database")
print(f"Database options: {options}")
# Output: ['postgres', 'sqlite', 'mysql']
```

#### Selective Template Generation
```python
# Define your selections
selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM", "option": "openai"}
]

# Generate template with only selected options
content = oneenv.generate_template(".env.example", selections)
print("Generated template for selected options")
```

### 2. Creating Custom Scaffolding Tools

#### Simple CLI Tool
```python
#!/usr/bin/env python3
"""Custom scaffolding tool example"""

import oneenv
import argparse

def list_available():
    """List all available templates"""
    structure = oneenv.get_all_template_structure()
    
    print("🔍 Available Templates:")
    for category, options in structure.items():
        print(f"\n📁 {category}:")
        for option in options:
            print(f"   • {option}")

def generate_custom(selections):
    """Generate custom template"""
    try:
        content = oneenv.generate_template(".env.custom", selections)
        print("✅ Custom template generated successfully!")
        print(f"📁 File: .env.custom")
        
        print("\n📋 Selected configuration:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Custom OneEnv Scaffolding Tool")
    parser.add_argument("--list", action="store_true", help="List available templates")
    parser.add_argument("--generate", nargs="+", help="Generate template (format: Category:Option)")
    
    args = parser.parse_args()
    
    if args.list:
        list_available()
    elif args.generate:
        selections = []
        for item in args.generate:
            category, option = item.split(":")
            selections.append({"category": category, "option": option})
        generate_custom(selections)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python custom_scaffold.py --list
python custom_scaffold.py --generate Database:postgres VectorStore:chroma
```

#### Interactive Wizard
```python
#!/usr/bin/env python3
"""Interactive scaffolding wizard"""

import oneenv

def interactive_setup():
    """Interactive setup wizard"""
    print("🚀 OneEnv Interactive Setup Wizard")
    print("=" * 40)
    
    structure = oneenv.get_all_template_structure()
    selections = []
    
    for category, options in structure.items():
        print(f"\n📁 {category} Category:")
        print("Available options:")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = input(f"Select option (1-{len(options)}, or skip): ")
                if choice.lower() == 'skip':
                    break
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    selected_option = options[choice_num - 1]
                    selections.append({
                        "category": category,
                        "option": selected_option
                    })
                    print(f"✅ Selected: {category} → {selected_option}")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    if selections:
        print(f"\n🎯 Generating configuration...")
        content = oneenv.generate_template(".env.wizard", selections)
        print("✅ Configuration generated: .env.wizard")
        
        print("\n📋 Your selections:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
    else:
        print("No selections made.")

if __name__ == "__main__":
    interactive_setup()
```

### 3. JSON Output for Scripting

#### Get Structure in JSON Format
```bash
oneenv template --structure --json
```

**Output:**
```json
{
  "Database": ["postgres", "sqlite", "mysql"],
  "VectorStore": ["chroma", "pinecone", "weaviate"],
  "LLM": ["openai", "anthropic", "local"],
  "Cache": ["redis", "memcached"],
  "Monitoring": ["basic", "advanced"]
}
```

#### Category Info in JSON
```bash
oneenv template --info Database --json
```

**Output:**
```json
{
  "category": "Database",
  "options": ["postgres", "sqlite", "mysql"],
  "total_variables": 8,
  "critical_variables": 3,
  "important_variables": 3,
  "optional_variables": 2,
  "description": "Database connection and configuration templates"
}
```

## Practical Examples

### 1. RAG System Configuration

```python
# Setup for Retrieval-Augmented Generation system
import oneenv

# Define RAG components
rag_selections = [
    {"category": "Database", "option": "postgres"},      # Document metadata
    {"category": "VectorStore", "option": "chroma"},     # Embeddings
    {"category": "LLM", "option": "openai"},            # Text generation
    {"category": "Cache", "option": "redis"},           # Response caching
    {"category": "Monitoring", "option": "basic"}       # System monitoring
]

# Generate RAG-specific configuration
content = oneenv.generate_template(".env.rag", rag_selections)
print("RAG system configuration generated!")
```

### 2. Web Application Setup

```python
# Setup for web application
web_selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "Cache", "option": "redis"},
    {"category": "Monitoring", "option": "advanced"}
]

content = oneenv.generate_template(".env.web", web_selections)
```

### 3. Development vs Production

```python
# Development environment
dev_selections = [
    {"category": "Database", "option": "sqlite"},       # Lightweight for dev
    {"category": "Cache", "option": "redis"},
    {"category": "Monitoring", "option": "basic"}
]

# Production environment
prod_selections = [
    {"category": "Database", "option": "postgres"},     # Robust for production
    {"category": "Cache", "option": "redis"},
    {"category": "Monitoring", "option": "advanced"}   # Comprehensive monitoring
]

oneenv.generate_template(".env.development", dev_selections)
oneenv.generate_template(".env.production", prod_selections)
```

## Understanding Output Format

### Importance-Based Organization

Generated templates are organized by importance levels:

#### 1. **CRITICAL** 🚨
Settings essential for application operation:
- Database connection URLs
- API keys for external services
- Authentication secrets

#### 2. **IMPORTANT** ⚠️
Settings to configure for production use:
- Connection pool sizes
- Cache configurations
- API endpoints

#### 3. **OPTIONAL** ℹ️
Fine-tuning settings (defaults are sufficient):
- Timeout values
- Debug flags
- Performance optimizations

### Category-Based Grouping

Within each importance level, variables are grouped by category:

```env
# ========== CRITICAL: Essential Settings for Application Operation ==========

# ----- Database (postgres) -----
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# ----- LLM (openai) -----
OPENAI_API_KEY=

# ----- VectorStore (chroma) -----
CHROMA_HOST=localhost

# ========== IMPORTANT: Settings to Configure for Production Use ==========

# ----- Database (postgres) -----
DATABASE_POOL_SIZE=10

# ----- Cache (redis) -----
REDIS_URL=redis://localhost:6379/0

# ========== OPTIONAL: Fine-tuning Settings (Defaults are Sufficient) ==========

# ----- Database (postgres) -----
DATABASE_SSL_MODE=prefer

# ----- LLM (openai) -----
OPENAI_TEMPERATURE=0.7
```

## Troubleshooting

### Common Issues

#### 1. "No scaffolding templates are currently available"
**Cause**: No packages with OneEnv templates are installed.

**Solution**:
```bash
# Install packages that provide templates
pip install your-package-with-templates

# Or create your own templates (see Tutorial 9)
```

#### 2. "Category 'X' not found"
**Cause**: The specified category doesn't exist in available templates.

**Solution**:
```bash
# Check available categories
oneenv template --structure

# Use correct category name
oneenv template --info Database  # Not "database"
```

#### 3. "Option 'X' not found in category 'Y'"
**Cause**: The option doesn't exist in the specified category.

**Solution**:
```bash
# Check available options
oneenv template --info Database

# Use correct option name
oneenv template --preview Database postgres  # Not "postgresql"
```

#### 4. Empty or Minimal Template Generated
**Cause**: No templates match your selections, or templates are not properly installed.

**Solution**:
```python
# Check what's actually available
import oneenv
structure = oneenv.get_all_template_structure()
print(f"Available templates: {structure}")

# Verify your selections exist
for selection in your_selections:
    if not oneenv.has_category(selection['category']):
        print(f"Missing category: {selection['category']}")
```

### Performance Optimization

#### 1. Caching Template Discovery
```python
# Cache structure for repeated use
structure = oneenv.get_all_template_structure()

# Reuse cached structure instead of calling repeatedly
for category in structure.keys():
    options = oneenv.get_options(category)
    # Process options...
```

#### 2. Batch Processing
```python
# Process multiple selections at once
all_selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM", "option": "openai"}
]

# Single generation call
content = oneenv.generate_template(".env.example", all_selections)
```

### Error Handling Best Practices

```python
import oneenv

def safe_template_generation(selections, output_file):
    """Generate template with proper error handling"""
    try:
        # Validate selections first
        for selection in selections:
            if not oneenv.has_category(selection['category']):
                raise ValueError(f"Category '{selection['category']}' not found")
            
            options = oneenv.get_options(selection['category'])
            if selection['option'] not in options:
                raise ValueError(f"Option '{selection['option']}' not found in category '{selection['category']}'")
        
        # Generate template
        content = oneenv.generate_template(output_file, selections)
        return content
        
    except Exception as e:
        print(f"Error generating template: {e}")
        
        # Provide helpful suggestions
        structure = oneenv.get_all_template_structure()
        print(f"Available categories: {list(structure.keys())}")
        
        return None
```

## Best Practices

### 1. Template Organization
- **Start with Critical**: Always configure critical settings first
- **Environment-Specific**: Use different templates for dev/staging/production
- **Modular Approach**: Generate templates for specific components separately

### 2. Tool Development
- **User-Friendly**: Provide clear options and feedback
- **Error Handling**: Give helpful error messages with suggestions
- **Documentation**: Include usage examples and troubleshooting

### 3. Team Collaboration
- **Standardization**: Use consistent category and option names
- **Version Control**: Track template changes and versions
- **Documentation**: Document custom templates and their purposes

## Next Steps

- **Create Your Own Templates**: See [Tutorial 9: New Template Creation](../tutorials/09-new-template-creation.md)
- **Build Custom Tools**: See [Tutorial 10: Scaffolding Tool Creation](../tutorials/10-scaffolding-tool-creation.md)
- **Practical Examples**: See [Tutorial 11: Practical Guide](../tutorials/11-practical-guide.md)
- **API Reference**: See [Scaffolding API Reference](../api-reference/scaffolding-api.md)
- **Migration Guide**: See [Migration Guide](../migration-guides/scaffolding-format-migration.md)

---

**🎉 Congratulations!** You now understand how to effectively use OneEnv's Scaffolding System to manage environment configurations. The system provides powerful tools for both individual developers and teams to streamline their development workflows.