# OneEnv Scaffolding API Reference

## Overview

The OneEnv Scaffolding API provides programmatic access to the enhanced template system that organizes environment variable templates by categories and options. This API enables developers to create custom tools, scripts, and applications that leverage OneEnv's template discovery and generation capabilities.

## Core Functions

### `oneenv.get_all_template_structure()`

Returns the complete structure of all available templates organized by categories and options.

**Signature:**
```python
def get_all_template_structure() -> Dict[str, List[str]]
```

**Parameters:**
- None

**Returns:**
- `Dict[str, List[str]]`: Dictionary mapping category names to lists of available options

**Example:**
```python
import oneenv

structure = oneenv.get_all_template_structure()
print(structure)
# Output: {
#     'Database': ['postgres', 'sqlite', 'mysql'],
#     'VectorStore': ['chroma', 'pinecone', 'weaviate'],
#     'LLM': ['openai', 'anthropic', 'local'],
#     'Cache': ['redis', 'memcached'],
#     'Monitoring': ['basic', 'advanced']
# }
```

**Usage Notes:**
- This function scans all installed packages with OneEnv templates
- Results are cached for performance
- Returns empty dict if no scaffolding templates are available
- Categories and options are sorted alphabetically

---

### `oneenv.has_category(category)`

Checks if a specific category exists in the available templates.

**Signature:**
```python
def has_category(category: str) -> bool
```

**Parameters:**
- `category` (str): The category name to check

**Returns:**
- `bool`: True if the category exists, False otherwise

**Example:**
```python
import oneenv

if oneenv.has_category("Database"):
    print("Database templates are available")
else:
    print("No database templates found")

# Check multiple categories
categories_to_check = ["Database", "VectorStore", "NonExistent"]
for cat in categories_to_check:
    status = "✅" if oneenv.has_category(cat) else "❌"
    print(f"{status} {cat}")
```

**Usage Notes:**
- Case-sensitive category matching
- Returns False for None or empty string input
- Useful for validation before calling other category-specific functions

---

### `oneenv.get_options(category)`

Returns all available options for a specific category.

**Signature:**
```python
def get_options(category: str) -> List[str]
```

**Parameters:**
- `category` (str): The category name to get options for

**Returns:**
- `List[str]`: List of available options for the category

**Raises:**
- `ValueError`: If the category doesn't exist

**Example:**
```python
import oneenv

try:
    options = oneenv.get_options("Database")
    print(f"Database options: {options}")
    # Output: ['postgres', 'sqlite', 'mysql']
    
    for option in options:
        print(f"  • {option}")
        
except ValueError as e:
    print(f"Error: {e}")
```

**Usage Notes:**
- Always check `has_category()` first to avoid exceptions
- Options are sorted alphabetically
- Returns empty list if category exists but has no options

---

### `oneenv.generate_template(dest, generation_range)`

Generates a customized environment template file based on selected categories and options.

**Signature:**
```python
def generate_template(dest: str, generation_range: List[Dict[str, str]]) -> str
```

**Parameters:**
- `dest` (str): Destination file path for the generated template
- `generation_range` (List[Dict[str, str]]): List of category/option selections

**Returns:**
- `str`: The generated template content

**Generation Range Format:**
Each selection dictionary must contain:
- `category` (str): The category name
- `option` (str): The option name within the category

**Example:**
```python
import oneenv

# Define your selections
selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM", "option": "openai"},
    {"category": "Cache", "option": "redis"}
]

# Generate template
content = oneenv.generate_template(".env.example", selections)
print("Generated template content:")
print(content)
```

**Generated Output Format:**
```env
# ========== CRITICAL: Essential Settings for Application Operation ==========

# ----- Database (postgres) -----
# PostgreSQL connection URL
# Required | Critical
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# ----- LLM (openai) -----
# OpenAI API key for text generation
# Required | Critical
OPENAI_API_KEY=

# ========== IMPORTANT: Settings to Configure for Production Use ==========

# ----- Database (postgres) -----
# Connection pool size
# Optional | Important
DATABASE_POOL_SIZE=10

# ----- Cache (redis) -----
# Redis connection URL
# Optional | Important
REDIS_URL=redis://localhost:6379/0

# ========== OPTIONAL: Fine-tuning Settings (Defaults are Sufficient) ==========

# ----- Database (postgres) -----
# SSL mode for connections
# Optional | Optional
# Choices: require, prefer, disable
DATABASE_SSL_MODE=prefer
```

**Usage Notes:**
- Template content is organized by importance: Critical → Important → Optional
- Variables are grouped by category within each importance level
- Comments include description, requirement status, and choices (if applicable)
- File is created/overwritten at the specified destination path

---

## Information Retrieval Functions

### `oneenv.get_structure_info()`

Returns detailed information about the overall template structure.

**Signature:**
```python
def get_structure_info() -> Dict[str, Any]
```

