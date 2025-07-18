# チュートリアル 11: パッケージ開発者向け実践ガイド

**所要時間:** 15-20分  
**対象:** パッケージ開発者、ツール作成者  
**前提条件:** 前のチュートリアル、実際のプロジェクト経験

## 概要

OneEnvテンプレートとscaffoldingツールを実際のシナリオで活用する方法を学習します。このチュートリアルでは、RAGシステムからWebフレームワークまでの実践例を扱い、テスト、CI/CD統合、コミュニティ配布に関する洞察を提供します。

## 学習内容

- 実世界でのRAGシステム実装
- マルチパッケージ連携戦略
- テストとCI/CD統合
- コミュニティ配布のベストプラクティス
- 高度なトラブルシューティング技術

## 1. RAGシステム実装 (8分)

### 完全なRAGスタックテンプレート

RAG（Retrieval-Augmented Generation）システム用の包括的なテンプレートを作成しましょう：

```python
# rag_package/templates.py
def rag_system_template():
    """完全なRAGシステム環境テンプレート"""
    return [
        # データベース - ベクトルストレージとメタデータ
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "ドキュメントメタデータとユーザーデータ用PostgreSQL接続",
                    "default": "postgresql://user:pass@localhost:5432/rag_db",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "高スループット操作用コネクションプールサイズ",
                    "default": "20",
                    "required": False,
                    "importance": "important"
                },
                "DATABASE_TIMEOUT": {
                    "description": "クエリタイムアウト（秒）",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # ベクトルデータベース - エンベディングストレージ
        {
            "category": "VectorStore",
            "option": "chroma",
            "env": {
                "CHROMA_HOST": {
                    "description": "Chromaベクトルデータベースホスト",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "CHROMA_PORT": {
                    "description": "Chromaサーバーポート",
                    "default": "8000",
                    "required": False,
                    "importance": "important"
                },
                "CHROMA_COLLECTION": {
                    "description": "ドキュメントエンベディング用デフォルトコレクション",
                    "default": "rag_documents",
                    "required": False,
                    "importance": "important"
                },
                "CHROMA_PERSIST_DIRECTORY": {
                    "description": "永続ストレージ用ディレクトリ",
                    "default": "./chroma_db",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # 代替ベクトルストア
        {
            "category": "VectorStore",
            "option": "pinecone",
            "env": {
                "PINECONE_API_KEY": {
                    "description": "クラウドベクトルストレージ用Pinecone APIキー",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "PINECONE_ENVIRONMENT": {
                    "description": "Pinecone環境（例: us-west1-gcp）",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "PINECONE_INDEX": {
                    "description": "エンベディング用Pineconeインデックス名",
                    "default": "rag-index",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        
        # LLMプロバイダー
        {
            "category": "LLM",
            "option": "openai",
            "env": {
                "OPENAI_API_KEY": {
                    "description": "テキスト生成用OpenAI APIキー",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "OPENAI_MODEL": {
                    "description": "テキスト生成用プライマリモデル",
                    "default": "gpt-4",
                    "required": False,
                    "importance": "important",
                    "choices": ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
                },
                "OPENAI_EMBEDDING_MODEL": {
                    "description": "エンベディング生成用モデル",
                    "default": "text-embedding-ada-002",
                    "required": False,
                    "importance": "important"
                },
                "OPENAI_MAX_TOKENS": {
                    "description": "レスポンス当たりの最大トークン数",
                    "default": "1000",
                    "required": False,
                    "importance": "optional"
                },
                "OPENAI_TEMPERATURE": {
                    "description": "レスポンスの創造性（0.0-1.0）",
                    "default": "0.7",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # 代替LLM
        {
            "category": "LLM",
            "option": "anthropic",
            "env": {
                "ANTHROPIC_API_KEY": {
                    "description": "Claudeモデル用Anthropic APIキー",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "ANTHROPIC_MODEL": {
                    "description": "Claudeモデルバージョン",
                    "default": "claude-3-sonnet-20240229",
                    "required": False,
                    "importance": "important",
                    "choices": ["claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
                }
            }
        },
        
        # パフォーマンス用キャッシュ
        {
            "category": "Cache",
            "option": "redis",
            "env": {
                "REDIS_URL": {
                    "description": "エンベディングとレスポンス用Redisキャッシュ",
                    "default": "redis://localhost:6379/0",
                    "required": False,
                    "importance": "important"
                },
                "REDIS_TTL": {
                    "description": "キャッシュTTL（秒）",
                    "default": "3600",
                    "required": False,
                    "importance": "optional"
                },
                "REDIS_MAX_CONNECTIONS": {
                    "description": "最大Redis接続数",
                    "default": "10",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # モニタリングと可観測性
        {
            "category": "Monitoring",
            "option": "basic",
            "env": {
                "LOG_LEVEL": {
                    "description": "アプリケーションログレベル",
                    "default": "INFO",
                    "required": False,
                    "importance": "important",
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                },
                "METRICS_ENABLED": {
                    "description": "パフォーマンスメトリクス収集を有効化",
                    "default": "true",
                    "required": False,
                    "importance": "optional",
                    "choices": ["true", "false"]
                },
                "TRACE_QUERIES": {
                    "description": "デバッグ用クエリトレースを有効化",
                    "default": "false",
                    "required": False,
                    "importance": "optional",
                    "choices": ["true", "false"]
                }
            }
        }
    ]
```

