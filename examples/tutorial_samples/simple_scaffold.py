#!/usr/bin/env python3
"""
Tutorial 10 Example: Simple Scaffolding Tool
シンプルなOneEnv Scaffoldingツールの例
"""

import oneenv
import argparse
import sys
from typing import List, Dict

def list_available_options():
    """利用可能な全カテゴリとオプションを表示"""
    print("🔍 利用可能なテンプレート:")
    print("=" * 30)
    
    try:
        structure = oneenv.get_all_template_structure()
        
        if not structure:
            print("❌ テンプレートが見つかりません。OneEnvテンプレートを持つパッケージを先にインストールしてください。")
            return
        
        for category, options in structure.items():
            print(f"\n📁 {category}:")
            for option in options:
                print(f"   • {option}")
                
    except Exception as e:
        print(f"❌ テンプレート取得エラー: {e}")
        sys.exit(1)

def validate_selection(category: str, option: str) -> bool:
    """カテゴリ/オプションの組み合わせが存在することを検証"""
    if not oneenv.has_category(category):
        print(f"❌ カテゴリ '{category}' が見つかりません。")
        
        # 類似カテゴリを提案
        structure = oneenv.get_all_template_structure()
        available = list(structure.keys())
        print(f"📋 利用可能なカテゴリ: {', '.join(available)}")
        return False
    
    available_options = oneenv.get_options(category)
    if option not in available_options:
        print(f"❌ オプション '{option}' がカテゴリ '{category}' に見つかりません。")
        print(f"📋 利用可能なオプション: {', '.join(available_options)}")
        return False
    
    return True

def generate_template_file(selections: List[Dict[str, str]], output_file: str):
    """選択からテンプレートファイルを生成"""
    print(f"🔨 テンプレート生成中: {output_file}")
    
    try:
        content = oneenv.generate_template(output_file, selections)
        
        print("✅ テンプレートの生成に成功しました！")
        print(f"📁 ファイル: {output_file}")
        print("\n📋 選択された設定:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
            
        print(f"\n💡 次のステップ:")
        print(f"   1. {output_file}を確認")
        print(f"   2. .envにコピーして値を設定")
        
    except Exception as e:
        print(f"❌ テンプレート生成エラー: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="シンプルなOneEnv Scaffoldingツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  %(prog)s --list
  %(prog)s --generate Database:postgres Cache:redis
  %(prog)s --generate Database:sqlite --output .env.dev
        """
    )
    
    parser.add_argument(
        "--list", 
        action="store_true",
        help="利用可能な全カテゴリとオプションをリスト表示"
    )
    
    parser.add_argument(
        "--generate", 
        nargs="+",
        metavar="CATEGORY:OPTION",
        help="指定されたcategory:optionペアでテンプレートを生成"
    )
    
    parser.add_argument(
        "--output", 
        default=".env.example",
        help="出力ファイル名 (デフォルト: .env.example)"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_available_options()
        return
    
    if args.generate:
        # category:optionペアを解析
        selections = []
        
        for item in args.generate:
            if ":" not in item:
                print(f"❌ 無効な形式: '{item}'。CATEGORY:OPTION形式を使用してください。")
                sys.exit(1)
            
            category, option = item.split(":", 1)
            
            if not validate_selection(category, option):
                sys.exit(1)
            
            selections.append({"category": category, "option": option})
        
        generate_template_file(selections, args.output)
        return
    
    # 引数がない場合はヘルプを表示
    parser.print_help()

if __name__ == "__main__":
    main()