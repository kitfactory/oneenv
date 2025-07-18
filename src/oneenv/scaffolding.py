"""
OneEnv Scaffolding System
Provides interactive environment configuration generation
"""

import os
import sys
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from .core import collect_all_options


def get_available_categories() -> Dict[str, Dict[str, Any]]:
    """
    Get all available categories from collected options
    
    Returns:
        Dict mapping category names to their options
    """
    all_options = collect_all_options()
    return all_options


def display_categories(categories: Dict[str, Dict[str, Any]]) -> None:
    """
    Display available categories in a user-friendly format
    
    Args:
        categories: Dictionary of categories and their options
    """
    print("\n📦 Available Categories:")
    print("=" * 50)
    
    for i, (category, options) in enumerate(categories.items(), 1):
        option_count = len(options)
        critical_count = sum(1 for opt in options.values() if opt.get('importance') == 'critical')
        
        print(f"{i:2d}. {category}")
        print(f"    📊 {option_count} options ({critical_count} critical)")
        
        # Show a few example variables
        examples = list(options.keys())[:3]
        if examples:
            example_text = ", ".join(examples)
            if len(options) > 3:
                example_text += f", ... ({len(options) - 3} more)"
            print(f"    🔧 Variables: {example_text}")
        print()


def interactive_category_selection(categories: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    Interactive category selection interface
    
    Args:
        categories: Available categories
        
    Returns:
        List of selected category names
    """
    display_categories(categories)
    
    print("💡 Selection Options:")
    print("  • Enter numbers (e.g., 1,3,5 or 1-3 or 1 3 5)")
    print("  • Enter 'all' to select all categories")
    print("  • Enter 'none' or press Enter to cancel")
    print()
    
    category_list = list(categories.keys())
    
    while True:
        try:
            user_input = input("Select categories: ").strip()
            
            if not user_input or user_input.lower() == 'none':
                return []
            
            if user_input.lower() == 'all':
                return category_list
            
            # Parse input
            selected_indices = []
            
            # Handle comma-separated values
            parts = user_input.replace(',', ' ').split()
            
            for part in parts:
                if '-' in part and len(part.split('-')) == 2:
                    # Handle range (e.g., 1-3)
                    start, end = part.split('-')
                    start_idx = int(start) - 1
                    end_idx = int(end) - 1
                    selected_indices.extend(range(start_idx, end_idx + 1))
                else:
                    # Handle single number
                    selected_indices.append(int(part) - 1)
            
            # Validate indices
            selected_categories = []
            for idx in selected_indices:
                if 0 <= idx < len(category_list):
                    selected_categories.append(category_list[idx])
                else:
                    print(f"❌ Invalid selection: {idx + 1}. Please choose 1-{len(category_list)}")
                    continue
            
            if selected_categories:
                print(f"\n✅ Selected: {', '.join(selected_categories)}")
                return selected_categories
            
        except ValueError:
            print("❌ Invalid input. Please enter numbers, ranges, 'all', or 'none'")
        except KeyboardInterrupt:
            print("\n\n❌ Selection cancelled")
            return []


def interactive_option_configuration(category: str, options: Dict[str, Any], importance_filter: Optional[str] = None) -> Dict[str, str]:
    """
    Interactive configuration of options within a category
    
    Args:
        category: Category name
        options: Options in the category
        importance_filter: Minimum importance level
        
    Returns:
        Dictionary of configured variable values
    """
    print(f"\n🔧 Configuring {category}")
    print("=" * 50)
    
    # Filter options by importance
    filtered_options = options
    if importance_filter:
        importance_levels = {"critical": 3, "important": 2, "optional": 1}
        min_level = importance_levels.get(importance_filter, 1)
        filtered_options = {
            name: config for name, config in options.items()
            if importance_levels.get(config.get('importance', 'optional'), 1) >= min_level
        }
    
    if not filtered_options:
        print(f"⚠️  No options match the importance filter '{importance_filter}'")
        return {}
    
    configured_values = {}
    
    print("💡 Configuration Options:")
    print("  • Press Enter to use default value")
    print("  • Enter 'skip' to skip this variable")
    print("  • Enter custom value to override default")
    print()
    
    for var_name, config in filtered_options.items():
        default_value = config.get('default', '')
        description = config.get('description', '')
        importance = config.get('importance', 'optional')
        required = config.get('required', False)
        choices = config.get('choices', [])
        
        # Display variable info
        importance_emoji = {"critical": "🔴", "important": "🟡", "optional": "🟢"}
        req_text = " (Required)" if required else ""
        
        print(f"{importance_emoji.get(importance, '🔵')} {var_name}{req_text}")
        if description:
            # Handle multi-line descriptions
            desc_lines = description.split('\n')
            for line in desc_lines:
                print(f"   {line}")
        
        if choices:
            print(f"   Choices: {', '.join(choices)}")
        
        if default_value:
            print(f"   Default: {default_value}")
        
        # Get user input
        while True:
            try:
                prompt = f"   Value: "
                user_value = input(prompt).strip()
                
                if user_value.lower() == 'skip':
                    break
                
                if not user_value:
                    # Use default
                    if default_value:
                        configured_values[var_name] = str(default_value)
                        print(f"   ✅ Using default: {default_value}")
                    elif required:
                        print(f"   ❌ This is a required field. Please provide a value or 'skip'")
                        continue
                    break
                
                # Validate choices
                if choices and user_value not in choices:
                    print(f"   ❌ Invalid choice. Must be one of: {', '.join(choices)}")
                    continue
                
                configured_values[var_name] = user_value
                print(f"   ✅ Set to: {user_value}")
                break
                
            except KeyboardInterrupt:
                print("\n   ⏭️  Skipping this variable")
                break
        
        print()
    
    return configured_values


def generate_env_content(configured_values: Dict[str, Dict[str, str]]) -> str:
    """
    Generate .env file content from configured values
    
    Args:
        configured_values: Dictionary mapping categories to their configured values
        
    Returns:
        String content for .env file
    """
    content = ["# Environment Configuration"]
    content.append("# Generated by OneEnv Scaffolding System")
    content.append("# https://github.com/oneenv-project/oneenv")
    content.append("")
    
    for category, values in configured_values.items():
        if not values:
            continue
            
        content.append(f"# === {category} ===")
        
        for var_name, var_value in values.items():
            content.append(f"{var_name}={var_value}")
        
        content.append("")
    
    return "\n".join(content)


def generate_scaffolding_env(
    categories: Optional[List[str]] = None,
    output_file: str = ".env",
    importance_filter: Optional[str] = None,
    interactive: bool = True
) -> Dict[str, Any]:
    """
    Generate scaffolding environment configuration
    
    Args:
        categories: List of categories to include (None for interactive selection)
        output_file: Path to output file
        importance_filter: Minimum importance level to include
        interactive: Whether to use interactive mode
        
    Returns:
        Dictionary with generation results
    """
    # Collect available options
    all_categories = get_available_categories()
    
    if not all_categories:
        print("❌ No scaffolding categories found. Please install packages with OneEnv templates.")
        return {}
    
    # Select categories
    if categories:
        # Validate provided categories
        invalid_categories = [cat for cat in categories if cat not in all_categories]
        if invalid_categories:
            print(f"❌ Invalid categories: {', '.join(invalid_categories)}")
            print(f"Available categories: {', '.join(all_categories.keys())}")
            return {}
        selected_categories = categories
    elif interactive:
        selected_categories = interactive_category_selection(all_categories)
        if not selected_categories:
            print("❌ No categories selected")
            return {}
    else:
        # Non-interactive mode without categories specified
        print("❌ No categories specified. Use --interactive or provide category names.")
        return {}
    
    print(f"\n🚀 Generating configuration for: {', '.join(selected_categories)}")
    
    # Configure each category
    all_configured_values = {}
    total_variables = 0
    
    for category in selected_categories:
        category_options = all_categories[category]
        
        if interactive:
            configured_values = interactive_option_configuration(
                category, category_options, importance_filter
            )
        else:
            # Non-interactive: use defaults for all options
            configured_values = {}
            for var_name, config in category_options.items():
                # Apply importance filter
                if importance_filter:
                    importance_levels = {"critical": 3, "important": 2, "optional": 1}
                    min_level = importance_levels.get(importance_filter, 1)
                    var_importance = importance_levels.get(config.get('importance', 'optional'), 1)
                    if var_importance < min_level:
                        continue
                
                default_value = config.get('default', '')
                if default_value or config.get('required', False):
                    configured_values[var_name] = str(default_value) if default_value else ''
        
        if configured_values:
            all_configured_values[category] = configured_values
            total_variables += len(configured_values)
    
    if not all_configured_values:
        print("❌ No variables configured")
        return {}
    
    # Generate content
    env_content = generate_env_content(all_configured_values)
    
    # Write to file
    try:
        output_path = Path(output_file)
        
        # Check if file exists and ask for confirmation
        if output_path.exists() and interactive:
            print(f"\n⚠️  File {output_file} already exists.")
            overwrite = input("Overwrite? (y/N): ").strip().lower()
            if overwrite not in ['y', 'yes']:
                print("❌ Generation cancelled")
                return {}
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        return {
            "success": True,
            "output_file": output_file,
            "categories_used": selected_categories,
            "variables_count": total_variables,
            "content": env_content
        }
        
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return {}


def main():
    """
    Main entry point for scaffolding generation
    For testing purposes
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="OneEnv Scaffolding Generator")
    parser.add_argument("categories", nargs="*", help="Categories to include")
    parser.add_argument("-o", "--output", default=".env", help="Output file")
    parser.add_argument("--importance", choices=["critical", "important", "optional"])
    parser.add_argument("--non-interactive", action="store_true")
    
    args = parser.parse_args()
    
    result = generate_scaffolding_env(
        categories=args.categories if args.categories else None,
        output_file=args.output,
        importance_filter=args.importance,
        interactive=not args.non_interactive
    )
    
    if result.get("success"):
        print(f"✅ Successfully generated {args.output}")
    else:
        print("❌ Generation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()