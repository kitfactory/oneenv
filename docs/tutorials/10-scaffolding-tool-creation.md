# Tutorial 10: Creating Scaffolding Tools with Information API

**Time:** 20-25 minutes  
**Target:** Tool creators, package developers  
**Prerequisites:** Basic Python, CLI development knowledge

## Overview

Learn how to create custom scaffolding tools using OneEnv's information API. These tools can provide interactive setup experiences tailored to your specific use cases.

## What You'll Learn

- Understand OneEnv's information API
- Create simple CLI scaffolding tools
- Build interactive selection wizards
- Handle errors and edge cases gracefully
- Integrate with existing workflows

## 1. Understanding the Information API (5 minutes)

### Core API Functions

OneEnv provides four main functions for retrieving template information:

```python
import oneenv

# Get all available categories and their options
structure = oneenv.get_all_template_structure()
# Returns: {"Database": ["postgres", "sqlite"], "Cache": ["redis"]}

# Check if a category exists
has_db = oneenv.has_category("Database")
# Returns: True or False

# Get options for a specific category
db_options = oneenv.get_options("Database")
# Returns: ["postgres", "sqlite", "mysql"]

# Generate template based on selections
selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "Cache", "option": "redis"}
]
content = oneenv.generate_template(".env.example", selections)
# Returns: Generated template content
```

### CLI Information Commands

Before building tools, explore what's available:

```bash
# See all available structure
oneenv template --structure

# Get category details
oneenv template --info Database

# Preview specific option
oneenv template --preview Database postgres

# Get JSON output for scripts
oneenv template --structure --json
```

## 2. Simple CLI Tool (8 minutes)

Let's create a basic command-line scaffolding tool.

### Step 1: Create the Basic Structure

Create `simple_scaffold.py`:

```python
#!/usr/bin/env python3
"""Simple OneEnv Scaffolding Tool"""

import oneenv
import argparse
import sys
from typing import List, Dict

def list_available_options():
    """Display all available categories and options"""
    print("🔍 Available Templates:")
    print("=" * 30)
    
    try:
        structure = oneenv.get_all_template_structure()
        
        if not structure:
            print("❌ No templates found. Install packages with OneEnv templates first.")
            return
        
        for category, options in structure.items():
            print(f"\n📁 {category}:")
            for option in options:
                print(f"   • {option}")
                
    except Exception as e:
        print(f"❌ Error retrieving templates: {e}")
        sys.exit(1)

def validate_selection(category: str, option: str) -> bool:
    """Validate that a category/option combination exists"""
    if not oneenv.has_category(category):
        print(f"❌ Category '{category}' not found.")
        
        # Suggest similar categories
        structure = oneenv.get_all_template_structure()
        available = list(structure.keys())
        print(f"📋 Available categories: {', '.join(available)}")
        return False
    
    available_options = oneenv.get_options(category)
    if option not in available_options:
        print(f"❌ Option '{option}' not found in category '{category}'.")
        print(f"📋 Available options: {', '.join(available_options)}")
        return False
    
    return True

def generate_template_file(selections: List[Dict[str, str]], output_file: str):
    """Generate template file from selections"""
    print(f"🔨 Generating template: {output_file}")
    
    try:
        content = oneenv.generate_template(output_file, selections)
        
        print("✅ Template generated successfully!")
        print(f"📁 File: {output_file}")
        print("\n📋 Selected configuration:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
            
        print(f"\n💡 Next steps:")
        print(f"   1. Review {output_file}")
        print(f"   2. Copy to .env and set your values")
        
    except Exception as e:
        print(f"❌ Error generating template: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Simple OneEnv Scaffolding Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list
  %(prog)s --generate Database:postgres Cache:redis
  %(prog)s --generate Database:sqlite --output .env.dev
        """
    )
    
    parser.add_argument(
        "--list", 
        action="store_true",
        help="List all available categories and options"
    )
    
    parser.add_argument(
        "--generate", 
        nargs="+",
        metavar="CATEGORY:OPTION",
        help="Generate template with specified category:option pairs"
    )
    
    parser.add_argument(
        "--output", 
        default=".env.example",
        help="Output file name (default: .env.example)"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_available_options()
        return
    
    if args.generate:
        # Parse category:option pairs
        selections = []
        
        for item in args.generate:
            if ":" not in item:
                print(f"❌ Invalid format: '{item}'. Use CATEGORY:OPTION format.")
                sys.exit(1)
            
            category, option = item.split(":", 1)
            
            if not validate_selection(category, option):
                sys.exit(1)
            
            selections.append({"category": category, "option": option})
        
        generate_template_file(selections, args.output)
        return
    
    # Show help if no arguments
    parser.print_help()

if __name__ == "__main__":
    main()
```

### Step 2: Test the Tool

```bash
# Make it executable
chmod +x simple_scaffold.py

# List available options
./simple_scaffold.py --list

# Generate a template
./simple_scaffold.py --generate Database:postgres Cache:redis

# Custom output file
./simple_scaffold.py --generate Database:sqlite --output .env.dev
```

## 3. Interactive Wizard (7 minutes)

