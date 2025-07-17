# Step 5: プロジェクトテンプレートの作成

**所要時間:** 10-15分  
**難易度:** 中級

## 学習目標

- カスタムプロジェクトテンプレートの作成方法を学ぶ
- 新しいGroups形式と従来形式の使い分けを理解する
- プロジェクト固有の設定テンプレートを設計する
- テンプレートの再利用可能な構造を作成する

## テンプレートの基本構造

OneEnvでは2つの形式でテンプレートを定義できます：

### 1. **新しいGroups形式（v0.3.1+）**
```python
@oneenv
def webapp_template():
    return {
        "groups": {
            "グループ名": {
                "変数名": {設定}
            }
        }
    }
```

### 2. **従来形式**
```python
@oneenv
def legacy_template():
    return {
        "変数名": {
            "group": "グループ名",
            # その他の設定
        }
    }
```

## 実践演習

### 演習1: ウェブアプリケーションテンプレート

1. プロジェクトディレクトリを作成：
```bash
mkdir custom-template-project
cd custom-template-project
```

2. カスタムテンプレートを作成（`project_templates.py`）：

```python
from oneenv import oneenv

@oneenv
def webapp_core_template():
    """
    ウェブアプリケーションの中核設定テンプレート
    新しいGroups形式を使用
    """
    return {
        "groups": {
            "Application": {
                "APP_NAME": {
                    "description": "アプリケーション名\n本番環境では正式なサービス名を設定してください",
                    "default": "My Web Application",
                    "required": True,
                    "importance": "critical"
                },
                "APP_VERSION": {
                    "description": "アプリケーションバージョン",
                    "default": "1.0.0",
                    "required": False,
                    "importance": "important"
                },
                "ENVIRONMENT": {
                    "description": "実行環境\n本番環境では必ずproductionを設定",
                    "default": "development",
                    "required": True,
                    "choices": ["development", "staging", "production"],
                    "importance": "critical"
                }
            },
            
            "Security": {
                "SECRET_KEY": {
                    "description": "アプリケーションの秘密鍵\n本番環境では強力なランダム文字列を使用",
                    "default": "dev-secret-key-change-in-production",
                    "required": True,
                    "importance": "critical"
                },
                "JWT_SECRET": {
                    "description": "JWT認証用の秘密鍵",
                    "default": "jwt-secret-key",
                    "required": True,
                    "importance": "critical"
                },
                "SESSION_TIMEOUT": {
                    "description": "セッションタイムアウト時間（秒）",
                    "default": "3600",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Database": {
                "DATABASE_URL": {
                    "description": "データベース接続URL\n例: postgresql://user:pass@localhost:5432/dbname",
                    "default": "sqlite:///app.db",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "データベース接続プール数",
                    "default": "20",
                    "required": False,
                    "importance": "important"
                },
                "DATABASE_TIMEOUT": {
                    "description": "データベース接続タイムアウト（秒）",
                    "default": "30",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Performance": {
                "WORKERS": {
                    "description": "ワーカープロセス数\nCPUコア数に合わせて調整",
                    "default": "4",
                    "required": False,
                    "choices": ["1", "2", "4", "8", "16"],
                    "importance": "important"
                },
                "MAX_REQUESTS": {
                    "description": "ワーカーあたりの最大リクエスト数",
                    "default": "1000",
                    "required": False,
                    "importance": "optional"
                }
            },
            
            "Logging": {
                "LOG_LEVEL": {
                    "description": "ログレベル\n本番環境ではINFO以上を推奨",
                    "default": "INFO",
                    "required": False,
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR"],
                    "importance": "optional"
                },
                "LOG_FORMAT": {
                    "description": "ログフォーマット",
                    "default": "json",
                    "required": False,
                    "choices": ["text", "json"],
                    "importance": "optional"
                }
            }
        }
    }

@oneenv
def external_services_template():
    """
    外部サービス連携設定テンプレート
    従来形式とGroups形式の混在例
    """
    return {
        # 直接変数定義（従来形式）
        "EXTERNAL_API_TIMEOUT": {
            "description": "外部API呼び出しタイムアウト（秒）",
            "default": "10",
            "required": False,
            "group": "External APIs",
            "importance": "important"
        },
        
        # Groups形式
        "groups": {
            "Email Service": {
                "SMTP_HOST": {
                    "description": "SMTPサーバーホスト",
                    "default": "localhost",
                    "required": True,
                    "importance": "important"
                },
                "SMTP_PORT": {
                    "description": "SMTPサーバーポート",
                    "default": "587",
                    "required": False,
                    "choices": ["25", "465", "587"],
                    "importance": "important"
                },
                "SMTP_USERNAME": {
                    "description": "SMTP認証ユーザー名",
                    "default": "",
                    "required": False,
                    "importance": "important"
                },
                "SMTP_PASSWORD": {
                    "description": "SMTP認証パスワード",
                    "default": "",
                    "required": False,
                    "importance": "critical"
                }
            },
            
            "File Storage": {
                "STORAGE_TYPE": {
                    "description": "ファイルストレージタイプ",
                    "default": "local",
                    "required": False,
                    "choices": ["local", "s3", "gcs"],
                    "importance": "important"
                },
                "STORAGE_BUCKET": {
                    "description": "ストレージバケット名（S3/GCS使用時）",
                    "default": "",
                    "required": False,
                    "importance": "important"
                },
                "STORAGE_REGION": {
                    "description": "ストレージリージョン",
                    "default": "us-east-1",
                    "required": False,
                    "importance": "optional"
                }
            },
            
            "Monitoring": {
                "SENTRY_DSN": {
                    "description": "Sentryエラートラッキング用DSN",
                    "default": "",
                    "required": False,
                    "importance": "important"
                },
                "HEALTH_CHECK_PATH": {
                    "description": "ヘルスチェックエンドポイント",
                    "default": "/health",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    }

# 従来形式の例
@oneenv  
def legacy_cache_template():
    """
    キャッシュ設定（従来形式の例）
    """
    return {
        "REDIS_URL": {
            "description": "Redis接続URL\n例: redis://localhost:6379/0",
            "default": "redis://localhost:6379/0",
            "required": True,
            "group": "Cache",
            "importance": "important"
        },
        "CACHE_DEFAULT_TIMEOUT": {
            "description": "デフォルトキャッシュタイムアウト（秒）",
            "default": "300",
            "required": False,
            "group": "Cache",
            "importance": "optional"
        },
        "CACHE_KEY_PREFIX": {
            "description": "キャッシュキーのプレフィックス",
            "default": "myapp:",
            "required": False,
            "group": "Cache",
            "importance": "optional"
        }
    }
```