### RAGシステムScaffoldingツール

RAGシステムセットアップ用の専用ツールを作成：

```python
# rag_package/rag_scaffold.py
import oneenv
import sys
from typing import Dict, List

class RAGSystemScaffold:
    def __init__(self):
        self.selections = []
        self.vector_store = None
        self.llm_provider = None
        self.use_cache = False
        
    def welcome(self):
        """RAGシステムセットアップのウェルカム表示"""
        print("🤖 RAGシステム環境セットアップ")
        print("=" * 40)
        print("このウィザードは、Retrieval-Augmented Generationシステムを設定します。")
        print("ベクトルストレージ、LLMプロバイダー、オプションコンポーネントを設定します。\n")
    
    def select_vector_store(self):
        """ベクトルストレージソリューションの選択"""
        print("🔍 ベクトルストア選択")
        print("エンベディングストレージ用のベクトルデータベースを選択してください:")
        
        if not oneenv.has_category("VectorStore"):
            print("❌ ベクトルストアテンプレートが見つかりません！")
            return False
        
        options = oneenv.get_options("VectorStore")
        
        print("\n利用可能なオプション:")
        for i, option in enumerate(options, 1):
            description = {
                "chroma": "ローカル/セルフホスト、開発に適している",
                "pinecone": "クラウドホスト、本番対応、APIキーが必要",
                "weaviate": "オープンソース、GraphQL API",
                "qdrant": "高性能、Rust製"
            }.get(option, "ベクトルデータベースオプション")
            
            print(f"  {i}. {option} - {description}")
        
        while True:
            try:
                choice = int(input(f"\nベクトルストアを選択 (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    self.vector_store = options[choice - 1]
                    self.selections.append({
                        "category": "VectorStore",
                        "option": self.vector_store
                    })
                    print(f"✅ 選択: {self.vector_store}")
                    return True
                else:
                    print(f"1から{len(options)}の間の数字を入力してください")
            except ValueError:
                print("有効な数字を入力してください")
    
    def select_llm_provider(self):
        """LLMプロバイダーの選択"""
        print("\n🧠 LLMプロバイダー選択")
        print("言語モデルプロバイダーを選択してください:")
        
        if not oneenv.has_category("LLM"):
            print("❌ LLMテンプレートが見つかりません！")
            return False
        
        options = oneenv.get_options("LLM")
        
        print("\n利用可能なオプション:")
        for i, option in enumerate(options, 1):
            description = {
                "openai": "GPTモデル、最も人気、APIキーが必要",
                "anthropic": "Claudeモデル、優れた推論、APIキーが必要",
                "local": "Ollama/LMStudio経由のローカルモデル、APIキー不要",
                "azure": "Azure OpenAI、エンタープライズ機能"
            }.get(option, "LLMプロバイダーオプション")
            
            print(f"  {i}. {option} - {description}")
        
        while True:
            try:
                choice = int(input(f"\nLLMプロバイダーを選択 (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    self.llm_provider = options[choice - 1]
                    self.selections.append({
                        "category": "LLM",
                        "option": self.llm_provider
                    })
                    print(f"✅ 選択: {self.llm_provider}")
                    return True
                else:
                    print(f"1から{len(options)}の間の数字を入力してください")
            except ValueError:
                print("有効な数字を入力してください")
    
    def select_optional_components(self):
        """オプションコンポーネントの選択"""
        print("\n⚡ オプションコンポーネント")
        
        # データベース
        if oneenv.has_category("Database"):
            use_db = input("メタデータストレージ用にデータベースを追加しますか？ (y/n): ").lower().startswith('y')
            if use_db:
                db_options = oneenv.get_options("Database")
                if "postgres" in db_options:
                    self.selections.append({
                        "category": "Database",
                        "option": "postgres"
                    })
                    print("✅ メタデータ用PostgreSQLを追加")
        
        # キャッシュ
        if oneenv.has_category("Cache"):
            use_cache = input("パフォーマンス向上のためRedisキャッシュを追加しますか？ (y/n): ").lower().startswith('y')
            if use_cache:
                self.use_cache = True
                cache_options = oneenv.get_options("Cache")
                if "redis" in cache_options:
                    self.selections.append({
                        "category": "Cache",
                        "option": "redis"
                    })
                    print("✅ Redisキャッシュを追加")
        
        # モニタリング
        if oneenv.has_category("Monitoring"):
            use_monitoring = input("モニタリングとログ機能を追加しますか？ (y/n): ").lower().startswith('y')
            if use_monitoring:
                monitoring_options = oneenv.get_options("Monitoring")
                if "basic" in monitoring_options:
                    self.selections.append({
                        "category": "Monitoring",
                        "option": "basic"
                    })
                    print("✅ 基本モニタリングを追加")
    
    def show_summary(self):
        """設定サマリーの表示"""
        print("\n📋 RAGシステム設定サマリー")
        print("=" * 40)
        
        for selection in self.selections:
            print(f"• {selection['category']}: {selection['option']}")
        
        print(f"\n🎯 あなたのRAGシステムで使用するもの:")
        print(f"  - ベクトルストア: {self.vector_store}")
        print(f"  - LLMプロバイダー: {self.llm_provider}")
        if self.use_cache:
            print(f"  - キャッシュ: 有効")
        
        print(f"\n💡 生成後の次のステップ:")
        if self.llm_provider in ["openai", "anthropic"]:
            print(f"  1. {self.llm_provider.upper()}_API_KEYを設定")
        if self.vector_store == "pinecone":
            print(f"  2. PINECONE_API_KEYとPINECONE_ENVIRONMENTを設定")
        print(f"  3. 他の設定を確認・カスタマイズ")
        print(f"  4. .env.exampleを.envにコピー")
    
    def generate_config(self):
        """最終設定の生成"""
        if not self.selections:
            print("❌ コンポーネントが選択されていません！")
            return False
        
        try:
            filename = input("\n出力ファイル (デフォルト: .env.rag): ").strip() or ".env.rag"
            oneenv.generate_template(filename, self.selections)
            print(f"\n🎉 RAGシステム設定を生成しました: {filename}")
            return True
        except Exception as e:
            print(f"❌ 設定生成エラー: {e}")
            return False
    
    def run(self):
        """RAG scaffoldingウィザードの実行"""
        self.welcome()
        
        if not self.select_vector_store():
            return
        
        if not self.select_llm_provider():
            return
        
        self.select_optional_components()
        self.show_summary()
        
        confirm = input("\n✅ この設定を生成しますか？ (y/n): ").lower().startswith('y')
        if confirm:
            self.generate_config()
        else:
            print("設定がキャンセルされました。")

if __name__ == "__main__":
    scaffold = RAGSystemScaffold()
    scaffold.run()
```

