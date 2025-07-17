# Step 7: プラグインの作成

**所要時間:** 20-25分  
**難易度:** 上級

## 学習目標

- OneEnvプラグインの作成方法を理解する
- Entry-pointsシステムの活用方法を学ぶ
- 配布可能なパッケージとしてプラグインを作成する
- プラグインのテストとデバッグ方法を実践する

## プラグインシステムの概要

OneEnvのプラグインシステムは、Pythonの**Entry-points**メカニズムを使用して、パッケージが自動的に環境変数テンプレートを提供できるようにします。

### Entry-pointsとは
```toml
# pyproject.toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
web = "mypackage.templates:web_template"
```

これにより、パッケージをインストールするだけでOneEnvが自動的にテンプレートを発見できます。

## 実践演習

### 演習1: シンプルなプラグインの作成

1. プラグインプロジェクトを作成：
```bash
mkdir oneenv-database-plugin
cd oneenv-database-plugin
```

2. プロジェクト構造を作成：
```
oneenv-database-plugin/
├── pyproject.toml
├── README.md
├── src/
│   └── oneenv_database/
│       ├── __init__.py
│       └── templates.py
└── tests/
    └── test_templates.py
```

3. パッケージ設定（`pyproject.toml`）：
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "oneenv-database-plugin"
version = "1.0.0"
description = "Database environment templates for OneEnv"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
dependencies = [
    "oneenv>=0.3.0",
]
requires-python = ">=3.10"

[project.urls]
Homepage = "https://github.com/yourusername/oneenv-database-plugin"
Repository = "https://github.com/yourusername/oneenv-database-plugin"

# OneEnvプラグインとして登録
[project.entry-points."oneenv.templates"]
postgresql = "oneenv_database.templates:postgresql_template"
mysql = "oneenv_database.templates:mysql_template"
redis = "oneenv_database.templates:redis_template"
mongodb = "oneenv_database.templates:mongodb_template"

[tool.hatch.build.targets.wheel]
packages = ["src/oneenv_database"]
```

4. テンプレート実装（`src/oneenv_database/templates.py`）：
```python
"""
OneEnv Database Plugin Templates
データベース関連の環境変数テンプレートを提供
"""

