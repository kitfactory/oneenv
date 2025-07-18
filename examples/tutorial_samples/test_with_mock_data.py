#!/usr/bin/env python3
"""
Tutorial Demo with Mock Data Setup
モックデータを使ったチュートリアルデモ
"""

import sys
import os
import tempfile
import oneenv
from oneenv.core import _scaffolding_processor
from oneenv.models import EnvOption, EnvVarConfig


def setup_mock_templates_directly():
    """直接モックテンプレートを設定"""
    # 既存のテンプレートをクリア
    _scaffolding_processor.env_options.clear()
    
    # Tutorial 9のデータベーステンプレート
    database_postgres = EnvOption(
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
            ),
            "DATABASE_SSL_MODE": EnvVarConfig(
                description="SSL mode for connections",
                default="prefer",
                required=False,
                importance="optional",
                choices=["require", "prefer", "disable"]
            )
        }
    )
    
    database_sqlite = EnvOption(
        category="Database",
        option="sqlite",
        env={
            "DATABASE_URL": EnvVarConfig(
                description="SQLite database file path",
                default="sqlite:///app.db",
                required=True,
                importance="critical"
            ),
            "DATABASE_TIMEOUT": EnvVarConfig(
                description="Database connection timeout in seconds",
                default="30",
                required=False,
                importance="optional"
            )
        }
    )
    
    # Tutorial 11のVectorStoreテンプレート
    vectorstore_chroma = EnvOption(
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
            ),
            "CHROMA_COLLECTION": EnvVarConfig(
                description="Default collection for document embeddings",
                default="rag_documents",
                required=False,
                importance="important"
            )
        }
    )
    
    vectorstore_pinecone = EnvOption(
        category="VectorStore",
        option="pinecone",
        env={
            "PINECONE_API_KEY": EnvVarConfig(
                description="Pinecone API key for cloud vector storage",
                default="",
                required=True,
                importance="critical"
            ),
            "PINECONE_ENVIRONMENT": EnvVarConfig(
                description="Pinecone environment (e.g., us-west1-gcp)",
                default="",
                required=True,
                importance="critical"
            ),
            "PINECONE_INDEX": EnvVarConfig(
                description="Pinecone index name for embeddings",
                default="rag-index",
                required=True,
                importance="critical"
            )
        }
    )
    
    # LLMテンプレート
    llm_openai = EnvOption(
        category="LLM",
        option="openai",
        env={
            "OPENAI_API_KEY": EnvVarConfig(
                description="OpenAI API key for text generation",
                default="",
                required=True,
                importance="critical"
            ),
            "OPENAI_MODEL": EnvVarConfig(
                description="Primary model for text generation",
                default="gpt-4",
                required=False,
                importance="important",
                choices=["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
            ),
            "OPENAI_TEMPERATURE": EnvVarConfig(
                description="Response creativity (0.0-1.0)",
                default="0.7",
                required=False,
                importance="optional"
            )
        }
    )
    
    llm_anthropic = EnvOption(
        category="LLM",
        option="anthropic",
        env={
            "ANTHROPIC_API_KEY": EnvVarConfig(
                description="Anthropic API key for Claude models",
                default="",
                required=True,
                importance="critical"
            ),
            "ANTHROPIC_MODEL": EnvVarConfig(
                description="Claude model version",
                default="claude-3-sonnet-20240229",
                required=False,
                importance="important",
                choices=["claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
            )
        }
    )
    
    # Cache テンプレート
    cache_redis = EnvOption(
        category="Cache",
        option="redis",
        env={
            "REDIS_URL": EnvVarConfig(
                description="Redis server connection for caching",
                default="redis://localhost:6379/0",
                required=False,
                importance="important"
            ),
            "REDIS_TTL": EnvVarConfig(
                description="Cache TTL in seconds",
                default="3600",
                required=False,
                importance="optional"
            )
        }
    )
    
    # テンプレートを追加
    _scaffolding_processor.env_options.extend([
        database_postgres,
        database_sqlite,
        vectorstore_chroma,
        vectorstore_pinecone,
        llm_openai,
        llm_anthropic,
        cache_redis
    ])
    
    print("✅ モックテンプレートを設定しました")
    print(f"   テンプレート数: {len(_scaffolding_processor.env_options)}")


def test_api_functions():
    """API関数のテスト"""
    print("\n🚀 OneEnv Scaffolding API テスト")
    print("=" * 50)
    
    # 1. 構造情報の取得
    print("\n1. 📊 テンプレート構造の取得:")
    structure = oneenv.get_all_template_structure()
    
    if not structure:
        print("   ❌ テンプレートが見つかりません")
        return False
    
    for category, options in structure.items():
        print(f"   {category}: {options}")
    
    # 2. カテゴリ存在確認
    print("\n2. 🔍 カテゴリ存在確認:")
    categories_to_check = ["Database", "VectorStore", "LLM", "Cache", "NonExistent"]
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
        
        print(f"\n   📄 生成されたファイルの内容（最初の15行）:")
        for i, line in enumerate(lines[:15]):
            print(f"     {i+1:2d}: {line.rstrip()}")
        
        if len(lines) > 15:
            print(f"     ... (合計 {len(lines)} 行)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ テンプレート生成エラー: {e}")
        return False


def test_error_handling():
    """エラーハンドリングのテスト"""
    print("\n\n🚨 エラーハンドリングのテスト")
    print("=" * 50)
    
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


def test_tutorial_workflow():
    """チュートリアルワークフローのテスト"""
    print("\n\n🎯 チュートリアルワークフローのテスト")
    print("=" * 50)
    
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
            for env_option in _scaffolding_processor.env_options:
                if env_option.category == "Database" and env_option.option == option:
                    for var_name, var_config in env_option.env.items():
                        print(f"  {var_name}: {var_config.description}")
    
    # ステップ3: ユーザーの選択をシミュレート
    print("\nステップ3: ユーザー選択のシミュレーション")
    user_selections = [
        {"category": "Database", "option": "postgres"},
        {"category": "VectorStore", "option": "chroma"},
        {"category": "Cache", "option": "redis"}
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
            content_lines = f.readlines()
        
        # 重要度別の変数数をカウント
        critical_vars = []
        important_vars = []
        optional_vars = []
        
        for line in content_lines:
            if "=" in line and not line.startswith("#"):
                if "critical" in line.lower():
                    critical_vars.append(line.split("=")[0].strip())
                elif "important" in line.lower():
                    important_vars.append(line.split("=")[0].strip())
                elif "optional" in line.lower():
                    optional_vars.append(line.split("=")[0].strip())
        
        print(f"\n生成された環境変数の分類:")
        print(f"  • Critical: {len(critical_vars)} 個")
        print(f"  • Important: {len(important_vars)} 個")
        print(f"  • Optional: {len(optional_vars)} 個")
        print(f"  • 合計行数: {len(content_lines)}")
        
        # 重要度別の変数例を表示
        if critical_vars:
            print(f"\n  Critical変数例: {critical_vars[:3]}")
        if important_vars:
            print(f"  Important変数例: {important_vars[:3]}")
        if optional_vars:
            print(f"  Optional変数例: {optional_vars[:3]}")
        
        return True
        
    except Exception as e:
        print(f"❌ テンプレート生成エラー: {e}")
        return False


def test_cli_simulation():
    """CLIシミュレーションのテスト"""
    print("\n\n🖥️ CLIシミュレーションのテスト")
    print("=" * 50)
    
    # Tutorial 10のシンプルCLIツールのシミュレーション
    print("\n📋 Tutorial 10: シンプルCLIツールのシミュレーション")
    
    # --list オプションのシミュレーション
    print("\n1. --list オプションのシミュレーション:")
    print("🔍 利用可能なテンプレート:")
    print("=" * 30)
    
    structure = oneenv.get_all_template_structure()
    if not structure:
        print("❌ テンプレートが見つかりません。")
        return False
    
    for category, options in structure.items():
        print(f"\n📁 {category}:")
        for option in options:
            print(f"   • {option}")
    
    # --generate オプションのシミュレーション
    print("\n\n2. --generate オプションのシミュレーション:")
    print("🔨 テンプレート生成中: cli_test.env")
    
    selections = [
        {"category": "Database", "option": "postgres"},
        {"category": "LLM", "option": "openai"}
    ]
    
    try:
        content = oneenv.generate_template("cli_test.env", selections)
        print("✅ テンプレートの生成に成功しました！")
        print("📁 ファイル: cli_test.env")
        print("\n📋 選択された設定:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
        
        print("\n💡 次のステップ:")
        print("   1. cli_test.envを確認")
        print("   2. .envにコピーして値を設定")
        
        return True
        
    except Exception as e:
        print(f"❌ テンプレート生成エラー: {e}")
        return False


def main():
    """メイン関数"""
    print("🧪 OneEnv Tutorial Demo & Validation")
    print("=" * 60)
    
    # モックテンプレートの設定
    setup_mock_templates_directly()
    
    # 各種テストの実行
    success_count = 0
    total_tests = 4
    
    if test_api_functions():
        success_count += 1
    
    test_error_handling()  # エラーハンドリングは成功/失敗でカウントしない
    
    if test_tutorial_workflow():
        success_count += 1
    
    if test_cli_simulation():
        success_count += 1
    
    # 最終結果の表示
    print(f"\n\n🎉 テスト完了！")
    print(f"成功したテスト: {success_count}/{total_tests}")
    
    print("\n生成されたファイル:")
    generated_files = ["demo.env", "user_selection.env", "cli_test.env"]
    for filename in generated_files:
        if os.path.exists(filename):
            print(f"  ✅ {filename}")
        else:
            print(f"  ❌ {filename} (生成されませんでした)")
    
    print("\n💡 これらのファイルを確認して、実際の生成結果を確認してください。")
    
    # 成功率の評価
    if success_count == total_tests:
        print("\n🎯 すべてのテストが成功しました！")
        return 0
    else:
        print(f"\n⚠️  {total_tests - success_count} 個のテストが失敗しました。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)