**Parameters:**
- None

**Returns:**
- `Dict[str, Any]`: Detailed structure information

**Example:**
```python
import oneenv

info = oneenv.get_structure_info()
print(f"Total categories: {info['total_categories']}")
print(f"Total options: {info['total_options']}")
print(f"Total variables: {info['total_variables']}")

# Example output:
# {
#     'total_categories': 5,
#     'total_options': 12,
#     'total_variables': 45,
#     'categories': {
#         'Database': {'options': 3, 'variables': 8},
#         'VectorStore': {'options': 3, 'variables': 12},
#         'LLM': {'options': 3, 'variables': 9},
#         'Cache': {'options': 2, 'variables': 6},
#         'Monitoring': {'options': 2, 'variables': 10}
#     }
# }
```

---

### `oneenv.get_category_info(category)`

Returns detailed information about a specific category.

**Signature:**
```python
def get_category_info(category: str) -> Dict[str, Any]
```

**Parameters:**
- `category` (str): The category name to get information about

**Returns:**
- `Dict[str, Any]`: Category information including options and variable counts

**Raises:**
- `ValueError`: If the category doesn't exist

**Example:**
```python
import oneenv

try:
    info = oneenv.get_category_info("Database")
    print(f"Category: {info['category']}")
    print(f"Options: {info['options']}")
    print(f"Total variables: {info['total_variables']}")
    print(f"Critical variables: {info['critical_variables']}")
    print(f"Important variables: {info['important_variables']}")
    print(f"Optional variables: {info['optional_variables']}")
    
    # Example output:
    # {
    #     'category': 'Database',
    #     'options': ['postgres', 'sqlite', 'mysql'],
    #     'total_variables': 8,
    #     'critical_variables': 3,
    #     'important_variables': 3,
    #     'optional_variables': 2,
    #     'description': 'Database connection and configuration templates'
    # }
    
except ValueError as e:
    print(f"Error: {e}")
```

---

### `oneenv.get_option_preview(category, option)`

Returns a preview of what variables would be generated for a specific option.

**Signature:**
```python
def get_option_preview(category: str, option: str) -> Dict[str, Any]
```

**Parameters:**
- `category` (str): The category name
- `option` (str): The option name within the category

**Returns:**
- `Dict[str, Any]`: Preview information including variables and their configurations

**Raises:**
- `ValueError`: If the category or option doesn't exist

**Example:**
```python
import oneenv

try:
    preview = oneenv.get_option_preview("Database", "postgres")
    print(f"Preview: {preview['category']} → {preview['option']}")
    print(f"Variables: {len(preview['variables'])}")
    
    for var_name, var_config in preview['variables'].items():
        importance = var_config['importance']
        required = "Required" if var_config['required'] else "Optional"
        print(f"  {var_name}: {required} | {importance.title()}")
        print(f"    {var_config['description']}")
        print(f"    Default: {var_config['default']}")
        if 'choices' in var_config:
            print(f"    Choices: {var_config['choices']}")
        print()
        
except ValueError as e:
    print(f"Error: {e}")
```

---

## CLI Integration Functions

### `oneenv.cli_structure_display()`

Formats template structure for CLI display.

**Signature:**
```python
def cli_structure_display(json_output: bool = False) -> str
```

**Parameters:**
- `json_output` (bool): Whether to return JSON format (default: False)

**Returns:**
- `str`: Formatted structure display

**Example:**
```python
import oneenv

# Table format
table_output = oneenv.cli_structure_display()
print(table_output)

# JSON format
json_output = oneenv.cli_structure_display(json_output=True)
print(json_output)
```

---

### `oneenv.cli_category_display(category)`

Formats category information for CLI display.

**Signature:**
```python
def cli_category_display(category: str, json_output: bool = False) -> str
```

**Parameters:**
- `category` (str): The category name to display
- `json_output` (bool): Whether to return JSON format (default: False)

**Returns:**
- `str`: Formatted category information

**Example:**
```python
import oneenv

# Human-readable format
info = oneenv.cli_category_display("Database")
print(info)

# JSON format
json_info = oneenv.cli_category_display("Database", json_output=True)
print(json_info)
```

---

### `oneenv.cli_option_preview(category, option)`

Formats option preview for CLI display.

**Signature:**
```python
def cli_option_preview(category: str, option: str) -> str
```

**Parameters:**
- `category` (str): The category name
- `option` (str): The option name

**Returns:**
- `str`: Formatted option preview

**Example:**
```python
import oneenv

preview = oneenv.cli_option_preview("Database", "postgres")
print(preview)
```

---

## Error Handling

### Exception Types

The Scaffolding API uses the following exception types:

#### `ValueError`
Raised when invalid parameters are provided:
- Category doesn't exist
- Option doesn't exist in category
- Invalid generation range format

