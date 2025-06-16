# OneEnv 🌟

[![PyPI Downloads](https://static.pepy.tech/badge/oneenv)](https://pepy.tech/projects/oneenv)

**Python環境変数管理の新しいスタンダード。**

OneEnvはインストールされた全パッケージから環境変数テンプレートを自動発見し、
単一の `.env.example` ファイルに統合します。手動設定は一切不要です。

## OneEnvが開発を効率化する理由 🚀

**OneEnv導入前:**
- 😓 プロジェクトごとに `.env.example` ファイルを手作業で作成
- 😤 必要な環境変数を見つけるためドキュメントを漁る
- 😱 新しいパッケージ導入時に重要な設定を見落とし
- 🤯 プロジェクト間で一貫性のない環境変数フォーマット

**OneEnv導入後:**
- ✨ **全パッケージから環境変数を自動発見**
- 🎯 **1つのコマンド** で完全な `.env.example` ファイルを生成
- 🔄 **重複変数をスマートにマージ** し、詳細な説明も統合
- 📦 **プラグインエコシステム** でパッケージが独自テンプレートを提供
- 🛡️ **Pydantic による型安全性**

## 主要機能 🌟

### 🔌 **Entry-Points プラグインシステム**
パッケージが環境変数テンプレートを自動提供 - インストールするだけで使えます！

### 🎨 **スマートな重複処理**
複数のパッケージが同じ変数を定義していても、OneEnv が説明を統合し設定の一貫性を保ちます。

### ⚡ **ゼロ設定セットアップ**
OneEnv テンプレート対応パッケージをインストール？自動で発見されます。
インポートも手動登録も不要。

### 🔒 **型安全テンプレート**
Pydantic モデルによる実行時検証とより良いエラーメッセージ。

### 📋 **レガシーデコレータサポート**
既存の `@oneenv` デコレータは新しいプラグインシステムと完全互換で併用可能。

## 対応環境 🖥️

- **Python**: 3.10以上
- **対応OS**: Windows, macOS, Linux

## インストール 📦

pipコマンドで簡単にインストールできます：

```bash
pip install oneenv
```

開発モードでインストールする場合は、以下のコマンドを実行してください：

```bash
pip install -e .
```

## 超簡単な使い方 🎯

### ステップ1: OneEnv対応パッケージをインストール

```bash
pip install oneenv
pip install django-oneenv-plugin  # 例: Django テンプレート
pip install fastapi-oneenv-plugin # 例: FastAPI テンプレート
```

### ステップ2: 環境変数テンプレートを生成

```bash
oneenv template
```

**これだけ！** 🎉

OneEnv が自動的にインストール済みパッケージから環境変数を発見し、
完全な `.env.example` ファイルを作成します。

## 高度な使い方 🚀

### 🔍 発見された内容を確認

```bash
oneenv template -d
```

以下の情報が表示されます：
- 📦 発見されたプラグイン
- 🔄 パッケージ間で重複している変数
- ⚡ テンプレート生成プロセス

### 📝 カスタム出力ファイル

```bash
oneenv template -o my-custom.env
```

### 🔄 環境ファイルの比較

```bash
oneenv diff old.env new.env
```

## 実運用での活用 🔄

### CI/CDでの自動チェック

OneEnvを CI/CD パイプラインに統合することで、環境変数テンプレートの整合性を自動で維持できます。

#### GitHub Actions での例

```yaml
# .github/workflows/env-check.yml
name: Environment Template Check

on:
  pull_request:
    branches: [ main ]

jobs:
  check-env-template:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install oneenv
        pip install -r requirements.txt
    
    - name: Generate latest .env.example
      run: oneenv template -o .env.example.new
    
    - name: Check for differences
      run: |
        if ! diff -q .env.example .env.example.new > /dev/null; then
          echo "❌ .env.example is outdated!"
          echo "Run 'oneenv template' to update it."
          oneenv diff .env.example .env.example.new
          exit 1
        else
          echo "✅ .env.example is up to date!"
        fi
```

#### 自動更新ワークフロー

```yaml
# .github/workflows/env-update.yml
name: Auto-update Environment Template

on:
  schedule:
    - cron: '0 2 * * 1'  # 毎週月曜日 2:00 AM
  workflow_dispatch:

jobs:
  update-env-template:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install oneenv
        pip install -r requirements.txt
    
    - name: Update .env.example
      run: oneenv template
    
    - name: Create Pull Request
      uses: peter-evans/create-pull-request@v5
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        commit-message: "chore: update .env.example template"
        title: "Auto-update environment template"
        body: |
          📝 Environment template has been automatically updated.
          
          Changes detected in installed packages or their environment variable definitions.
          Please review the changes before merging.
        branch: chore/update-env-template
```

### Docker との連携

```dockerfile
# Dockerfile
FROM python:3.10

WORKDIR /app

# 依存関係をインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# OneEnvで環境変数テンプレートを生成
RUN pip install oneenv && oneenv template

COPY . .

CMD ["python", "app.py"]
```

## パッケージ開発者向け: OneEnvプラグインの作成 📦

### 方法1: モダンプラグインシステム（推奨） ⭐

自動発見される環境変数テンプレートを作成：

**1. テンプレート関数を作成:**

```python
# mypackage/templates.py

# オプションA: 新しいグループ形式（推奨） ⭐
def database_template():
    """データベース設定テンプレート"""
    return {
        "groups": {
            "Database": {
                "DATABASE_URL": {
                    "description": "データベース接続URL\n例: postgresql://user:pass@localhost:5432/db",
                    "default": "sqlite:///app.db",
                    "required": True,
                    "importance": "critical"
                },
                "DB_POOL_SIZE": {
                    "description": "データベース接続プールサイズ",
                    "default": "10",
                    "required": False,
                    "choices": ["5", "10", "20", "50"],
                    "importance": "important"
                }
            },
            "Cache": {
                "REDIS_URL": {
                    "description": "Redis接続URL",
                    "default": "redis://localhost:6379/0",
                    "importance": "important"
                }
            }
        }
    }

# オプションB: 従来形式（引き続きサポート）
def legacy_template():
    """レガシー形式テンプレート"""
    return {
        "DATABASE_URL": {
            "description": "データベース接続URL",
            "default": "sqlite:///app.db",
            "required": True,
            "group": "Database",
            "importance": "critical"
        }
    }
```

**2. pyproject.toml に登録:**

```toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
redis = "mypackage.templates:redis_template"
```

**3. 完了！** 🎉

ユーザーがあなたのパッケージをインストールすると、
OneEnv が自動的にテンプレートを発見します。

### 方法2: レガシーデコレータシステム 📋

後方互換性のため引き続きサポート:

```python
from oneenv import oneenv

@oneenv
def my_env_template():
    return {
        "MY_API_KEY": {
            "description": "サービスにアクセスするためのAPIキー",
            "default": "",
            "required": True
        },
        "MODE": {
            "description": "アプリケーションモード設定",
            "default": "development",
            "required": False,
            "choices": ["development", "production"]
        }
    }
```

## スマート重複変数処理 🎨

複数のパッケージが同じ環境変数を定義している場合、OneEnv が賢く統合します：

**出力例:**
```bash
# Auto-generated by OneEnv

# (Defined in: django-plugin, fastapi-plugin)
# Django データベース接続URL
# 例: postgresql://user:pass@localhost:5432/django_db
# From fastapi-plugin:
# FastAPI アプリケーション データベース接続
# サポート: PostgreSQL, MySQL, SQLite
# Required
DATABASE_URL=sqlite:///django.db

# (Defined in: redis-plugin)
# Redis 接続URL
# 例: redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/0
```

**動作原理:**
- ✅ **単一エントリ**: 各変数は1回のみ表示
- 📝 **説明の統合**: 全パッケージの説明が統合される
- ⚙️ **最初が勝ち**: 設定値（default、required、choices）は最初のパッケージの設定を使用
- 📋 **ソース追跡**: どのパッケージが各変数を定義しているかを表示

## テンプレートフィールドリファレンス 📚

### 従来形式拡張 (v0.3.0+)
```python
{
    "変数名": {
        "description": "この変数が何をするかの明確な説明",  # 必須
        "default": "デフォルト値",                    # オプション: デフォルト値
        "required": True,                           # オプション: 必須かどうか（デフォルト: False）
        "choices": ["選択肢1", "選択肢2"],              # オプション: 有効な選択肢
        "group": "カテゴリ名",                        # 新機能: グループ化のため
        "importance": "critical"                    # 新機能: critical/important/optional
    }
}
```

### 新しいグループ形式 (v0.3.1+) ⭐
```python
{
    "groups": {
        "Database": {
            "DATABASE_URL": {
                "description": "データベース接続URL",
                "default": "postgresql://localhost:5432/mydb",
                "required": True,
                "importance": "critical"
            },
            "DB_POOL_SIZE": {
                "description": "最大データベース接続数",
                "default": "10",
                "importance": "important"
            }
        },
        "Security": {
            "SECRET_KEY": {
                "description": "アプリケーションシークレットキー",
                "required": True,
                "importance": "critical"
            }
        }
    }
}
```

### 混合形式（両方サポート）
```python
{
    # 直接変数（デフォルトグループに割り当て）
    "GLOBAL_VAR": {
        "description": "グローバル設定",
        "group": "Application",  # 明示的グループ割り当て
        "importance": "critical"
    },
    
    # グループ化された変数
    "groups": {
        "Database": {
            "DATABASE_URL": {...}
        }
    }
}
```

### 重要度レベル
- **`critical`**: アプリケーション動作に必須の設定
- **`important`**: 本番環境で設定すべき項目
- **`optional`**: 細かい調整設定（デフォルトで十分）

## 実際の使用例 🌍

### Django + FastAPI + Redis プロジェクト
```bash
pip install oneenv django-oneenv fastapi-oneenv redis-oneenv
oneenv template
```

**生成される .env.example:**
```bash
# Auto-generated by OneEnv

# (Defined in: django-oneenv, fastapi-oneenv)
# Django データベース接続URL
# From fastapi-oneenv: FastAPI データベース接続
# Required
DATABASE_URL=sqlite:///django.db

# (Defined in: redis-oneenv)
# キャッシュとセッション用Redis接続
REDIS_URL=redis://localhost:6379/0

# (Defined in: django-oneenv)
# セキュリティ用Django シークレットキー
# Required
SECRET_KEY=your-secret-key-here
```

### カスタムプロジェクトテンプレート (v0.3.1拡張)
```python
# myproject/env_templates.py
from oneenv import oneenv

# 新しいグループ形式（推奨）
@oneenv
def custom_project_config():
    return {
        "groups": {
            "Application": {
                "PROJECT_NAME": {
                    "description": "あなたの素晴らしいプロジェクトの名前",
                    "default": "My Awesome App",
                    "required": True,
                    "importance": "critical"
                },
                "ENVIRONMENT": {
                    "description": "デプロイメント環境",
                    "default": "development",
                    "choices": ["development", "staging", "production"],
                    "importance": "important"
                }
            },
            "Logging": {
                "LOG_ROTATION_DAYS": {
                    "description": "ログファイルを保持する日数",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                },
                "LOG_LEVEL": {
                    "description": "アプリケーションログレベル",
                    "default": "INFO",
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR"],
                    "importance": "optional"
                }
            }
        }
    }

# 従来形式（引き続きサポート）
@oneenv
def legacy_project_config():
    return {
        "PROJECT_NAME": {
            "description": "あなたの素晴らしいプロジェクトの名前",
            "default": "My Awesome App",
            "required": True,
            "group": "Application",
            "importance": "critical"
        }
    }
```

## dotenvとの連携 🔄

OneEnvは [python-dotenv](https://github.com/theskumar/python-dotenv) をラップしているため、dotenvの全機能をそのまま利用できます：

```python
from oneenv import load_dotenv, dotenv_values

# 環境変数を読み込み
load_dotenv()

# 変数を辞書として取得
config = dotenv_values(".env")
```

## v0.3.1の新機能 🆕

### 🏗️ **新しいグループ形式**
1つの関数で複数のグループを定義でき、テンプレートの整理が非常に柔軟になりました：

```python
@oneenv
def complete_webapp_config():
    return {
        "groups": {
            "Database": {
                "DATABASE_URL": {...},
                "DB_POOL_SIZE": {...}
            },
            "Security": {
                "SECRET_KEY": {...},
                "JWT_EXPIRY": {...}
            },
            "Cache": {
                "REDIS_URL": {...}
            }
        }
    }
```

**メリット:**
- **📦 単一ソース**: 1つの関数で関連する全変数を定義
- **🎯 論理的グループ化**: 変数が自動的に目的別に整理される
- **🔄 後方互換性**: 従来形式も完全に動作
- **🚀 Entry-Points 最適化**: entry-point登録数を削減

## 過去のアップデート

### v0.2.0: 新しいプラグインシステム
- **Entry-points統合**: パッケージが自動的に環境変数テンプレートを提供
- **スマート重複処理**: 複数パッケージからの変数をインテリジェントにマージ
- **Pydantic型安全性**: クリアなエラーメッセージ付きの実行時検証
- **ゼロ設定**: 自動発見 - インポートや手動登録は不要

### 🔄 v0.1.xからの移行
既存の `@oneenv` デコレータは変更なしで引き続き動作します！新しいプラグインシステムは現在のセットアップと並行動作します。

**パッケージ開発者向け:** 自動発見のため `pyproject.toml` にentry-pointsの追加をご検討ください：
```toml
[project.entry-points."oneenv.templates"]
myfeature = "mypackage.templates:my_template_function"
```

## 他のツールとの比較 📊

| 機能 | OneEnv | python-dotenv | django-environ | pydantic-settings | dynaconf |
|------|--------|---------------|----------------|-------------------|----------|
| **自動テンプレート発見** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **プラグインシステム** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **重複変数の統合** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **型安全性** | ✅ | ❌ | ❌ | ✅ | ✅ |
| **CI/CD統合** | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| **設定ファイル生成** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **フレームワーク依存** | ❌ | ❌ | Django | ❌ | ❌ |
| **学習コスト** | 低 | 低 | 中 | 中 | 高 |
| **エコシステム** | 成長中 | 成熟 | 成熟 | 成長中 | 成熟 |

### OneEnv が特に優れている点

- **🔍 完全自動化**: インストールされたパッケージから設定を自動発見
- **🎯 ゼロ設定**: 手動でのテンプレート作成が不要
- **🔄 動的更新**: 新しいパッケージの追加時に自動で設定を更新
- **🤝 エコシステム連携**: パッケージ開発者が設定テンプレートを直接提供可能

## OneEnvの優位性 🎯

- **🚫 探し回らない**: 環境変数が自動的にドキュメント化される
- **⚡ ゼロセットアップ時間**: パッケージをインストール、1つのコマンド実行、完了
- **🔄 同期を保つ**: パッケージ更新と共に環境設定も自動更新
- **👥 チームの調和**: 全員が同じ環境セットアップを取得
- **📦 エコシステムの成長**: パッケージ作者がより良い設定体験を提供可能

## FAQ・トラブルシュート 🛠️

### よくある質問

#### Q. 特定の環境変数をテンプレートから除外したい
```python
# 除外したい変数がある場合は、プラグイン側で条件分岐を使用
@oneenv
def my_template():
    import os
    if os.getenv('EXCLUDE_SENSITIVE_VARS'):
        return {}  # 除外する場合は空の辞書を返す
    
    return {
        "SENSITIVE_VAR": {
            "description": "機密情報",
            "required": True
        }
    }
```

#### Q. 複数のプロジェクトで異なるテンプレートを使いたい
各プロジェクトのディレクトリで `oneenv template` を実行すると、そのプロジェクトにインストールされたパッケージに基づいてテンプレートが生成されます。

#### Q. プラグインが発見されない
```bash
# インストール済みプラグインを確認
oneenv template -d

# パッケージが正しくインストールされているか確認
pip list | grep oneenv
```

#### Q. Windows PowerShell で文字化けが発生する
```powershell
# UTF-8 エンコーディングを設定
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new()
oneenv template
```

#### Q. 重複した変数の優先順位を変更したい
現在、最初に発見されたパッケージの設定が優先されます。優先順位を変更するには、`pyproject.toml` での Entry-Points の登録順序を調整してください。

### トラブルシュート

#### プラグインが見つからない場合
1. パッケージが正しくインストールされているか確認
2. `pyproject.toml` の Entry-Points 設定を確認
3. 仮想環境が正しく有効化されているか確認

#### 生成されたテンプレートが期待と異なる場合
1. デバッグモードで実行: `oneenv template -d`
2. 重複している変数を確認
3. パッケージのバージョンを確認

#### パフォーマンスが遅い場合
大量のパッケージがインストールされている環境では、処理に時間がかかる場合があります。特定のパッケージのみを対象とする場合は、専用の仮想環境を作成することを推奨します。

## テストの実行 🧪

```bash
pytest tests
```

## コントリビュート 🤝

コントリビュートは大歓迎です！GitHubでPull RequestやIssueをお気軽にお送りください。

## ライセンス ⚖️

このプロジェクトはMITライセンスの下で公開されています。 