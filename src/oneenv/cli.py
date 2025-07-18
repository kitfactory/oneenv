import argparse
import sys
import json

from oneenv import template, generate_env_example, diff
from oneenv.info_api import get_structure_info, get_category_info, get_option_preview
from oneenv.scaffolding import generate_scaffolding_env

def main():
    """
    English: Main entry point for the oneenv command line interface.
    Japanese: oneenvコマンドラインインターフェースのメインエントリーポイント。
    """
    parser = argparse.ArgumentParser(description="OneEnv: Environment variable management tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Template command
    template_parser = subparsers.add_parser("template", help="Generate .env.example file or show template information")
    
    # Info options (mutually exclusive)
    info_group = template_parser.add_mutually_exclusive_group()
    info_group.add_argument("--structure", action="store_true", 
                           help="Show available template structure")
    info_group.add_argument("--info", metavar="CATEGORY",
                           help="Show detailed info for a category")
    info_group.add_argument("--preview", nargs=2, metavar=("CATEGORY", "OPTION"),
                           help="Preview specific option template")
    
    # Output options
    template_parser.add_argument("--json", action="store_true",
                                help="Output in JSON format (for --structure and --info)")
    template_parser.add_argument(
        "-o", "--output",
        help="Output file path (default: .env.example)",
        default=".env.example"
    )
    template_parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate scaffolding environment configuration")
    generate_parser.add_argument(
        "categories",
        nargs="*",
        help="Categories to include (e.g., Database VectorStore). If not specified, interactive selection will be used."
    )
    generate_parser.add_argument(
        "-o", "--output",
        help="Output file path (default: .env)",
        default=".env"
    )
    generate_parser.add_argument(
        "--importance",
        choices=["critical", "important", "optional"],
        help="Minimum importance level to include"
    )
    generate_parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Force interactive mode even when categories are specified"
    )

    # Diff command
    diff_parser = subparsers.add_parser("diff", help="Show differences between two .env files")
    diff_parser.add_argument(
        "previous",
        help="Path to the previous .env file"
    )
    diff_parser.add_argument(
        "current",
        help="Path to the current .env file"
    )

    args = parser.parse_args()

    if args.command == "template":
        try:
            # Handle info commands
            if args.structure:
                result = get_structure_info(json_format=args.json)
                if args.json:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print(result)
                return
            
            elif args.info:
                result = get_category_info(args.info, json_format=args.json)
                if args.json:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print(result)
                return
            
            elif args.preview:
                category, option = args.preview
                result = get_option_preview(category, option)
                print(result)
                return
            
            # Default behavior: generate template
            generate_env_example(args.output, debug=args.debug)
            print(f"Generated template at: {args.output}")
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "generate":
        try:
            result = generate_scaffolding_env(
                categories=args.categories if args.categories else None,
                output_file=args.output,
                importance_filter=args.importance,
                interactive=args.interactive or not args.categories
            )
            if result:
                print(f"✅ Generated environment file: {args.output}")
                if result.get("categories_used"):
                    print(f"📂 Categories included: {', '.join(result['categories_used'])}")
                if result.get("variables_count"):
                    print(f"🔧 Variables configured: {result['variables_count']}")
            else:
                print("❌ Generation cancelled or failed")
                sys.exit(1)
        except Exception as e:
            print(f"Error generating scaffolding environment: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "diff":
        try:
            with open(args.previous, 'r', encoding='utf-8') as f:
                previous_text = f.read()
            with open(args.current, 'r', encoding='utf-8') as f:
                current_text = f.read()
            
            diff_result = diff(previous_text, current_text)
            print(diff_result)
        except FileNotFoundError as e:
            print(f"Error: File not found - {e.filename}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error comparing files: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 