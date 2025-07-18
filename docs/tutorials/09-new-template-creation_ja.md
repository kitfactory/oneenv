# チュートリアル 9: 新しいテンプレート作成方法

**所要時間:** 15-20分  
**対象:** パッケージ開発者  
**前提条件:** Python基礎、パッケージ開発の知識

## 概要

従来のgroups形式より優れた構造と柔軟性を提供する新しいScaffolding形式を使用してOneEnvテンプレートを作成する方法を学習します。

## 学習内容

- Scaffolding形式の構造を理解
- 複数オプションを持つカテゴリベースのテンプレート作成
- 重要度レベルと検証機能の活用
- entry-pointsによるテンプレート登録
- テンプレートのテスト・検証

## 1. Scaffolding形式の理解 (5分)

### 主要コンセプト

新しいScaffolding形式は**カテゴリ**と**オプション**を中心にテンプレートを整理します：

- **カテゴリ**: 高レベルのグループ化（例: "Database", "VectorStore"）
- **オプション**: 具体的な実装（例: "postgres", "sqlite"）
- **環境変数**: 各オプションの設定

### 基本構造

```python
def my_template():
    return [
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL接続URL",
                    "default": "postgresql://user:pass@localhost:5432/db",
                    "required": True,
                    "importance": "critical"
                }
            }
        }
    ]
```

### 重要度レベル

- **critical**: アプリケーション動作に不可欠
- **important**: 本番環境で設定すべき
- **optional**: 細かい調整設定（デフォルトで十分）

## 2. 最初のテンプレート作成 (5分)

パッケージ用のシンプルなデータベーステンプレートを作成しましょう。

### ステップ1: テンプレートファイルの作成

`my_package/templates.py`を作成：

```python
def database_template():
    """MyPackage用データベース設定テンプレート"""
    return [
        {
            "category": "Database",
            "option": "sqlite",
            "env": {
                "DATABASE_URL": {
                    "description": "SQLiteデータベースファイルパス",
                    "default": "sqlite:///app.db",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_TIMEOUT": {
                    "description": "データベース接続タイムアウト（秒）",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL接続URL",
                    "default": "postgresql://user:pass@localhost:5432/mydb",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "コネクションプールサイズ",
                    "default": "10",
                    "required": False,
                    "importance": "important"
                },
                "DATABASE_SSL_MODE": {
                    "description": "接続時のSSLモード",
                    "default": "prefer",
                    "required": False,
                    "importance": "optional",
                    "choices": ["require", "prefer", "disable"]
                }
            }
        }
    ]
```

### ステップ2: テンプレートのテスト

テンプレートを検証するテストスクリプトを作成：

```python
# test_template.py
from my_package.templates import database_template
from oneenv.models import validate_scaffolding_format

def test_template():
    template_data = database_template()
    
    try:
        validate_scaffolding_format(template_data)
        print("✅ テンプレート検証成功！")
        
        # 構造を表示
        categories = {}
        for item in template_data:
            category = item["category"]
            option = item["option"]
            if category not in categories:
                categories[category] = []
            categories[category].append(option)
        
        print(f"📊 テンプレート構造: {categories}")
        
    except Exception as e:
        print(f"❌ テンプレート検証失敗: {e}")

if __name__ == "__main__":
    test_template()
```

## 3. 高度なテンプレート機能 (5分)

### 複数カテゴリ

複数の技術カテゴリをまたがるテンプレートを作成：

```python
def full_stack_template():
    """完全なアプリケーションスタックテンプレート"""
    return [
        # データベースオプション
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "メインデータベース接続",
                    "default": "postgresql://user:pass@localhost:5432/app",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        
        # キャッシュオプション
        {
            "category": "Cache",
            "option": "redis",
            "env": {
                "REDIS_URL": {
                    "description": "Redisサーバー接続",
                    "default": "redis://localhost:6379/0",
                    "required": False,
                    "importance": "important"
                },
                "REDIS_MAX_CONNECTIONS": {
                    "description": "Redis最大接続数",
                    "default": "50",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # APIオプション
        {
            "category": "API",
            "option": "fastapi",
            "env": {
                "API_HOST": {
                    "description": "APIサーバーホスト",
                    "default": "0.0.0.0",
                    "required": False,
                    "importance": "important"
                },
                "API_PORT": {
                    "description": "APIサーバーポート",
                    "default": "8000",
                    "required": False,
                    "importance": "important"
                },
                "API_WORKERS": {
                    "description": "ワーカープロセス数",
                    "default": "4",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    ]
```

