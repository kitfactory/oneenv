#!/usr/bin/env python3
"""
重複変数の処理を実演するサンプル

複数のプラグインパッケージが同じ環境変数を定義した場合の
OneEnvの動作を確認するためのデモンストレーション
"""

from oneenv import oneenv, template

# Clear registry for clean demo
from oneenv.core import _oneenv_core
_oneenv_core._legacy_registry.clear()

# プラグインパッケージ1: Django用設定
@oneenv
def django_package():
    """Django用の環境変数テンプレート"""
    return {
        "DATABASE_URL": {
            "description": "Django用データベース接続URL\n例: postgresql://user:pass@localhost:5432/django_db",
            "default": "sqlite:///django.db",
            "required": True,
            "choices": None,
            "group": "Database",
            "importance": "critical"
        },
        "SECRET_KEY": {
            "description": "Djangoのシークレットキー\n本番環境では必ず変更してください",
            "default": "django-insecure-change-me",
            "required": True,
            "group": "Security",
            "importance": "critical"
        },
        "DEBUG": {
            "description": "Djangoデバッグモード",
            "default": "False",
            "required": False,
            "choices": ["True", "False"],
            "group": "Development",
            "importance": "important"
        }
    }

# プラグインパッケージ2: FastAPI用設定
@oneenv
def fastapi_package():
    """FastAPI用の環境変数テンプレート"""
    return {
        "DATABASE_URL": {
            "description": "FastAPI application database connection\nSupported: PostgreSQL, MySQL, SQLite",
            "default": "postgresql://user:pass@localhost:5432/fastapi_db", 
            "required": False,  # FastAPIでは必須ではない
            "choices": None,
            "group": "Database",
            "importance": "critical"
        },
        "SECRET_KEY": {
            "description": "JWT signing secret for FastAPI",
            "default": "",
            "required": True,
            "group": "Security",
            "importance": "critical"
        },
        "API_PREFIX": {
            "description": "API path prefix for FastAPI routes",
            "default": "/api/v1",
            "required": False,
            "group": "API",
            "importance": "important"
        }
    }

# プラグインパッケージ3: Redis用設定
@oneenv
def redis_package():
    """Redis用の環境変数テンプレート"""
    return {
        "REDIS_URL": {
            "description": "Redis接続URL\n例: redis://localhost:6379/0",
            "default": "redis://localhost:6379/0",
            "required": False,
            "group": "Cache",
            "importance": "important"
        },
        "REDIS_POOL_SIZE": {
            "description": "Redis接続プールサイズ",
            "default": "10",
            "required": False,
            "group": "Cache",
            "importance": "optional"
        }
    }

if __name__ == "__main__":
    print("🔧 OneEnv 重複変数処理デモンストレーション")
    print("=" * 50)
    
    # テンプレート生成（デバッグ情報付き）
    print("\n📋 発見されたテンプレートとプラグイン:")
    content = template(debug=True)
    
    print("\n📝 生成された .env.example:")
    print("=" * 50)
    print(content)
    
    print("\n🎯 重複変数の処理結果:")
    print("- DATABASE_URL: Django とFastAPI の両方で定義されているが、1箇所にのみ表示")
    print("- SECRET_KEY: Django とFastAPI の両方で定義されているが、1箇所にのみ表示")
    print("- 説明: 両方のパッケージからの説明が集約されている")
    print("- 設定値: 最初のパッケージ（Django）の設定を使用")
    print("- ソース: 両方のパッケージがソースとして記載")