def postgresql_template():
    """PostgreSQLデータベース設定テンプレート"""
    return {
        "groups": {
            "PostgreSQL Database": {
                "POSTGRES_HOST": {
                    "description": "PostgreSQLサーバーホスト\n例: localhost, db.example.com",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "POSTGRES_PORT": {
                    "description": "PostgreSQLサーバーポート",
                    "default": "5432",
                    "required": False,
                    "choices": ["5432", "5433", "5434"],
                    "importance": "important"
                },
                "POSTGRES_DB": {
                    "description": "データベース名",
                    "default": "myapp",
                    "required": True,
                    "importance": "critical"
                },
                "POSTGRES_USER": {
                    "description": "データベースユーザー名",
                    "default": "postgres",
                    "required": True,
                    "importance": "critical"
                },
                "POSTGRES_PASSWORD": {
                    "description": "データベースパスワード\n本番環境では強力なパスワードを使用",
                    "default": "password",
                    "required": True,
                    "importance": "critical"
                }
            },
            
            "PostgreSQL Connection": {
                "POSTGRES_POOL_SIZE": {
                    "description": "接続プールサイズ\nアプリケーションの負荷に応じて調整",
                    "default": "20",
                    "required": False,
                    "importance": "important"
                },
                "POSTGRES_MAX_OVERFLOW": {
                    "description": "最大オーバーフロー接続数",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                },
                "POSTGRES_TIMEOUT": {
                    "description": "接続タイムアウト（秒）",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    }

def mysql_template():
    """MySQL/MariaDBデータベース設定テンプレート"""
    return {
        "groups": {
            "MySQL Database": {
                "MYSQL_HOST": {
                    "description": "MySQLサーバーホスト",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "MYSQL_PORT": {
                    "description": "MySQLサーバーポート",
                    "default": "3306",
                    "required": False,
                    "importance": "important"
                },
                "MYSQL_DATABASE": {
                    "description": "データベース名",
                    "default": "myapp",
                    "required": True,
                    "importance": "critical"
                },
                "MYSQL_USER": {
                    "description": "データベースユーザー名",
                    "default": "mysql",
                    "required": True,
                    "importance": "critical"
                },
                "MYSQL_PASSWORD": {
                    "description": "データベースパスワード",
                    "default": "password",
                    "required": True,
                    "importance": "critical"
                },
                "MYSQL_CHARSET": {
                    "description": "文字セット",
                    "default": "utf8mb4",
                    "required": False,
                    "choices": ["utf8", "utf8mb4", "latin1"],
                    "importance": "important"
                }
            }
        }
    }

def redis_template():
    """Redisキャッシュ設定テンプレート"""
    return {
        "groups": {
            "Redis Cache": {
                "REDIS_HOST": {
                    "description": "Redisサーバーホスト",
                    "default": "localhost",
                    "required": True,
                    "importance": "important"
                },
                "REDIS_PORT": {
                    "description": "Redisサーバーポート",
                    "default": "6379",
                    "required": False,
                    "importance": "important"
                },
                "REDIS_DB": {
                    "description": "Redis データベース番号",
                    "default": "0",
                    "required": False,
                    "choices": ["0", "1", "2", "3", "4"],
                    "importance": "optional"
                },
                "REDIS_PASSWORD": {
                    "description": "Redis認証パスワード",
                    "default": "",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Redis Settings": {
                "REDIS_MAX_CONNECTIONS": {
                    "description": "最大接続数",
                    "default": "50",
                    "required": False,
                    "importance": "optional"
                },
                "REDIS_SOCKET_TIMEOUT": {
                    "description": "ソケットタイムアウト（秒）",
                    "default": "5",
                    "required": False,
                    "importance": "optional"
                },
                "REDIS_DECODE_RESPONSES": {
                    "description": "レスポンスのデコード",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            }
        }
    }

def mongodb_template():
    """MongoDBデータベース設定テンプレート"""
    return {
        "groups": {
            "MongoDB Database": {
                "MONGODB_HOST": {
                    "description": "MongoDBサーバーホスト",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "MONGODB_PORT": {
                    "description": "MongoDBサーバーポート",
                    "default": "27017",
                    "required": False,
                    "importance": "important"
                },
                "MONGODB_DATABASE": {
                    "description": "データベース名",
                    "default": "myapp",
                    "required": True,
                    "importance": "critical"
                },
                "MONGODB_USERNAME": {
                    "description": "データベースユーザー名",
                    "default": "",
                    "required": False,
                    "importance": "important"
                },
                "MONGODB_PASSWORD": {
                    "description": "データベースパスワード",
                    "default": "",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "MongoDB Options": {
                "MONGODB_AUTH_SOURCE": {
                    "description": "認証データベース",
                    "default": "admin",
                    "required": False,
                    "importance": "optional"
                },
                "MONGODB_REPLICA_SET": {
                    "description": "レプリカセット名",
                    "default": "",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    }
```

5. パッケージ初期化（`src/oneenv_database/__init__.py`）：
```python
"""
OneEnv Database Plugin

データベース関連の環境変数テンプレートを提供するOneEnvプラグイン
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# テンプレート関数をエクスポート
from .templates import (
    postgresql_template,
    mysql_template,
    redis_template,
    mongodb_template
)

__all__ = [
    "postgresql_template",
    "mysql_template", 
    "redis_template",
    "mongodb_template"
]
```

### 演習2: プラグインのテスト

1. テストファイルを作成（`tests/test_templates.py`）：
```python
import pytest
from oneenv_database.templates import (
    postgresql_template,
    mysql_template,
    redis_template,
    mongodb_template
)

class TestPostgreSQLTemplate:
    def test_postgresql_template_structure(self):
        """PostgreSQLテンプレートの構造をテスト"""
        template = postgresql_template()
        
        assert "groups" in template
        assert "PostgreSQL Database" in template["groups"]
        assert "PostgreSQL Connection" in template["groups"]
        
        # 必須フィールドの確認
        db_group = template["groups"]["PostgreSQL Database"]
        assert "POSTGRES_HOST" in db_group
        assert "POSTGRES_DB" in db_group
        assert "POSTGRES_USER" in db_group
        assert "POSTGRES_PASSWORD" in db_group
    
    def test_postgresql_required_fields(self):
        """PostgreSQL必須フィールドのテスト"""
        template = postgresql_template()
        db_group = template["groups"]["PostgreSQL Database"]
        
        required_fields = ["POSTGRES_HOST", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
        for field in required_fields:
            assert db_group[field]["required"] is True
            assert db_group[field]["importance"] == "critical"
    
    def test_postgresql_default_values(self):
        """PostgreSQLデフォルト値のテスト"""
        template = postgresql_template()
        db_group = template["groups"]["PostgreSQL Database"]
        
        assert db_group["POSTGRES_HOST"]["default"] == "localhost"
        assert db_group["POSTGRES_PORT"]["default"] == "5432"
        assert db_group["POSTGRES_USER"]["default"] == "postgres"

class TestMySQLTemplate:
    def test_mysql_template_structure(self):
        """MySQLテンプレートの構造をテスト"""
        template = mysql_template()
        
        assert "groups" in template
        assert "MySQL Database" in template["groups"]
        
        db_group = template["groups"]["MySQL Database"]
        assert "MYSQL_HOST" in db_group
        assert "MYSQL_DATABASE" in db_group
        assert "MYSQL_CHARSET" in db_group
    
    def test_mysql_charset_choices(self):
        """MySQL文字セット選択肢のテスト"""
        template = mysql_template()
        db_group = template["groups"]["MySQL Database"]
        
        charset_choices = db_group["MYSQL_CHARSET"]["choices"]
        assert "utf8mb4" in charset_choices
        assert "utf8" in charset_choices

class TestRedisTemplate:
    def test_redis_template_structure(self):
        """Redisテンプレートの構造をテスト"""
        template = redis_template()
        
        assert "groups" in template
        assert "Redis Cache" in template["groups"]
        assert "Redis Settings" in template["groups"]
    
    def test_redis_db_choices(self):
        """RedisデータベースID選択肢のテスト"""
        template = redis_template()
        cache_group = template["groups"]["Redis Cache"]
        
        db_choices = cache_group["REDIS_DB"]["choices"]
        assert len(db_choices) == 5
        assert "0" in db_choices

class TestMongoDBTemplate:
    def test_mongodb_template_structure(self):
        """MongoDBテンプレートの構造をテスト"""
        template = mongodb_template()
        
        assert "groups" in template
        assert "MongoDB Database" in template["groups"]
        assert "MongoDB Options" in template["groups"]
    
    def test_mongodb_optional_auth(self):
        """MongoDB認証設定のテスト"""
        template = mongodb_template()
        db_group = template["groups"]["MongoDB Database"]
        
        # ユーザー名とパスワードは任意
        assert db_group["MONGODB_USERNAME"]["required"] is False
        assert db_group["MONGODB_PASSWORD"]["required"] is False

class TestAllTemplates:
    def test_all_templates_callable(self):
        """全テンプレート関数が呼び出し可能かテスト"""
        templates = [
            postgresql_template,
            mysql_template,
            redis_template,
            mongodb_template
        ]
        
        for template_func in templates:
            result = template_func()
            assert isinstance(result, dict)
            assert "groups" in result
    
    def test_template_consistency(self):
        """テンプレートの一貫性をテスト"""
        templates = [
            postgresql_template(),
            mysql_template(),
            redis_template(),
            mongodb_template()
        ]
        
        for template in templates:
            assert "groups" in template
            
            for group_name, group_vars in template["groups"].items():
                for var_name, var_config in group_vars.items():
                    # 必須フィールドの確認
                    assert "description" in var_config
                    assert "importance" in var_config
                    
                    # 重要度レベルの確認
                    assert var_config["importance"] in ["critical", "important", "optional"]
```

2. テスト実行用設定：
```bash
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### 演習3: 高度なプラグイン機能

複数環境対応プラグイン（`src/oneenv_database/advanced_templates.py`）：

```python
"""
高度なデータベーステンプレート
環境別設定や動的テンプレート生成を含む
"""

import os

def environment_aware_postgresql_template():
    """
    環境を考慮したPostgreSQLテンプレート
    """
    environment = os.getenv("ENVIRONMENT", "development")
    
    base_template = {
        "groups": {
            "PostgreSQL Database": {
                "POSTGRES_HOST": {
                    "description": "PostgreSQLサーバーホスト",
                    "default": "localhost" if environment == "development" else "prod-db.example.com",
                    "required": True,
                    "importance": "critical"
                },
                "POSTGRES_DB": {
                    "description": "データベース名",
                    "default": f"myapp_{environment}",
                    "required": True,
                    "importance": "critical"
                }
            }
        }
    }
    
    # 本番環境でのみSSL設定を追加
    if environment == "production":
        base_template["groups"]["PostgreSQL Security"] = {
            "POSTGRES_SSL_MODE": {
                "description": "SSL接続モード",
                "default": "require",
                "required": True,
                "choices": ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"],
                "importance": "critical"
            },
            "POSTGRES_SSL_CERT": {
                "description": "SSL証明書パス",
                "default": "/etc/ssl/client-cert.pem",
                "required": False,
                "importance": "important"
            }
        }
    
    return base_template

def clustered_redis_template():
    """
    Redis クラスター対応テンプレート
    """
    return {
        "groups": {
            "Redis Cluster": {
                "REDIS_CLUSTER_ENABLED": {
                    "description": "Redisクラスターモード",
                    "default": "False",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "important"
                },
                "REDIS_CLUSTER_NODES": {
                    "description": "クラスターノード（カンマ区切り）\n例: node1:7000,node2:7000,node3:7000",
                    "default": "localhost:7000,localhost:7001,localhost:7002",
                    "required": False,
                    "importance": "important"
                },
                "REDIS_CLUSTER_REQUIRE_FULL_COVERAGE": {
                    "description": "フルカバレッジ要求",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            },
            
            "Redis Sentinel": {
                "REDIS_SENTINEL_ENABLED": {
                    "description": "Redis Sentinelモード",
                    "default": "False",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "important"
                },
                "REDIS_SENTINEL_HOSTS": {
                    "description": "Sentinelホスト（カンマ区切り）",
                    "default": "localhost:26379",
                    "required": False,
                    "importance": "important"
                },
                "REDIS_SENTINEL_SERVICE": {
                    "description": "Sentinelサービス名",
                    "default": "mymaster",
                    "required": False,
                    "importance": "important"
                }
            }
        }
    }

def database_url_builder_template():
    """
    データベースURL構築支援テンプレート
    """
    return {
        "groups": {
            "Database URL Builder": {
                "DATABASE_TYPE": {
                    "description": "データベースタイプ",
                    "default": "postgresql",
                    "required": True,
                    "choices": ["postgresql", "mysql", "sqlite", "mongodb"],
                    "importance": "critical"
                },
                "DATABASE_URL": {
                    "description": "完全なデータベースURL\n自動構築されない場合に使用",
                    "default": "",
                    "required": False,
                    "importance": "critical"
                }
            },
            
            "Auto-generated URLs": {
                "AUTO_BUILD_DATABASE_URL": {
                    "description": "データベースURLの自動構築",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            }
        }
    }
```

### 演習4: プラグインのパッケージ化とテスト

1. 開発環境でのインストール：
```bash
# 開発モードでインストール
pip install -e .

# 依存関係のインストール
pip install pytest oneenv
```

2. プラグインのテスト：
```bash
# テスト実行
pytest tests/ -v

# OneEnvでプラグインが認識されるかテスト
python -c "import oneenv; print(oneenv.template(debug=True))"
```

3. プラグインのデバッグスクリプト（`debug_plugin.py`）：
```python
import oneenv
import sys
from oneenv_database.templates import (
    postgresql_template,
    mysql_template,
    redis_template
)

def test_individual_templates():
    """個別テンプレートのテスト"""
    print("=== Individual Template Tests ===")
    
    templates = {
        "PostgreSQL": postgresql_template,
        "MySQL": mysql_template,
        "Redis": redis_template
    }
    
    for name, template_func in templates.items():
        print(f"\n--- {name} Template ---")
        try:
            result = template_func()
            print(f"✅ {name} template loaded successfully")
            print(f"Groups: {list(result['groups'].keys())}")
        except Exception as e:
            print(f"❌ {name} template failed: {e}")

def test_oneenv_integration():
    """OneEnv統合テスト"""
    print("\n=== OneEnv Integration Test ===")
    
    try:
        # OneEnvのデバッグモードでテンプレート生成
        debug_output = oneenv.template(debug=True)
        print("✅ OneEnv integration successful")
        
        # プラグインが発見されているか確認
        if "oneenv_database" in debug_output:
            print("✅ Plugin discovered by OneEnv")
        else:
            print("⚠️  Plugin not found in debug output")
            
    except Exception as e:
        print(f"❌ OneEnv integration failed: {e}")

def test_template_generation():
    """テンプレート生成テスト"""
    print("\n=== Template Generation Test ===")
    
    try:
        template_content = oneenv.template()
        print("✅ Template generation successful")
        
        # データベース関連の設定が含まれているか確認
        db_keywords = ["POSTGRES", "MYSQL", "REDIS", "MONGODB"]
        found_keywords = [kw for kw in db_keywords if kw in template_content]
        
        print(f"Found database keywords: {found_keywords}")
        
        if found_keywords:
            print("✅ Database templates are included")
        else:
            print("⚠️  No database templates found in output")
            
    except Exception as e:
        print(f"❌ Template generation failed: {e}")

if __name__ == "__main__":
    test_individual_templates()
    test_oneenv_integration()
    test_template_generation()
```

### 演習5: プラグインの配布

1. README.mdの作成：
```markdown
# OneEnv Database Plugin

OneEnv用のデータベース環境変数テンプレートプラグイン

## サポートデータベース

- PostgreSQL
- MySQL/MariaDB  
- Redis
- MongoDB

## インストール

```bash
pip install oneenv-database-plugin
```

## 使用方法

プラグインをインストール後、OneEnvが自動的にテンプレートを発見します：

```bash
oneenv template
```

## 提供されるテンプレート

### PostgreSQL
- 接続設定（ホスト、ポート、データベース名等）
- プール設定
- タイムアウト設定

### MySQL
- 接続設定
- 文字セット設定

### Redis
- 基本接続設定
- キャッシュ設定
- クラスター設定（高度な機能）

### MongoDB
- 接続設定
- 認証設定
- レプリカセット設定
```

2. パッケージのビルドと配布：
```bash
# ビルド
pip install build
python -m build

# テスト配布（TestPyPI）
pip install twine
twine upload --repository testpypi dist/*

# 本番配布（PyPI）
twine upload dist/*
```

## プラグイン開発のベストプラクティス

### 1. **一貫したネーミング**
```python
# プラグイン名: oneenv-{domain}-plugin
# パッケージ名: oneenv_{domain}
# Entry-points: {service} = "oneenv_{domain}.templates:{service}_template"
```

### 2. **適切なグループ化**
```python
"groups": {
    "Service Name": {  # 明確なサービス名
        # メイン設定
    },
    "Service Advanced": {  # 高度な設定
        # オプション設定
    }
}
```

### 3. **環境対応**
```python
def environment_aware_template():
    environment = os.getenv("ENVIRONMENT", "development")
    # 環境に応じたテンプレート生成
```

### 4. **包括的なテスト**
```python
# 構造テスト、デフォルト値テスト、統合テスト
```

### 5. **適切なドキュメント**
- README.md
- 設定例
- トラブルシューティング

## 次のステップ

プラグイン開発を学びました。最後に、CI/CDパイプラインとの連携方法を学びましょう。

**→ [Step 8: CI/CDとの連携](08-cicd-integration.md)**

## よくある質問

### Q: Entry-pointsが認識されない場合は？
A: パッケージを開発モード（`pip install -e .`）でインストールし、`oneenv template -d`で確認してください。

### Q: 既存のテンプレートと競合する場合は？
A: OneEnvは最初に発見されたテンプレートを優先します。Entry-pointsの名前を一意にしてください。

### Q: 動的テンプレートでエラーが発生する場合は？
A: テンプレート関数内で例外処理を追加し、安全なデフォルト値を返すようにしてください。

### Q: プラグインのバージョニングはどうすべきですか？
A: セマンティックバージョニングを使用し、OneEnvとの互換性を明記してください。