Now let's create an interactive wizard for better user experience.

### Step 1: Create the Interactive Wizard

Create `interactive_scaffold.py`:

```python
#!/usr/bin/env python3
"""Interactive OneEnv Scaffolding Wizard"""

import oneenv
import sys
from typing import List, Dict, Optional

class ScaffoldingWizard:
    def __init__(self):
        self.selections: List[Dict[str, str]] = []
        self.structure = {}
        
    def load_templates(self):
        """Load available templates"""
        try:
            self.structure = oneenv.get_all_template_structure()
            if not self.structure:
                print("❌ No templates found. Install packages with OneEnv templates first.")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading templates: {e}")
            sys.exit(1)
    
    def show_welcome(self):
        """Display welcome message"""
        print("🚀 OneEnv Interactive Scaffolding Wizard")
        print("=" * 45)
        print("This wizard will help you set up your environment configuration.")
        print("You can select from multiple categories and options.\n")
    
    def display_categories(self) -> List[str]:
        """Display available categories and return the list"""
        categories = list(self.structure.keys())
        
        print("📁 Available Categories:")
        for i, category in enumerate(categories, 1):
            options_count = len(self.structure[category])
            print(f"   {i}. {category} ({options_count} options)")
        
        return categories
    
    def select_category(self) -> Optional[str]:
        """Let user select a category"""
        categories = self.display_categories()
        
        while True:
            try:
                print(f"\n❓ Select a category (1-{len(categories)}, or 0 to finish):")
                choice = input("👉 ").strip()
                
                if choice == "0":
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    return categories[choice_num - 1]
                else:
                    print(f"❌ Please enter a number between 1 and {len(categories)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def display_options(self, category: str) -> List[str]:
        """Display options for a category"""
        options = oneenv.get_options(category)
        
        print(f"\n🔧 Available options for {category}:")
        for i, option in enumerate(options, 1):
            # Get a preview to show variable count
            try:
                preview = oneenv.get_option_preview(category, option)
                var_lines = [line for line in preview.split('\n') 
                           if '=' in line and not line.startswith('#')]
                var_count = len(var_lines)
                print(f"   {i}. {option} ({var_count} variables)")
            except:
                print(f"   {i}. {option}")
        
        return options
    
    def select_option(self, category: str) -> Optional[str]:
        """Let user select an option from a category"""
        options = self.display_options(category)
        
        while True:
            try:
                print(f"\n❓ Select an option (1-{len(options)}, or 0 to skip):")
                choice = input("👉 ").strip()
                
                if choice == "0":
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return options[choice_num - 1]
                else:
                    print(f"❌ Please enter a number between 1 and {len(options)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def show_preview(self, category: str, option: str):
        """Show preview of selected option"""
        try:
            preview = oneenv.get_option_preview(category, option)
            print(f"\n📋 Preview of {category}:{option}:")
            print("-" * 30)
            # Show only the first few lines
            lines = preview.split('\n')[:10]
            for line in lines:
                print(line)
            if len(preview.split('\n')) > 10:
                print("...")
            print("-" * 30)
        except Exception as e:
            print(f"⚠️  Could not load preview: {e}")
    
    def confirm_selection(self, category: str, option: str) -> bool:
        """Ask user to confirm their selection"""
        self.show_preview(category, option)
        
        while True:
            confirm = input(f"\n✅ Add {category}:{option} to your configuration? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                return True
            elif confirm in ['n', 'no']:
                return False
            else:
                print("❌ Please enter 'y' or 'n'")
    
    def show_current_selections(self):
        """Display current selections"""
        if not self.selections:
            print("\n📝 No selections made yet.")
            return
        
        print("\n📝 Current selections:")
        for i, selection in enumerate(self.selections, 1):
            print(f"   {i}. {selection['category']}: {selection['option']}")
    
    def generate_final_template(self) -> str:
        """Generate the final template"""
        if not self.selections:
            print("❌ No selections made. Cannot generate template.")
            return ""
        
        output_file = input("\n📁 Output filename (default: .env.example): ").strip()
        if not output_file:
            output_file = ".env.example"
        
        try:
            content = oneenv.generate_template(output_file, self.selections)
            return output_file
        except Exception as e:
            print(f"❌ Error generating template: {e}")
            return ""
    
    def run(self):
        """Run the interactive wizard"""
        self.load_templates()
        self.show_welcome()
        
        while True:
            self.show_current_selections()
            
            category = self.select_category()
            if category is None:
                break
            
            option = self.select_option(category)
            if option is None:
                continue
            
            if self.confirm_selection(category, option):
                self.selections.append({"category": category, "option": option})
                print(f"✅ Added {category}:{option}")
        
        if self.selections:
            print("\n🎯 Finalizing your configuration...")
            output_file = self.generate_final_template()
            
            if output_file:
                print(f"\n🎉 Success! Generated {output_file}")
                print("\n💡 Next steps:")
                print(f"   1. Review {output_file}")
                print("   2. Copy to .env and set your actual values")
                print("   3. Add .env to your .gitignore file")
        else:
            print("\n👋 No selections made. Goodbye!")

def main():
    wizard = ScaffoldingWizard()
    wizard.run()

if __name__ == "__main__":
    main()
```

