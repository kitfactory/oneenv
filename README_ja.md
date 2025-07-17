# OneEnv 🌟

[![PyPI Downloads](https://static.pepy.tech/badge/oneenv)](https://pepy.tech/projects/oneenv)

**Python環境変数管理をシンプルに。**

OneEnvはインストールされたパッケージから環境変数テンプレートを自動発見し、名前空間で管理します。

## 中核機能 🎯

### 1. パッケージ環境変数発見 📦
インストールされた全パッケージから環境変数テンプレートを自動収集 - 手動設定不要。

### 2. 名前空間管理 🏷️
サービス/コンポーネント別に環境変数を整理し、インテリジェントなフォールバック機能。

## インストール 📦

```bash
pip install oneenv
```

## クイックスタート 🚀

### 環境変数テンプレート生成
```bash
oneenv template
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

## パッケージ開発者向け 📦

ユーザーが自動で発見できるテンプレートを作成:

```python
# mypackage/templates.py
def database_template():
    return {
        "groups": {
            "Database": {
                "DATABASE_URL": {
                    "description": "データベース接続URL",
                    "default": "sqlite:///app.db",
                    "required": True
                }
            }
        }
    }
```

`pyproject.toml`に登録:
```toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
```

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

**ここから開始:** [Step 1: 基本的なdotenv使用法](docs/tutorials/01-basic-dotenv_ja.md)

## ライセンス ⚖️

MIT License