## 2. Webフレームワーク統合 (7分)

### Django/FastAPIテンプレート

```python
# web_framework/templates.py
def web_framework_template():
    """Webフレームワーク環境テンプレート"""
    return [
        # データベースオプション
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "プライマリデータベース接続",
                    "default": "postgresql://user:pass@localhost:5432/webapp",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "コネクションプールサイズ",
                    "default": "10",
                    "required": False,
                    "importance": "important"
                }
            }
        },
        
        # Webサーバー設定
        {
            "category": "WebServer",
            "option": "fastapi",
            "env": {
                "WEB_HOST": {
                    "description": "サーバーホストアドレス",
                    "default": "0.0.0.0",
                    "required": False,
                    "importance": "important"
                },
                "WEB_PORT": {
                    "description": "サーバーポート",
                    "default": "8000",
                    "required": False,
                    "importance": "important"
                },
                "WEB_WORKERS": {
                    "description": "ワーカープロセス数",
                    "default": "4",
                    "required": False,
                    "importance": "optional"
                },
                "WEB_RELOAD": {
                    "description": "開発環境での自動リロードを有効化",
                    "default": "false",
                    "required": False,
                    "importance": "optional",
                    "choices": ["true", "false"]
                }
            }
        },
        
        # 認証
        {
            "category": "Auth",
            "option": "jwt",
            "env": {
                "JWT_SECRET_KEY": {
                    "description": "JWTトークン署名用シークレットキー",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "JWT_EXPIRATION": {
                    "description": "トークン有効期限（秒）",
                    "default": "3600",
                    "required": False,
                    "importance": "important"
                },
                "JWT_ALGORITHM": {
                    "description": "JWT署名アルゴリズム",
                    "default": "HS256",
                    "required": False,
                    "importance": "optional",
                    "choices": ["HS256", "RS256", "ES256"]
                }
            }
        }
    ]
```

