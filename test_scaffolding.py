#!/usr/bin/env python3
"""
OneEnv Scaffolding API テストスクリプト
"""

import sys
import os

# パスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import oneenv

def test_scaffolding_api():
    """Scaffolding APIの基本テスト"""
    print("=== OneEnv Scaffolding API Test ===\n")
    
    # 1. get_all_template_structure() テスト
    print("1. Testing get_all_template_structure():")
    try:
        structure = oneenv.get_all_template_structure()
        print(f"✅ Structure: {structure}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # 2. has_category() テスト
    print("2. Testing has_category():")
    try:
        # 存在しないカテゴリ
        result = oneenv.has_category("Database")
        print(f"✅ has_category('Database'): {result}")
        
        result = oneenv.has_category("NonExistent")
        print(f"✅ has_category('NonExistent'): {result}")
        
        # 無効な引数テスト
        try:
            oneenv.has_category("")
            print("❌ Should have raised ValueError for empty string")
        except ValueError as e:
            print(f"✅ Correctly raised ValueError: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # 3. get_options() テスト
    print("3. Testing get_options():")
    try:
        options = oneenv.get_options("Database")
        print(f"✅ get_options('Database'): {options}")
        
        options = oneenv.get_options("NonExistent")
        print(f"✅ get_options('NonExistent'): {options}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    print()
    
    # 4. generate_template() テスト
    print("4. Testing generate_template():")
    try:
        # 空の選択範囲でテスト
        content = oneenv.generate_template("", [])
        print(f"✅ generate_template with empty range:")
        print(f"Content length: {len(content)} characters")
        
        # 無効な引数テスト
        try:
            oneenv.generate_template("", [{"invalid": "format"}])
            print("❌ Should have raised ValueError")
        except ValueError as e:
            print(f"✅ Correctly raised ValueError: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

def test_with_mock_templates():
    """モックテンプレートでテスト"""
    print("=== Mock Template Test ===\n")
    
    # モックentry-point関数を追加
    from oneenv.core import _scaffolding_processor
    from oneenv.models import EnvOption, EnvVarConfig
    
    # モックデータを直接追加
    mock_options = [
        EnvOption(
            category="Database",
            option="sqlite",
            env={
                "DATABASE_URL": EnvVarConfig(
                    description="SQLite database URL",
                    default="sqlite:///app.db",
                    required=True,
                    importance="critical"
                )
            }
        ),
        EnvOption(
            category="Database", 
            option="postgres",
            env={
                "DATABASE_URL": EnvVarConfig(
                    description="PostgreSQL connection URL",
                    default="postgresql://user:pass@localhost:5432/dbname",
                    required=True,
                    importance="critical"
                ),
                "DATABASE_POOL_SIZE": EnvVarConfig(
                    description="Connection pool size",
                    default="10",
                    required=False,
                    importance="optional"
                )
            }
        ),
        EnvOption(
            category="VectorStore",
            option="chroma",
            env={
                "CHROMA_HOST": EnvVarConfig(
                    description="Chroma host",
                    default="localhost",
                    required=True,
                    importance="important"
                ),
                "CHROMA_PORT": EnvVarConfig(
                    description="Chroma port",
                    default="8000",
                    required=False,
                    importance="optional"
                )
            }
        )
    ]
    
    # プロセッサーに直接追加
    _scaffolding_processor.env_options = mock_options
    
    print("1. Structure with mock data:")
    # 直接プロセッサーから取得（再読み込みを避ける）
    structure = _scaffolding_processor.get_template_structure()
    print(f"Structure: {structure}")
    print()
    
    print("2. Category existence:")
    print(f"has_category('Database'): {_scaffolding_processor.has_category('Database')}")
    print(f"has_category('VectorStore'): {_scaffolding_processor.has_category('VectorStore')}")
    print(f"has_category('NonExistent'): {_scaffolding_processor.has_category('NonExistent')}")
    print()
    
    print("3. Options by category:")
    print(f"get_options('Database'): {_scaffolding_processor.get_options('Database')}")
    print(f"get_options('VectorStore'): {_scaffolding_processor.get_options('VectorStore')}")
    print()
    
    print("4. Template generation:")
    generation_range = [
        {"category": "Database", "option": "postgres"},
        {"category": "VectorStore", "option": "chroma"}
    ]
    selected_vars = _scaffolding_processor.generate_by_selection(generation_range)
    from oneenv.core import generate_env_file_content
    content = generate_env_file_content(selected_vars)
    print("Generated template:")
    print(content)
    print()
    
    print("5. Template generation (all Database options):")
    generation_range = [
        {"category": "Database"}  # 全オプション
    ]
    selected_vars = _scaffolding_processor.generate_by_selection(generation_range)
    content = generate_env_file_content(selected_vars)
    print("Generated template (all Database):")
    print(content)
    print(f"Variables generated: {list(selected_vars.keys())}")
    print(f"Number of options found: {len([opt for opt in _scaffolding_processor.env_options if opt.category == 'Database'])}")

if __name__ == "__main__":
    test_scaffolding_api()
    test_with_mock_templates()