### 検証と選択肢

ユーザーエクスペリエンス向上のための検証機能を使用：

```python
def api_template():
    return [
        {
            "category": "API",
            "option": "production",
            "env": {
                "LOG_LEVEL": {
                    "description": "アプリケーションログレベル",
                    "default": "INFO",
                    "required": False,
                    "importance": "important",
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                },
                "ENVIRONMENT": {
                    "description": "デプロイメント環境",
                    "default": "production",
                    "required": True,
                    "importance": "critical",
                    "choices": ["development", "staging", "production"]
                }
            }
        }
    ]
```

## 4. Entry-points登録 (3分)

### ステップ1: pyproject.tomlの更新

OneEnv entry-pointsにテンプレートを追加：

```toml
[project.entry-points."oneenv.templates"]
database = "my_package.templates:database_template"
fullstack = "my_package.templates:full_stack_template"
api = "my_package.templates:api_template"
```

### ステップ2: 登録テスト

パッケージインストール後に登録をテスト：

```bash
# 開発モードでパッケージをインストール
pip install -e .

# OneEnvがテンプレートを見つけられるかチェック
oneenv template --structure
```

出力にカテゴリが表示されるはずです。

## 5. 実践演習 (2分)

自分のパッケージ用のテンプレートを作成：

1. **カテゴリを特定** パッケージに必要なもの（Database、Cache、APIなど）
2. **オプションを定義** 各カテゴリ用（postgres/mysql、redis/memcachedなど）
3. **環境変数をリスト** 各オプションが必要とするもの
4. **重要度レベルを設定**（critical/important/optional）
5. **検証を追加** 適切な場所でchoicesを使用

### 演習例

Webスクレイピングパッケージ用のテンプレート作成：

```python
def scraper_template():
    return [
        {
            "category": "Storage",
            "option": "filesystem",
            "env": {
                "STORAGE_PATH": {
                    "description": "スクレイピングデータ保存ディレクトリ",
                    "default": "./scraped_data",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        {
            "category": "Storage", 
            "option": "s3",
            "env": {
                "AWS_BUCKET": {
                    "description": "スクレイピングデータ用S3バケット",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "AWS_ACCESS_KEY_ID": {
                    "description": "AWSアクセスキー",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        {
            "category": "Rate_Limiting",
            "option": "basic",
            "env": {
                "REQUESTS_PER_SECOND": {
                    "description": "1秒あたりの最大リクエスト数",
                    "default": "1",
                    "required": False,
                    "importance": "important"
                },
                "DELAY_BETWEEN_REQUESTS": {
                    "description": "リクエスト間の遅延（秒）",
                    "default": "1.0",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    ]
```

## 新形式の利点

✅ **より良い整理**: カテゴリとオプションで明確な構造を提供  
✅ **柔軟な選択**: ユーザーが特定の組み合わせを選択可能  
✅ **重要度階層**: 重要な設定が強調表示される  
✅ **検証サポート**: 選択肢と必須フィールドでエラーを防止  
✅ **発見しやすさ**: CLIツールでオプションを簡単に探索  

## 次のステップ

- **チュートリアル10**: テンプレートを使用するscaffoldingツールの作成方法を学習
- **チュートリアル11**: 実際のプロジェクトでの実践例を確認
- 既存テンプレートの参考確認: `oneenv template --structure`

## クイックリファレンス

### テンプレート構造
```python
{
    "category": "CategoryName",
    "option": "option_name", 
    "env": {
        "VAR_NAME": {
            "description": "変数の説明",
            "default": "デフォルト値",
            "required": True|False,
            "importance": "critical"|"important"|"optional",
            "choices": ["選択肢1", "選択肢2"]  # オプション
        }
    }
}
```

### Entry-points登録
```toml
[project.entry-points."oneenv.templates"]
template_name = "package.module:function_name"
```

---

**🎉 おめでとうございます！** 新しいScaffolding形式を使用してOneEnvテンプレートを作成する方法をマスターしました。作成したテンプレートはユーザーやscaffoldingツールから自動的に発見可能になります。