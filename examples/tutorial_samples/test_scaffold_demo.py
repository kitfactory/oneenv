#!/usr/bin/env python3
"""
Tutorial Scaffolding Demo with Mock Data
テスト用のモックデータを使った scaffolding ツールのデモ
"""

import oneenv
from oneenv.core import ScaffoldingTemplateProcessor
from oneenv.models import EnvOption, EnvVarConfig

def setup_mock_templates():
    """テスト用のモックテンプレートを設定"""
    processor = ScaffoldingTemplateProcessor()
    
    # Tutorial 9のデータベーステンプレート
    database_options = [
        EnvOption(
            category="Database",
            option="postgres",
            env={
                "DATABASE_URL": EnvVarConfig(
                    description="PostgreSQL connection URL",
                    default="postgresql://user:pass@localhost:5432/mydb",
                    required=True,
                    importance="critical"
                ),
                "DATABASE_POOL_SIZE": EnvVarConfig(
                    description="Connection pool size",
                    default="10",
                    required=False,
                    importance="important"
                )
            }
        ),
        EnvOption(
            category="Database",
            option="sqlite",
            env={
                "DATABASE_URL": EnvVarConfig(
                    description="SQLite database file path",
                    default="sqlite:///app.db",
                    required=True,
                    importance="critical"
                )
            }
        )
    ]
    
    # Tutorial 11のVectorStoreテンプレート
    vectorstore_options = [
        EnvOption(
            category="VectorStore",
            option="chroma",
            env={
                "CHROMA_HOST": EnvVarConfig(
                    description="Chroma vector database host",
                    default="localhost",
                    required=True,
                    importance="critical"
                ),
                "CHROMA_PORT": EnvVarConfig(
                    description="Chroma server port",
                    default="8000",
                    required=False,
                    importance="important"
                )
            }
        ),
        EnvOption(
            category="VectorStore",
            option="pinecone",
            env={
                "PINECONE_API_KEY": EnvVarConfig(
                    description="Pinecone API key",
                    default="",
                    required=True,
                    importance="critical"
                ),
                "PINECONE_INDEX": EnvVarConfig(
                    description="Pinecone index name",
                    default="rag-index",
                    required=True,
                    importance="critical"
                )
            }
        )
    ]
    
    # LLMテンプレート
    llm_options = [
        EnvOption(
            category="LLM",
            option="openai",
            env={
                "OPENAI_API_KEY": EnvVarConfig(
                    description="OpenAI API key",
                    default="",
                    required=True,
                    importance="critical"
                ),
                "OPENAI_MODEL": EnvVarConfig(
                    description="OpenAI model",
                    default="gpt-4",
                    required=False,
                    importance="important",
                    choices=["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
                )
            }
        )
    ]
    
    # プロセッサにテンプレートを追加
    processor.env_options.extend(database_options)
    processor.env_options.extend(vectorstore_options)
    processor.env_options.extend(llm_options)
    
    return processor

def demo_api_functions():
    """API関数のデモ"""
    print("🚀 OneEnv Scaffolding API デモ")
    print("=" * 40)
    
    # モックデータをセットアップ
    processor = setup_mock_templates()
    
    # 1. 構造情報の取得
    print("\n1. 📊 テンプレート構造の取得:")
    structure = oneenv.get_all_template_structure()
    for category, options in structure.items():
        print(f"   {category}: {options}")
    
    # 2. カテゴリ存在確認
    print("\n2. 🔍 カテゴリ存在確認:")
    categories_to_check = ["Database", "VectorStore", "LLM", "NonExistent"]
    for category in categories_to_check:
        exists = oneenv.has_category(category)
        status = "✅" if exists else "❌"
        print(f"   {status} {category}: {exists}")
    
    # 3. オプション取得
    print("\n3. 📋 カテゴリ別オプション:")
    for category in structure.keys():
        options = oneenv.get_options(category)
        print(f"   {category}: {options}")
    
    # 4. テンプレート生成
    print("\n4. 🔨 テンプレート生成:")
    selections = [
        {"category": "Database", "option": "postgres"},
        {"category": "VectorStore", "option": "chroma"},
        {"category": "LLM", "option": "openai"}
    ]
    
    print("   選択:")
    for selection in selections:
        print(f"     • {selection['category']}: {selection['option']}")
    
    try:
        content = oneenv.generate_template("demo.env", selections)
        print(f"\n   ✅ テンプレート生成成功！")
        print(f"   📁 ファイル: demo.env")
        
        # 生成されたファイルの内容を表示
        with open("demo.env", "r") as f:
            lines = f.readlines()
        
        print(f"\n   📄 生成されたファイルの内容（最初の10行）:")
        for i, line in enumerate(lines[:10]):
            print(f"     {i+1:2d}: {line.rstrip()}")
        
        if len(lines) > 10:
            print(f"     ... (合計 {len(lines)} 行)")
            
    except Exception as e:
        print(f"   ❌ テンプレート生成エラー: {e}")

def demo_error_handling():
    """エラーハンドリングのデモ"""
    print("\n\n🚨 エラーハンドリングのデモ")
    print("=" * 40)
    
    processor = setup_mock_templates()
    
    # 1. 存在しないカテゴリ
    print("\n1. 存在しないカテゴリのテスト:")
    try:
        options = oneenv.get_options("NonExistentCategory")
        print(f"   結果: {options}")
    except Exception as e:
        print(f"   エラー: {e}")
    
    # 2. 無効な選択でのテンプレート生成
    print("\n2. 無効な選択でのテンプレート生成:")
    invalid_selections = [
        {"category": "Database", "option": "nonexistent"},
        {"category": "InvalidCategory", "option": "postgres"}
    ]
    
    for selection in invalid_selections:
        try:
            content = oneenv.generate_template("invalid.env", [selection])
            print(f"   ✅ {selection}: 成功")
        except Exception as e:
            print(f"   ❌ {selection}: {e}")

def demo_tutorial_workflow():
    """チュートリアルワークフローのデモ"""
    print("\n\n🎯 チュートリアルワークフローのデモ")
    print("=" * 40)
    
    processor = setup_mock_templates()
    
    # Tutorial 10のシンプルCLIツールのワークフロー
    print("\n📋 Tutorial 10: シンプルCLIツールのワークフロー")
    
    # ステップ1: 利用可能なオプションを確認
    print("\nステップ1: 利用可能なオプションの確認")
    structure = oneenv.get_all_template_structure()
    print("利用可能なテンプレート:")
    for category, options in structure.items():
        print(f"  {category}: {', '.join(options)}")
    
    # ステップ2: 特定のカテゴリの詳細情報を取得
    print("\nステップ2: Database カテゴリの詳細情報")
    if oneenv.has_category("Database"):
        db_options = oneenv.get_options("Database")
        print(f"Databaseオプション: {db_options}")
        
        # 各オプションの詳細情報を表示
        for option in db_options:
            print(f"\n{option} オプションの詳細:")
            # オプションの環境変数を表示
            for env_option in processor.env_options:
                if env_option.category == "Database" and env_option.option == option:
                    for var_name, var_config in env_option.env.items():
                        print(f"  {var_name}: {var_config.description}")
    
    # ステップ3: ユーザーの選択をシミュレート
    print("\nステップ3: ユーザー選択のシミュレーション")
    user_selections = [
        {"category": "Database", "option": "postgres"},
        {"category": "VectorStore", "option": "chroma"}
    ]
    
    print("ユーザーが選択:")
    for selection in user_selections:
        print(f"  • {selection['category']}: {selection['option']}")
    
    # ステップ4: テンプレート生成
    print("\nステップ4: テンプレート生成")
    try:
        content = oneenv.generate_template("user_selection.env", user_selections)
        print("✅ テンプレート生成成功！")
        print("📁 ファイル: user_selection.env")
        
        # 生成されたファイルの要約を表示
        with open("user_selection.env", "r") as f:
            lines = f.readlines()
        
        # 重要度別の変数数をカウント
        critical_count = sum(1 for line in lines if "critical" in line.lower())
        important_count = sum(1 for line in lines if "important" in line.lower())
        optional_count = sum(1 for line in lines if "optional" in line.lower())
        
        print(f"生成された環境変数:")
        print(f"  • Critical: {critical_count}")
        print(f"  • Important: {important_count}")
        print(f"  • Optional: {optional_count}")
        print(f"  • 合計行数: {len(lines)}")
        
    except Exception as e:
        print(f"❌ テンプレート生成エラー: {e}")

if __name__ == "__main__":
    demo_api_functions()
    demo_error_handling()
    demo_tutorial_workflow()
    
    print("\n\n🎉 デモ完了！")
    print("生成されたファイル:")
    print("  • demo.env")
    print("  • user_selection.env")
    print("\nこれらのファイルを確認して、実際の生成結果を確認してください。")