### 演習2: プロジェクト特化型テンプレート

特定のプロジェクトタイプに特化したテンプレート：

```python
# specialized_templates.py
from oneenv import oneenv

@oneenv
def ecommerce_template():
    """
    ECサイト特化テンプレート
    """
    return {
        "groups": {
            "Payment": {
                "STRIPE_PUBLIC_KEY": {
                    "description": "Stripe公開可能キー",
                    "default": "pk_test_...",
                    "required": True,
                    "importance": "critical"
                },
                "STRIPE_SECRET_KEY": {
                    "description": "Stripeシークレットキー",
                    "default": "sk_test_...",
                    "required": True,
                    "importance": "critical"
                },
                "PAYMENT_CURRENCY": {
                    "description": "決済通貨",
                    "default": "JPY",
                    "required": False,
                    "choices": ["JPY", "USD", "EUR"],
                    "importance": "important"
                }
            },
            
            "Inventory": {
                "INVENTORY_ALERT_THRESHOLD": {
                    "description": "在庫アラート閾値",
                    "default": "10",
                    "required": False,
                    "importance": "important"
                },
                "AUTO_REORDER_ENABLED": {
                    "description": "自動発注機能の有効化",
                    "default": "False",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            },
            
            "Shipping": {
                "SHIPPING_API_URL": {
                    "description": "配送API URL",
                    "default": "https://api.shipping.com/v1",
                    "required": True,
                    "importance": "important"
                },
                "FREE_SHIPPING_THRESHOLD": {
                    "description": "送料無料の金額閾値",
                    "default": "5000",
                    "required": False,
                    "importance": "important"
                }
            }
        }
    }

@oneenv
def blog_template():
    """
    ブログアプリケーション特化テンプレート
    """
    return {
        "groups": {
            "Content": {
                "POSTS_PER_PAGE": {
                    "description": "1ページあたりの記事数",
                    "default": "10",
                    "required": False,
                    "choices": ["5", "10", "20", "50"],
                    "importance": "optional"
                },
                "ALLOW_COMMENTS": {
                    "description": "コメント機能の有効化",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "important"
                },
                "COMMENT_MODERATION": {
                    "description": "コメント承認制",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "important"
                }
            },
            
            "SEO": {
                "SITE_NAME": {
                    "description": "サイト名",
                    "default": "My Blog",
                    "required": True,
                    "importance": "critical"
                },
                "SITE_DESCRIPTION": {
                    "description": "サイト説明文",
                    "default": "技術ブログです",
                    "required": True,
                    "importance": "important"
                },
                "GOOGLE_ANALYTICS_ID": {
                    "description": "Google Analytics ID",
                    "default": "",
                    "required": False,
                    "importance": "optional"
                }
            },
            
            "Social": {
                "TWITTER_USERNAME": {
                    "description": "Twitterユーザー名",
                    "default": "",
                    "required": False,
                    "importance": "optional"
                },
                "FACEBOOK_PAGE_ID": {
                    "description": "Facebook ページID",
                    "default": "",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    }

@oneenv
def api_service_template():
    """
    APIサービス特化テンプレート
    """
    return {
        "groups": {
            "API Configuration": {
                "API_VERSION": {
                    "description": "APIバージョン",
                    "default": "v1",
                    "required": True,
                    "importance": "important"
                },
                "API_PREFIX": {
                    "description": "APIパスプレフィックス",
                    "default": "/api",
                    "required": False,
                    "importance": "important"
                },
                "CORS_ORIGINS": {
                    "description": "CORS許可オリジン（カンマ区切り）",
                    "default": "http://localhost:3000,http://localhost:8080",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Rate Limiting": {
                "RATE_LIMIT_PER_MINUTE": {
                    "description": "1分間あたりのリクエスト制限",
                    "default": "60",
                    "required": False,
                    "importance": "important"
                },
                "RATE_LIMIT_PER_HOUR": {
                    "description": "1時間あたりのリクエスト制限",
                    "default": "1000",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Documentation": {
                "ENABLE_DOCS": {
                    "description": "API ドキュメントの有効化",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                },
                "DOCS_URL": {
                    "description": "ドキュメントURL",
                    "default": "/docs",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    }
```

