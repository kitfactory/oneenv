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

詳細な例と高度な使い方については、[チュートリアル](docs/tutorials/)ディレクトリを参照してください。

## ライセンス ⚖️

MIT License