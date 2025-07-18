# Phase 4: チュートリアル・ドキュメント強化計画書

## 概要

OneEnvの新機能（Scaffolding API、情報提供API）を活用するためのチュートリアルとドキュメントを強化し、パッケージ開発者が簡単にツールを作成できるようにする。

## チュートリアル構成方針

### 🎯 対象ユーザー
1. **パッケージ開発者** - OneEnvテンプレートを作成する開発者
2. **ツール作成者** - 独自scaffoldingツールを作成する開発者
3. **エンドユーザー** - OneEnvの高度な機能を活用したいユーザー

### 📋 新規チュートリアル構成

#### Tutorial 9: 新しいテンプレート作成方法 (15-20分)
- **目的**: Scaffolding形式でのテンプレート作成をマスター
- **対象**: パッケージ開発者
- **内容**:
  - 従来のgroups形式との違い
  - category/option/env構造の理解
  - importance、required、choicesの活用
  - entry-points登録方法
  - 実際のパッケージでの実装例

#### Tutorial 10: 情報提供APIを使ったScaffoldingツール作成 (20-25分)
- **目的**: OneEnvの情報APIを活用したカスタムツール作成
- **対象**: ツール作成者
- **内容**:
  - OneEnv情報APIの概要
  - `get_all_template_structure()`の活用
  - インタラクティブな選択UIの実装
  - `generate_template()`でのテンプレート生成
  - エラーハンドリングとユーザビリティ

#### Tutorial 11: パッケージ開発者向け実践ガイド (15-20分)
- **目的**: 実際のプロジェクトでの活用方法
- **対象**: パッケージ開発者・ツール作成者
- **内容**:
  - RAGシステムでの実例
  - 複数パッケージ連携の考慮事項
  - テストとCI/CDでの活用
  - コミュニティでの配布方法

## 詳細実装計画

### 🎯 Tutorial 9: 新しいテンプレート作成方法

#### ファイル構成
```
docs/tutorials/09-new-template-creation.md
docs/tutorials/09-new-template-creation_ja.md
examples/template_creation/
├── simple_template.py
├── advanced_template.py
├── rag_system_template.py
└── pyproject.toml.example
```

#### カリキュラム
1. **基本概念の理解** (5分)
   - Scaffolding形式の利点
   - category/option構造の説明
   - 従来形式との比較

2. **シンプルなテンプレート作成** (5分)
   ```python
   # simple_template.py
   def database_template():
       return [
           {
               "category": "Database",
               "option": "sqlite",
               "env": {
                   "DATABASE_URL": {
                       "description": "SQLite database file path",
                       "default": "sqlite:///app.db",
                       "required": True,
                       "importance": "critical"
                   }
               }
           }
       ]
   ```

3. **高度なテンプレート機能** (5分)
   - 複数オプションの提供
   - importance階層の活用
   - choicesフィールドの使用
   - required/optionalの使い分け

4. **entry-points登録** (3分)
   - pyproject.toml設定
   - パッケージ化の方法

5. **実践演習** (2分)
   - 実際にテンプレートを作成・テスト

### 🎯 Tutorial 10: Scaffoldingツール作成

#### ファイル構成
```
docs/tutorials/10-scaffolding-tool-creation.md
docs/tutorials/10-scaffolding-tool-creation_ja.md
examples/scaffolding_tools/
├── simple_cli.py
├── interactive_wizard.py
├── web_interface.py
└── rag_scaffold.py
```

#### カリキュラム
1. **OneEnv情報APIの理解** (5分)
   - APIの概要と用途
   - 構造情報の取得方法
   - CLIツールでの確認

2. **シンプルなCLIツール作成** (8分)
   ```python
   # simple_cli.py
   import oneenv
   import argparse
   
   def main():
       parser = argparse.ArgumentParser(description="Custom Scaffolding Tool")
       parser.add_argument("--list", action="store_true", help="List available options")
       parser.add_argument("--generate", nargs="+", help="Generate template")
       
       args = parser.parse_args()
       
       if args.list:
           structure = oneenv.get_all_template_structure()
           for category, options in structure.items():
               print(f"{category}: {', '.join(options)}")
       
       elif args.generate:
           # カスタム生成ロジック
           selections = parse_selections(args.generate)
           oneenv.generate_template(".env.example", selections)
   ```

3. **インタラクティブウィザード** (7分)
   - プログレッシブディスクロージャー
   - ユーザーフレンドリーな選択UI
   - バリデーションとエラーハンドリング

4. **実践演習** (5分)
   - 実際にツールを作成・テスト

### 🎯 Tutorial 11: 実践ガイド

#### ファイル構成
```
docs/tutorials/11-practical-guide.md
docs/tutorials/11-practical-guide_ja.md
examples/practical_examples/
├── rag_system/
│   ├── templates.py
│   ├── scaffold.py
│   └── pyproject.toml
├── web_framework/
│   ├── templates.py
│   └── setup_wizard.py
└── testing/
    ├── test_templates.py
    └── test_scaffolding.py
```

#### カリキュラム
1. **RAGシステムの実例** (8分)
   - Database、VectorStore、LLMの組み合わせ
   - 相互依存関係の管理
   - 設定の競合解決

2. **Webフレームワークでの活用** (7分)
   - Django/FastAPI向けテンプレート
   - プロジェクト初期化ツール
   - 開発環境の自動セットアップ

3. **テストとCI/CD** (3分)
   - テンプレートの自動テスト
   - CI/CDでの検証方法