## 3. テストとCI/CD統合 (3分)

### テスト設定

```python
# tests/test_templates.py
import pytest
import oneenv
from oneenv.models import validate_scaffolding_format

def test_rag_template_validation():
    """RAGテンプレートが有効であることをテスト"""
    from rag_package.templates import rag_system_template
    
    template_data = rag_system_template()
    
    # 検証エラーが発生しないはず
    validate_scaffolding_format(template_data)
    
    # 必要なカテゴリが存在することを確認
    categories = {item["category"] for item in template_data}
    assert "VectorStore" in categories
    assert "LLM" in categories

def test_template_generation():
    """選択でのテンプレート生成をテスト"""
    selections = [
        {"category": "VectorStore", "option": "chroma"},
        {"category": "LLM", "option": "openai"}
    ]
    
    # エラーなしで生成されるはず
    content = oneenv.generate_template("test.env", selections)
    assert content
    assert "CHROMA_HOST" in content
    assert "OPENAI_API_KEY" in content

def test_api_functions():
    """OneEnv API関数が正しく動作することをテスト"""
    # 構造取得のテスト
    structure = oneenv.get_all_template_structure()
    assert isinstance(structure, dict)
    
    # カテゴリ確認のテスト
    if "VectorStore" in structure:
        assert oneenv.has_category("VectorStore")
        options = oneenv.get_options("VectorStore")
        assert isinstance(options, list)
        assert len(options) > 0

@pytest.mark.parametrize("category,expected_options", [
    ("VectorStore", ["chroma", "pinecone"]),
    ("LLM", ["openai", "anthropic"]),
])
def test_expected_options(category, expected_options):
    """期待されるオプションが利用可能であることをテスト"""
    if oneenv.has_category(category):
        actual_options = oneenv.get_options(category)
        for expected in expected_options:
            assert expected in actual_options, f"{expected}が{category}で見つかりません"
```

### GitHub Actionsワークフロー

```yaml
# .github/workflows/test-templates.yml
name: OneEnvテンプレートテスト

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-templates:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Python ${{ matrix.python-version }}をセットアップ
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: 依存関係をインストール
      run: |
        python -m pip install --upgrade pip
        pip install oneenv pytest
        pip install -e .
    
    - name: テンプレート検証をテスト
      run: |
        pytest tests/test_templates.py -v
    
    - name: scaffoldingツールをテスト
      run: |
        # scaffoldingツールがインポートして実行できることをテスト
        python -c "from rag_package.rag_scaffold import RAGSystemScaffold; print('インポート成功')"
    
    - name: サンプル設定を生成
      run: |
        # テンプレート生成をテスト
        python -c "
        import oneenv
        selections = [
            {'category': 'VectorStore', 'option': 'chroma'},
            {'category': 'LLM', 'option': 'openai'}
        ]
        content = oneenv.generate_template('.env.test', selections)
        print('テスト設定の生成に成功')
        "
```

## 4. コミュニティ配布 (2分)

### パッケージ構造