### Step 2: Test the Interactive Wizard

```bash
# Make it executable
chmod +x interactive_scaffold.py

# Run the wizard
./interactive_scaffold.py
```

## 4. Advanced Features (5 minutes)

### Configuration File Support

Create `config_scaffold.py` for YAML-based configuration:

```python
#!/usr/bin/env python3
"""Configuration-based OneEnv Scaffolding Tool"""

import oneenv
import yaml
import argparse
import sys
from typing import Dict, List

def load_config(config_file: str) -> Dict:
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_file}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Invalid YAML in {config_file}: {e}")
        sys.exit(1)

def validate_config(config: Dict) -> List[Dict[str, str]]:
    """Validate configuration and return selections"""
    selections = []
    
    if 'selections' not in config:
        print("❌ Configuration must contain 'selections' key")
        sys.exit(1)
    
    for item in config['selections']:
        if 'category' not in item or 'option' not in item:
            print(f"❌ Each selection must have 'category' and 'option': {item}")
            sys.exit(1)
        
        category = item['category']
        option = item['option']
        
        # Validate with OneEnv
        if not oneenv.has_category(category):
            print(f"❌ Category '{category}' not found")
            sys.exit(1)
        
        available_options = oneenv.get_options(category)
        if option not in available_options:
            print(f"❌ Option '{option}' not found in category '{category}'")
            print(f"📋 Available: {', '.join(available_options)}")
            sys.exit(1)
        
        selections.append({"category": category, "option": option})
    
    return selections

def create_sample_config():
    """Create a sample configuration file"""
    sample = {
        'output': '.env.example',
        'selections': [
            {'category': 'Database', 'option': 'postgres'},
            {'category': 'Cache', 'option': 'redis'}
        ]
    }
    
    with open('scaffold.yaml', 'w') as f:
        yaml.dump(sample, f, default_flow_style=False)
    
    print("📝 Created sample configuration: scaffold.yaml")
    print("💡 Edit this file and run: python config_scaffold.py scaffold.yaml")

def main():
    parser = argparse.ArgumentParser(description="Configuration-based OneEnv Scaffolding")
    parser.add_argument('config', nargs='?', help="YAML configuration file")
    parser.add_argument('--sample', action='store_true', help="Create sample configuration")
    
    args = parser.parse_args()
    
    if args.sample:
        create_sample_config()
        return
    
    if not args.config:
        parser.print_help()
        return
    
    # Load and validate configuration
    config = load_config(args.config)
    selections = validate_config(config)
    
    # Generate template
    output_file = config.get('output', '.env.example')
    
    try:
        oneenv.generate_template(output_file, selections)
        print(f"✅ Generated {output_file} from {args.config}")
        
        print("\n📋 Applied configuration:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
            
    except Exception as e:
        print(f"❌ Error generating template: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Sample YAML Configuration

```yaml
# scaffold.yaml
output: .env.example
selections:
  - category: Database
    option: postgres
  - category: Cache
    option: redis
  - category: VectorStore
    option: chroma
```

## 5. Integration with Build Tools

### Adding to package.json Scripts

```json
{
  "scripts": {
    "env:setup": "python scripts/scaffold.py",
    "env:interactive": "python scripts/interactive_scaffold.py"
  }
}
```

### Adding to Makefile

```makefile
.PHONY: env-setup
env-setup:
	python scripts/scaffold.py --generate Database:postgres Cache:redis

.PHONY: env-interactive
env-interactive:
	python scripts/interactive_scaffold.py
```

## Best Practices

### 🛡️ Error Handling
- Always validate category/option combinations
- Provide helpful error messages with suggestions
- Handle network/file system errors gracefully

### 🎨 User Experience
- Use clear visual indicators (emojis, colors if supported)
- Provide previews before final selection
- Show progress and next steps

### 📦 Distribution
- Make tools executable with shebang lines
- Include requirements.txt or pyproject.toml dependencies
- Add help text and examples

### 🔧 Extensibility
- Support configuration files for repeatable setups
- Allow custom output formats
- Enable integration with existing workflows

## Next Steps

- **Try the Examples**: Test all three tools with your projects
- **Tutorial 11**: See real-world applications in practical projects
- **Customize**: Adapt these examples for your specific needs
- **Share**: Consider packaging your tools for the community

## Quick Reference

### Essential API Functions
```python
oneenv.get_all_template_structure()  # Get full structure
oneenv.has_category(category)        # Check category exists
oneenv.get_options(category)         # Get category options
oneenv.generate_template(file, selections)  # Generate template
```

### CLI Information Commands
```bash
oneenv template --structure          # Show all structure
oneenv template --info CATEGORY      # Category details
oneenv template --preview CAT OPTION # Option preview
oneenv template --structure --json   # JSON output
```

---

**🎉 Congratulations!** You now know how to create powerful scaffolding tools using OneEnv's information API. These tools can greatly improve the developer experience for your packages and projects.