4. **コミュニティ配布** (2分)
   - PyPIでの公開方法
   - ドキュメントのベストプラクティス

## サンプルコード設計

### 🔧 RAGシステムのテンプレート例

```python
# examples/practical_examples/rag_system/templates.py
def rag_templates():
    return [
        # Database options
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL connection URL for vector storage",
                    "default": "postgresql://user:pass@localhost:5432/rag_db",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "Connection pool size for high-throughput queries",
                    "default": "20",
                    "required": False,
                    "importance": "important"
                }
            }
        },
        
        # Vector Store options
        {
            "category": "VectorStore",
            "option": "chroma",
            "env": {
                "CHROMA_HOST": {
                    "description": "Chroma vector database host",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "CHROMA_PORT": {
                    "description": "Chroma server port",
                    "default": "8000",
                    "required": False,
                    "importance": "optional"
                },
                "CHROMA_COLLECTION": {
                    "description": "Default collection name for documents",
                    "default": "rag_documents",
                    "required": False,
                    "importance": "important"
                }
            }
        },
        
        # LLM options
        {
            "category": "LLM",
            "option": "openai",
            "env": {
                "OPENAI_API_KEY": {
                    "description": "OpenAI API key for text generation",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "OPENAI_MODEL": {
                    "description": "OpenAI model to use",
                    "default": "gpt-4",
                    "required": False,
                    "importance": "important",
                    "choices": ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
                }
            }
        }
    ]
```

### 🛠️ RAGシステム用Scaffoldingツール例

```python
# examples/practical_examples/rag_system/scaffold.py
import oneenv

def interactive_rag_setup():
    """Interactive RAG system setup wizard"""
    
    print("🤖 RAG System Environment Setup")
    print("=" * 40)
    
    # Get available structure
    structure = oneenv.get_all_template_structure()
    selections = []
    
    # Database selection
    if "Database" in structure:
        print("\n📊 Database Selection:")
        db_options = oneenv.get_options("Database")
        for i, option in enumerate(db_options, 1):
            preview = oneenv.get_option_preview("Database", option)
            var_count = len([line for line in preview.split('\n') if '=' in line and not line.startswith('#')])
            print(f"  {i}. {option} ({var_count} variables)")
        
        while True:
            try:
                choice = int(input(f"Select database (1-{len(db_options)}): "))
                if 1 <= choice <= len(db_options):
                    selections.append({
                        "category": "Database",
                        "option": db_options[choice - 1]
                    })
                    break
            except ValueError:
                print("Please enter a valid number.")
    
    # Vector Store selection
    if "VectorStore" in structure:
        print("\n🔍 Vector Store Selection:")
        vs_options = oneenv.get_options("VectorStore")
        for i, option in enumerate(vs_options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = int(input(f"Select vector store (1-{len(vs_options)}): "))
                if 1 <= choice <= len(vs_options):
                    selections.append({
                        "category": "VectorStore",
                        "option": vs_options[choice - 1]
                    })
                    break
            except ValueError:
                print("Please enter a valid number.")
    
    # LLM selection
    if "LLM" in structure:
        print("\n🧠 LLM Selection:")
        llm_options = oneenv.get_options("LLM")
        for i, option in enumerate(llm_options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = int(input(f"Select LLM (1-{len(llm_options)}): "))
                if 1 <= choice <= len(llm_options):
                    selections.append({
                        "category": "LLM",
                        "option": llm_options[choice - 1]
                    })
                    break
            except ValueError:
                print("Please enter a valid number.")
    
    # Generate template
    if selections:
        print(f"\n🎯 Generating RAG system configuration...")
        content = oneenv.generate_template(".env.example", selections)
        
        print("✅ Generated .env.example with the following configuration:")
        for selection in selections:
            print(f"  - {selection['category']}: {selection['option']}")
        
        print(f"\n📝 Please review and edit .env.example, then copy to .env")
        print("🔐 Remember to set your API keys and sensitive information!")
    
    else:
        print("❌ No selections made. Setup cancelled.")

if __name__ == "__main__":
    interactive_rag_setup()
```

## 実装スケジュール

### Day 1: Tutorial 9 - テンプレート作成
- [ ] チュートリアル文書作成（英語・日本語）
- [ ] サンプルコード作成
- [ ] 動作確認・テスト

### Day 2: Tutorial 10 - Scaffoldingツール作成
- [ ] チュートリアル文書作成（英語・日本語）
- [ ] サンプルツール作成
- [ ] 動作確認・テスト

### Day 3: Tutorial 11 - 実践ガイド
- [ ] 実践ガイド文書作成（英語・日本語）
- [ ] 実践サンプル作成
- [ ] 統合テスト・最終確認

## 成功基準

### 📚 教育効果
- ✅ パッケージ開発者が30分以内にテンプレート作成可能
- ✅ ツール作成者が1時間以内に基本的なscaffoldingツール作成可能
- ✅ 実践例が実際のプロジェクトで活用可能

### 🛠️ 技術面
- ✅ 全サンプルコードが動作確認済み
- ✅ チュートリアルの手順が明確で漏れなし
- ✅ エラーハンドリングとトラブルシューティングを含む

### 📖 ドキュメント品質
- ✅ 英語・日本語両方で完全なドキュメント
- ✅ 段階的な学習曲線の提供
- ✅ 既存チュートリアルとの整合性

---

**注意**: このチュートリアル計画は実用性を重視し、開発者が実際のプロジェクトですぐに活用できる内容を目指しています。