```
my_rag_package/
├── pyproject.toml
├── README.md
├── src/
│   └── my_rag_package/
│       ├── __init__.py
│       ├── templates.py
│       └── scaffold.py
├── tests/
│   ├── test_templates.py
│   └── test_scaffold.py
├── examples/
│   ├── basic_setup.py
│   └── advanced_setup.py
└── docs/
    └── configuration.md
```

### 配布用pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-rag-package"
version = "0.1.0"
description = "OneEnvテンプレート付きRAGシステム"
authors = [{name = "Your Name", email = "you@example.com"}]
dependencies = [
    "oneenv>=0.3.0",
    "pydantic>=2.0",
]
keywords = ["rag", "environment", "configuration", "templates"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

[project.optional-dependencies]
dev = ["pytest", "black", "isort", "mypy"]

[project.urls]
Homepage = "https://github.com/yourusername/my-rag-package"
Documentation = "https://my-rag-package.readthedocs.io"
Repository = "https://github.com/yourusername/my-rag-package"
Issues = "https://github.com/yourusername/my-rag-package/issues"

[project.scripts]
rag-setup = "my_rag_package.scaffold:main"

# OneEnvテンプレート登録
[project.entry-points."oneenv.templates"]
rag = "my_rag_package.templates:rag_system_template"
web = "my_rag_package.templates:web_framework_template"

[tool.hatch.build.targets.wheel]
packages = ["src/my_rag_package"]
```

### 配布用README

```markdown
# My RAG Package

OneEnv統合による簡単な環境設定を持つ完全なRAG（Retrieval-Augmented Generation）システム。

## クイックスタート

1. パッケージをインストール:
   ```bash
   pip install my-rag-package
   ```

2. セットアップウィザードを実行:
   ```bash
   rag-setup
   ```

3. またはOneEnvを直接使用:
   ```bash
   oneenv template --info VectorStore
   oneenv template --preview LLM openai
   ```

## 含まれるテンプレート

- **VectorStore**: Chroma、Pinecone、Weaviate
- **LLM**: OpenAI、Anthropic、ローカルモデル
- **Database**: PostgreSQL、SQLite
- **Cache**: Redis、Memcached
- **Monitoring**: 基本ログとメトリクス

## 貢献

新しいテンプレートの追加や既存のものの改善については、[貢献ガイド](CONTRIBUTING.md)を参照してください。
```

## ベストプラクティスまとめ

### 🏗️ テンプレート設計
- **論理的グループ化**: 技術カテゴリで整理
- **明確な命名**: 説明的なカテゴリとオプション名を使用
- **包括的なデフォルト**: 合理的なデフォルト値を提供
- **重要度レベル**: 重要 vs オプション設定をマーク

### 🧪 テスト戦略
- **検証テスト**: テンプレートがスキーマ検証を通ることを確認
- **統合テスト**: 実際のOneEnv APIでテスト
- **CI/CD自動化**: 複数のPythonバージョンでテストを実行
- **例の検証**: 例がドキュメント通りに動作することを確認

### 📦 配布
- **明確なドキュメント**: 各テンプレートの機能を説明
- **Entry-points登録**: テンプレートを自動発見可能にする
- **セマンティックバージョニング**: 適切なバージョン管理を使用
- **コミュニティエンゲージメント**: 課題テンプレートと貢献ガイドを提供

### 🔧 ツール作成
- **カスタムscaffolds**: ドメイン固有のセットアップウィザードを作成
- **設定検証**: ユーザー入力を徹底的に検証
- **エラーハンドリング**: 有用なエラーメッセージを提供
- **ユーザーエクスペリエンス**: ツールを直感的で情報豊富にする

## 次のステップ

1. **プロジェクトに適用**: これらのパターンを自分のパッケージで使用
2. **コミュニティ貢献**: 有用なテンプレートをコミュニティと共有
3. **高度な統合**: CI/CDとデプロイメント自動化を探索
4. **モニタリング**: テンプレートとツールに可観測性を追加

---

**🎉 おめでとうございます！** プロフェッショナルグレードのOneEnvテンプレートとscaffoldingツールを作成、テスト、配布するための知識を身につけました。あなたのパッケージは、箱から出してすぐに優れた開発者エクスペリエンスを提供できるようになりました！