### 演習3: テンプレートのテストと生成

1. テンプレートを組み込んだスクリプト（`test_templates.py`）：

```python
# テンプレートをインポートして登録
import project_templates
import specialized_templates

import oneenv

# テンプレート生成
print("=== カスタムテンプレートのテスト ===")

# デバッグモードで生成
print("Debug mode output:")
print(oneenv.template(debug=True))

print("\n" + "="*50)
print("Generated .env.example:")
print("="*50)
print(oneenv.template())
```

2. 実行：
```bash
python test_templates.py
```

### 演習4: 条件付きテンプレート

環境や設定に応じて動的にテンプレートを変更：

```python
# conditional_templates.py
from oneenv import oneenv
import os

@oneenv
def conditional_template():
    """
    環境に応じて動的に変更されるテンプレート
    """
    environment = os.getenv("ENVIRONMENT", "development")
    
    base_template = {
        "groups": {
            "Application": {
                "APP_NAME": {
                    "description": "アプリケーション名",
                    "default": "My App",
                    "required": True,
                    "importance": "critical"
                }
            }
        }
    }
    
    # 本番環境でのみ追加される設定
    if environment == "production":
        base_template["groups"]["Production"] = {
            "SSL_CERT_PATH": {
                "description": "SSL証明書パス",
                "default": "/etc/ssl/cert.pem",
                "required": True,
                "importance": "critical"
            },
            "SSL_KEY_PATH": {
                "description": "SSL秘密鍵パス",
                "default": "/etc/ssl/key.pem",
                "required": True,
                "importance": "critical"
            }
        }
    
    # 開発環境でのみ追加される設定
    if environment == "development":
        base_template["groups"]["Development"] = {
            "DEBUG_MODE": {
                "description": "デバッグモード",
                "default": "True",
                "required": False,
                "choices": ["True", "False"],
                "importance": "optional"
            },
            "HOT_RELOAD": {
                "description": "ホットリロード機能",
                "default": "True",
                "required": False,
                "choices": ["True", "False"],
                "importance": "optional"
            }
        }
    
    return base_template

@oneenv
def feature_flags_template():
    """
    機能フラグを含むテンプレート
    """
    return {
        "groups": {
            "Feature Flags": {
                "FEATURE_NEW_UI": {
                    "description": "新しいUI機能の有効化",
                    "default": "False",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                },
                "FEATURE_BETA_PAYMENT": {
                    "description": "ベータ決済機能の有効化",
                    "default": "False",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                },
                "FEATURE_ANALYTICS": {
                    "description": "詳細アナリティクス機能",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            }
        }
    }
```

