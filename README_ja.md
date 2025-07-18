# OneEnv 🌟

[![PyPI Downloads](https://static.pepy.tech/badge/oneenv)](https://pepy.tech/projects/oneenv)

**Python環境変数管理をシンプルに。**

OneEnvはインストールされたパッケージから環境変数テンプレートを自動発見し、名前空間で管理します。

## 中核機能 🎯

### 1. 🏗️ インテリジェントスキャフォールディングシステム
環境変数テンプレートをカテゴリ別（Database、VectorStore、LLMなど）に整理し、構造化された発見と選択的生成を提供。

### 2. 📦 パッケージ環境変数発見
インストールされた全パッケージから環境変数テンプレートを自動収集 - 手動設定不要。

### 3. 🏷️ 名前空間管理
サービス/コンポーネント別に環境変数を整理し、インテリジェントなフォールバック機能。

### 4. 🛠️ ツール対応API
カスタムスキャフォールディングツールや統合開発のためのテンプレート構造へのプログラマティックアクセス。

## インストール 📦

```bash
pip install oneenv
```

## クイックスタート 🚀

### 環境変数テンプレート生成
```bash
oneenv template
```

### 利用可能なテンプレートの探索
```bash
# 利用可能な全カテゴリとオプションを表示
oneenv template --structure

# 特定カテゴリの詳細情報を取得
oneenv template --info Database

# 特定オプションをプレビュー
oneenv template --preview Database postgres

# カスタム設定を生成
oneenv template --generate Database:postgres VectorStore:chroma
```

### 名前付き環境の使用
```python
import oneenv

# 異なる環境をロード
oneenv.env().load_dotenv("common.env")
oneenv.env("database").load_dotenv("database.env")
oneenv.env("web").load_dotenv("web.env")

# 名前空間フォールバックで値を取得
db_host = oneenv.env("database").get("HOST", "localhost")
web_port = oneenv.env("web").get("PORT", "8000")
timeout = oneenv.env("database").get("TIMEOUT", "30")  # 共通設定にフォールバック
```

## 例: 導入前vs導入後

**OneEnv導入前:**
```python
# 散らばった環境変数
DATABASE_URL = os.getenv("DATABASE_URL")
WEB_HOST = os.getenv("WEB_HOST")
API_KEY = os.getenv("API_KEY")
```

**OneEnv導入後:**
```python
# 名前空間で整理
db_url = oneenv.env("database").get("URL")
web_host = oneenv.env("web").get("HOST")
api_key = oneenv.env("api").get("KEY")
```

## 仕組み

1. **発見**: OneEnvがインストールされたパッケージから環境変数テンプレートを発見
2. **生成**: 統合された`.env.example`ファイルを作成
3. **名前空間**: 変数を別々の名前空間にロードし、共通設定にフォールバック

## 高度な使用法: スキャフォールディングシステム 🏗️

OneEnvのインテリジェントスキャフォールディングシステムは、テンプレートをカテゴリ別に整理し、カスタムツール開発のための強力なAPIを提供します:

### インタラクティブなテンプレート発見
```bash
# 利用可能なテンプレートを発見
oneenv template --structure

# 変数数を含むカテゴリ詳細を取得
oneenv template --info Database

# オプションが提供する変数をプレビュー
oneenv template --preview Database postgres

# 特定の選択でテンプレート生成
oneenv template --generate Database:postgres VectorStore:chroma LLM:openai

# 自動化用JSON出力
oneenv template --structure --json
```

### カスタムツール用プログラマティックAPI 🛠️

OneEnvの包括的なAPIを使用して高度なスキャフォールディングツールを構築:

```python
import oneenv

# 発見API
structure = oneenv.get_all_template_structure()
print("利用可能なカテゴリ:", list(structure.keys()))
# 出力: {'Database': ['postgres', 'sqlite'], 'VectorStore': ['chroma', 'pinecone']}

# 検証API
if oneenv.has_category("Database"):
    options = oneenv.get_options("Database")
    print(f"Databaseオプション: {options}")

# 情報API
info = oneenv.get_category_info("Database")
print(f"総変数数: {info['total_variables']}")
print(f"Critical変数数: {info['critical_variables']}")

# プレビューAPI
preview = oneenv.get_option_preview("Database", "postgres")
for var_name, config in preview['variables'].items():
    print(f"{var_name}: {config['importance']} - {config['description']}")

# 生成API
selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM", "option": "openai"}
]

content = oneenv.generate_template(".env.example", selections)
print("選択されたコンポーネントでカスタムテンプレートを生成しました！")
```

### パッケージテンプレートの作成 📦

開発者は新しいスキャフォールディング形式を使用して発見可能なテンプレートを作成できます:

```python
# mypackage/templates.py
def database_template():
    return [
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL接続URL",
                    "default": "postgresql://user:pass@localhost:5432/dbname",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "接続プールサイズ",
                    "default": "10",
                    "required": False,
                    "importance": "important"
                }
            }
        },
        {
            "category": "Database",
            "option": "sqlite",
            "env": {
                "DATABASE_URL": {
                    "description": "SQLiteデータベースファイルパス",
                    "default": "sqlite:///app.db",
                    "required": True,
                    "importance": "critical"
                }
            }
        }
    ]
```

`pyproject.toml`に登録:
```toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
```

**主要機能:**
- **カテゴリベースの整理** - 関連テンプレートをグループ化（Database、VectorStore、LLMなど）
- **カテゴリごとの複数オプション** - 代替案を提供（postgres、sqlite、mysql）
- **重要度レベル** - より良いユーザーガイダンスのためのCritical、Important、Optional
- **自動発見** - ユーザーは`oneenv template --structure`で自動的にテンプレートを確認可能

## 詳細情報 📚

### ステップ別チュートリアル

#### 🌱 **基礎編** (各5-10分)
1. **[基本的なdotenv使用法](docs/tutorials/01-basic-dotenv_ja.md)** - 環境変数の基礎とOneEnvの基本操作を学習
2. **[自動テンプレート生成](docs/tutorials/02-template-generation_ja.md)** - パッケージからの環境変数自動発見とテンプレート生成を体験  
3. **[名前付き環境の基本](docs/tutorials/03-named-environments_ja.md)** - 名前空間管理とインテリジェントフォールバックをマスター

#### 🚀 **実践編** (各10-15分)
4. **[マルチサービス設定管理](docs/tutorials/04-multi-service_ja.md)** - 複数サービスを持つ複雑なアプリケーションの設定管理
5. **[プロジェクトテンプレートの作成](docs/tutorials/05-custom-templates_ja.md)** - 再利用可能なプロジェクト固有テンプレートの作成
6. **[本番環境でのベストプラクティス](docs/tutorials/06-production-tips_ja.md)** - 本番環境での安全な設定管理手法

#### ⚡ **高度編** (各15-20分)
7. **[プラグインの作成](docs/tutorials/07-plugin-development_ja.md)** - コミュニティで配布可能なOneEnvプラグインの開発
8. **[CI/CDとの連携](docs/tutorials/08-cicd-integration_ja.md)** - デプロイメントパイプラインでの設定管理自動化

#### 🚀 **新しいスキャフォールディング機能** (各10-20分)
9. **[新しいテンプレート作成](docs/tutorials/09-new-template-creation_ja.md)** - 新しいスキャフォールディング形式を使用した発見可能なテンプレート作成
10. **[スキャフォールディングツール作成](docs/tutorials/10-scaffolding-tool-creation_ja.md)** - OneEnvのAPIを使用したカスタムスキャフォールディングツール構築
11. **[実践ガイド](docs/tutorials/11-practical-guide_ja.md)** - RAGシステム、Webアプリなどの実例

### 📚 **ドキュメント**
- **[スキャフォールディング使用ガイド](docs/user-guides/scaffolding-usage_ja.md)** - スキャフォールディングシステムの包括的なガイド
- **[APIリファレンス](docs/api-reference/scaffolding-api_ja.md)** - カスタムツール開発のための完全なAPIドキュメント

**ここから開始:** [Step 1: 基本的なdotenv使用法](docs/tutorials/01-basic-dotenv_ja.md)

## ライセンス ⚖️

MIT License