#### `FileNotFoundError`
Raised when template destination path is invalid

#### `PermissionError`
Raised when insufficient permissions to write template file

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
        
    except ValueError as e:
        print(f"Validation error: {e}")
        
        # Provide helpful suggestions
        structure = oneenv.get_all_template_structure()
        print(f"Available categories: {list(structure.keys())}")
        
        return None
        
    except PermissionError as e:
        print(f"Permission error: {e}")
        print("Please check file permissions and try again")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## Performance Considerations

### Caching

The API implements intelligent caching for performance:

```python
# Structure is cached after first call
structure = oneenv.get_all_template_structure()  # Slow - scans packages
structure = oneenv.get_all_template_structure()  # Fast - uses cache

# Cache is automatically invalidated when packages change
```

### Batch Processing

For multiple operations, batch calls for better performance:

```python
# Efficient approach
structure = oneenv.get_all_template_structure()
for category in structure.keys():
    options = oneenv.get_options(category)
    # Process options...

# Less efficient approach
for category in ["Database", "VectorStore", "LLM"]:
    if oneenv.has_category(category):  # Each call may scan packages
        options = oneenv.get_options(category)
```

---

## Integration Examples

### Custom CLI Tool

```python
#!/usr/bin/env python3
"""Custom scaffolding tool"""

import oneenv
import argparse

def main():
    parser = argparse.ArgumentParser(description="Custom OneEnv Scaffolding Tool")
    parser.add_argument("--list", action="store_true", help="List available templates")
    parser.add_argument("--info", help="Show category information")
    parser.add_argument("--preview", nargs=2, metavar=("CATEGORY", "OPTION"), 
                       help="Preview option")
    parser.add_argument("--generate", nargs="+", metavar="CATEGORY:OPTION",
                       help="Generate template")
    
    args = parser.parse_args()
    
    if args.list:
        print(oneenv.cli_structure_display())
    elif args.info:
        print(oneenv.cli_category_display(args.info))
    elif args.preview:
        category, option = args.preview
        print(oneenv.cli_option_preview(category, option))
    elif args.generate:
        selections = []
        for item in args.generate:
            category, option = item.split(":")
            selections.append({"category": category, "option": option})
        
        content = oneenv.generate_template(".env.custom", selections)
        print("✅ Custom template generated successfully!")

if __name__ == "__main__":
    main()
```

### Interactive Setup Wizard

```python
#!/usr/bin/env python3
"""Interactive setup wizard"""

import oneenv

def interactive_setup():
    """Interactive setup wizard"""
    print("🚀 OneEnv Interactive Setup Wizard")
    print("=" * 40)
    
    structure = oneenv.get_all_template_structure()
    selections = []
    
    for category, options in structure.items():
        print(f"\n📁 {category} Category:")
        
        # Show category info
        try:
            info = oneenv.get_category_info(category)
            print(f"Available options: {', '.join(info['options'])}")
            print(f"Total variables: {info['total_variables']}")
        except ValueError:
            pass
        
        # Show options
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        # Get user choice
        while True:
            choice = input(f"Select option (1-{len(options)}, or skip): ")
            if choice.lower() == 'skip':
                break
            
            try:
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

### Web API Integration

```python
from flask import Flask, jsonify, request
import oneenv

app = Flask(__name__)

@app.route('/api/structure', methods=['GET'])
def get_structure():
    """Get template structure"""
    try:
        structure = oneenv.get_all_template_structure()
        return jsonify(structure)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/category/<category>', methods=['GET'])
def get_category(category):
    """Get category information"""
    try:
        info = oneenv.get_category_info(category)
        return jsonify(info)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/generate', methods=['POST'])
def generate_template():
    """Generate template from selections"""
    try:
        selections = request.json.get('selections', [])
        content = oneenv.generate_template('.env.generated', selections)
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Version Compatibility

### Supported Python Versions
- Python 3.8+
- Dependencies: `pydantic`, `python-dotenv`

### API Stability
- **Stable**: Core functions (`get_all_template_structure`, `has_category`, `get_options`, `generate_template`)
- **Stable**: Information functions (`get_category_info`, `get_option_preview`)
- **Stable**: CLI integration functions

### Backward Compatibility
- Legacy template format continues to work
- Existing OneEnv APIs remain unchanged
- New API functions are additive only

---

## Next Steps

- **Create Custom Tools**: Use these APIs to build custom scaffolding tools
- **Integrate with CI/CD**: Automate environment setup in deployment pipelines
- **Build Web Interfaces**: Create web-based template generators
- **Package Development**: Create new template packages for your ecosystems

For more examples and tutorials, see:
- [Scaffolding Usage Guide](../user-guides/scaffolding-usage.md)
- [Tool Creation Tutorial](../tutorials/10-scaffolding-tool-creation.md)
- [Practical Examples](../tutorials/11-practical-guide.md)