## テンプレート設計のベストプラクティス

### 1. **論理的なグループ化**
```python
# 良い例: 機能ごとにグループ化
"groups": {
    "Database": {...},
    "Cache": {...},
    "Security": {...}
}
```

### 2. **わかりやすい説明**
```python
"description": "データベース接続URL\n例: postgresql://user:pass@localhost:5432/dbname\n本番環境では強力なパスワードを使用"
```

### 3. **適切なデフォルト値**
```python
"default": "development",  # 安全なデフォルト値
"choices": ["development", "staging", "production"]  # 有効な選択肢を明示
```

### 4. **重要度の設定**
```python
"importance": "critical"  # critical/important/optional
```

### 5. **必須項目の明確化**
```python
"required": True  # 必須項目を明確に
```

## テンプレートの再利用

### 共通テンプレートの作成
```python
# common_templates.py
from oneenv import oneenv

@oneenv
def database_template():
    """再利用可能なデータベーステンプレート"""
    return {
        "groups": {
            "Database": {
                # 共通のデータベース設定
            }
        }
    }
```

### プロジェクト固有の拡張
```python
# project_specific.py
import common_templates  # 共通テンプレートをインポート

@oneenv
def project_specific_template():
    """プロジェクト固有の追加設定"""
    return {
        "groups": {
            "Project Specific": {
                # プロジェクト固有の設定
            }
        }
    }
```

## 次のステップ

カスタムテンプレートの作成方法を学びました。次は、本番環境でのベストプラクティスを学びましょう。

**→ [Step 6: 本番環境でのベストプラクティス](06-production-tips.md)**

## よくある質問

### Q: Groups形式と従来形式はどちらを使うべきですか？
A: 新規プロジェクトではGroups形式を推奨します。関連する変数をまとめやすく、可読性が向上します。

### Q: テンプレートを複数ファイルに分割できますか？
A: はい。複数のPythonファイルでテンプレートを定義し、それぞれをインポートすることで分割できます。

### Q: 動的にテンプレートを変更したい場合は？
A: テンプレート関数内で環境変数やその他の条件を確認し、動的に辞書を構築できます。

### Q: テンプレートの設定が反映されない場合は？
A: `oneenv template -d` でデバッグモードを使用し、テンプレートが正しく発見されているか確認してください。