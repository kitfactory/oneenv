# Step 4: マルチサービス設定管理

**所要時間:** 15-20分  
**難易度:** 中級

## 学習目標

- マルチサービスアプリケーションでの設定管理を学ぶ
- サービス間での設定共有と分離のバランスを理解する
- Docker Composeとの連携パターンを実践する
- マイクロサービス環境での設定管理を体験する

## 想定シナリオ

ECサイトを構成する以下のサービスの設定管理：

- **Web Frontend** (React/Next.js)
- **API Backend** (FastAPI/Django)
- **Database** (PostgreSQL)
- **Cache** (Redis)
- **Worker** (Celery)
- **Monitoring** (Prometheus/Grafana)

## プロジェクト構造

```
ecommerce-app/
├── docker-compose.yml
├── env/
│   ├── common.env          # 共通設定
│   ├── web.env            # Web frontend
│   ├── api.env            # API backend
│   ├── database.env       # Database
│   ├── cache.env          # Redis cache
│   ├── worker.env         # Background worker
│   └── monitoring.env     # Monitoring
├── services/
│   ├── web/
│   ├── api/
│   ├── worker/
│   └── monitoring/
└── config.py              # 設定管理モジュール
```

## 実践演習

### 演習1: 環境ファイルの設計

1. プロジェクトディレクトリを作成：
```bash
mkdir ecommerce-app
cd ecommerce-app
mkdir env services
```

2. 共通設定ファイル（`env/common.env`）：
```bash
# 共通設定
PROJECT_NAME=ECommerce Platform
ENVIRONMENT=development
LOG_LEVEL=INFO
TIMEZONE=Asia/Tokyo

# セキュリティ
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET=jwt-secret-key

# 外部サービス
SMTP_HOST=localhost
SMTP_PORT=587
```

3. データベース設定（`env/database.env`）：
```bash
# PostgreSQL設定
HOST=localhost
PORT=5432
NAME=ecommerce_db
USER=postgres
PASSWORD=postgres_password

# 接続プール設定
POOL_SIZE=20
MAX_OVERFLOW=30
POOL_TIMEOUT=30

# バックアップ設定
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=7
```

4. API設定（`env/api.env`）：
```bash
# APIサーバー設定
HOST=0.0.0.0
PORT=8000
WORKERS=4

# API固有設定
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
RATE_LIMIT_PER_MINUTE=60
API_VERSION=v1

# 外部API
PAYMENT_API_URL=https://api.stripe.com/v1
SHIPPING_API_URL=https://api.shipping.com/v2
```

5. Web設定（`env/web.env`）：
```bash
# Webサーバー設定
HOST=0.0.0.0
PORT=3000

# フロントエンド設定
API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=ECommerce Platform
NEXT_PUBLIC_VERSION=1.0.0

# アセット設定
CDN_URL=https://cdn.example.com
STATIC_FILES_URL=/static
```

6. キャッシュ設定（`env/cache.env`）：
```bash
# Redis設定
HOST=localhost
PORT=6379
DB=0
PASSWORD=redis_password

# キャッシュ設定
DEFAULT_TIMEOUT=300
SESSION_TIMEOUT=3600
CART_TIMEOUT=1800

# Redis設定
MAX_CONNECTIONS=50
```

7. ワーカー設定（`env/worker.env`）：
```bash
# Celeryワーカー設定
CONCURRENCY=4
LOGLEVEL=INFO

# キュー設定
DEFAULT_QUEUE=default
EMAIL_QUEUE=email
REPORT_QUEUE=reports

# タスク設定
EMAIL_RETRY_DELAY=60
REPORT_TIMEOUT=300
```

### 演習2: 設定管理モジュールの作成

統一的な設定管理モジュール（`config.py`）：

```python
import oneenv
import os
from typing import Dict, Any

class ConfigBase:
    """設定基底クラス"""
    
    def __init__(self, service_name: str = None):
        self.service_name = service_name
        self._load_env_files()
    
    def _load_env_files(self):
        """環境ファイルをロード"""
        # 共通設定をロード
        oneenv.env().load_dotenv("env/common.env")
        
        # サービス固有設定をロード
        if self.service_name:
            oneenv.env(self.service_name).load_dotenv(f"env/{self.service_name}.env")
    
    def get(self, key: str, default: Any = None) -> str:
        """設定値を取得"""
        if self.service_name:
            return oneenv.env(self.service_name).get(key, default)
        return oneenv.env().get(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """整数設定値を取得"""
        value = self.get(key, str(default))
        return int(value)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """真偽値設定値を取得"""
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_list(self, key: str, separator: str = ',', default: list = None) -> list:
        """リスト設定値を取得"""
        if default is None:
            default = []
        value = self.get(key, separator.join(default))
        return [item.strip() for item in value.split(separator) if item.strip()]

class CommonConfig(ConfigBase):
    """共通設定"""
    
    def __init__(self):
        super().__init__()
    
    @property
    def project_name(self) -> str:
        return self.get("PROJECT_NAME", "Unknown Project")
    
    @property
    def environment(self) -> str:
        return self.get("ENVIRONMENT", "development")
    
    @property
    def log_level(self) -> str:
        return self.get("LOG_LEVEL", "INFO")
    
    @property
    def secret_key(self) -> str:
        return self.get("SECRET_KEY")
    
    @property
    def is_development(self) -> bool:
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"

class DatabaseConfig(ConfigBase):
    """データベース設定"""
    
    def __init__(self):
        super().__init__("database")
    
    @property
    def host(self) -> str:
        return self.get("HOST", "localhost")
    
    @property
    def port(self) -> int:
        return self.get_int("PORT", 5432)
    
    @property
    def name(self) -> str:
        return self.get("NAME", "app_db")
    
    @property
    def user(self) -> str:
        return self.get("USER", "postgres")
    
    @property
    def password(self) -> str:
        return self.get("PASSWORD")
    
    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
    
    @property
    def pool_size(self) -> int:
        return self.get_int("POOL_SIZE", 20)
    
    @property
    def timeout(self) -> int:
        # 共通設定からフォールバック
        return self.get_int("TIMEOUT", 30)

class APIConfig(ConfigBase):
    """API設定"""
    
    def __init__(self):
        super().__init__("api")
    
    @property
    def host(self) -> str:
        return self.get("HOST", "0.0.0.0")
    
    @property
    def port(self) -> int:
        return self.get_int("PORT", 8000)
    
    @property
    def workers(self) -> int:
        return self.get_int("WORKERS", 1)
    
    @property
    def cors_origins(self) -> list:
        return self.get_list("CORS_ORIGINS")
    
    @property
    def rate_limit(self) -> int:
        return self.get_int("RATE_LIMIT_PER_MINUTE", 60)
    
    @property
    def bind_address(self) -> str:
        return f"{self.host}:{self.port}"

class WebConfig(ConfigBase):
    """Web設定"""
    
    def __init__(self):
        super().__init__("web")
    
    @property
    def host(self) -> str:
        return self.get("HOST", "0.0.0.0")
    
    @property
    def port(self) -> int:
        return self.get_int("PORT", 3000)
    
    @property
    def api_base_url(self) -> str:
        return self.get("API_BASE_URL", "http://localhost:8000/api/v1")
    
    @property
    def cdn_url(self) -> str:
        return self.get("CDN_URL", "")

class CacheConfig(ConfigBase):
    """キャッシュ設定"""
    
    def __init__(self):
        super().__init__("cache")
    
    @property
    def host(self) -> str:
        return self.get("HOST", "localhost")
    
    @property
    def port(self) -> int:
        return self.get_int("PORT", 6379)
    
    @property
    def db(self) -> int:
        return self.get_int("DB", 0)
    
    @property
    def password(self) -> str:
        return self.get("PASSWORD")
    
    @property
    def url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"
    
    @property
    def default_timeout(self) -> int:
        return self.get_int("DEFAULT_TIMEOUT", 300)

class WorkerConfig(ConfigBase):
    """ワーカー設定"""
    
    def __init__(self):
        super().__init__("worker")
    
    @property
    def concurrency(self) -> int:
        return self.get_int("CONCURRENCY", 4)
    
    @property
    def log_level(self) -> str:
        # 共通設定からフォールバック
        return self.get("LOGLEVEL", self.get("LOG_LEVEL", "INFO"))
    
    @property
    def default_queue(self) -> str:
        return self.get("DEFAULT_QUEUE", "default")

# 設定インスタンスを作成
common = CommonConfig()
database = DatabaseConfig()
api = APIConfig()
web = WebConfig()
cache = CacheConfig()
worker = WorkerConfig()
```

### 演習3: 設定の使用例

各サービスでの設定使用例：

**APIサービス（`services/api/app.py`）:**
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config import common, database, api, cache
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title=common.project_name,
    version=api.get("API_VERSION", "1.0.0")
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": common.environment,
        "database": {
            "host": database.host,
            "port": database.port,
            "name": database.name
        },
        "cache": {
            "host": cache.host,
            "port": cache.port
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=api.host,
        port=api.port,
        workers=api.workers,
        log_level=common.log_level.lower()
    )
```

**ワーカーサービス（`services/worker/worker.py`）:**
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config import common, database, cache, worker
from celery import Celery

# Celeryアプリケーションを作成
celery_app = Celery(
    common.project_name,
    broker=cache.url,
    backend=cache.url
)

# 設定を適用
celery_app.conf.update(
    worker_concurrency=worker.concurrency,
    worker_log_level=worker.log_level,
    task_default_queue=worker.default_queue,
    timezone=common.get("TIMEZONE", "UTC")
)

@celery_app.task
def send_email(to: str, subject: str, body: str):
    """メール送信タスク"""
    print(f"Sending email to {to}: {subject}")
    # メール送信ロジック
    return {"status": "sent", "to": to}

@celery_app.task
def generate_report(report_type: str):
    """レポート生成タスク"""
    print(f"Generating {report_type} report")
    # レポート生成ロジック
    return {"status": "generated", "type": report_type}
```

### 演習4: Docker Composeとの連携

Docker Compose設定（`docker-compose.yml`）：

```yaml
version: '3.8'

services:
  database:
    image: postgres:15
    environment:
      - POSTGRES_DB=${DATABASE_NAME:-ecommerce_db}
      - POSTGRES_USER=${DATABASE_USER:-postgres}
      - POSTGRES_PASSWORD=${DATABASE_PASSWORD:-postgres_password}
    ports:
      - "${DATABASE_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  cache:
    image: redis:7
    command: redis-server --requirepass ${CACHE_PASSWORD:-redis_password}
    ports:
      - "${CACHE_PORT:-6379}:6379"
    volumes:
      - redis_data:/data

  api:
    build: ./services/api
    ports:
      - "${API_PORT:-8000}:8000"
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-development}
    env_file:
      - ./env/common.env
      - ./env/database.env
      - ./env/api.env
      - ./env/cache.env
    depends_on:
      - database
      - cache

  web:
    build: ./services/web
    ports:
      - "${WEB_PORT:-3000}:3000"
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-development}
    env_file:
      - ./env/common.env
      - ./env/web.env
    depends_on:
      - api

  worker:
    build: ./services/worker
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-development}
    env_file:
      - ./env/common.env
      - ./env/database.env
      - ./env/cache.env
      - ./env/worker.env
    depends_on:
      - database
      - cache

volumes:
  postgres_data:
  redis_data:
```

起動用スクリプト（`start.sh`）：
```bash
#!/bin/bash

# 環境変数を設定ファイルから読み込み
export $(grep -v '^#' env/common.env | xargs)
export $(grep -v '^#' env/database.env | sed 's/^/DATABASE_/' | xargs)
export $(grep -v '^#' env/api.env | sed 's/^/API_/' | xargs)
export $(grep -v '^#' env/web.env | sed 's/^/WEB_/' | xargs)
export $(grep -v '^#' env/cache.env | sed 's/^/CACHE_/' | xargs)

# Docker Composeで起動
docker-compose up --build
```

### 演習5: 設定の検証とテスト

設定検証スクリプト（`validate_config.py`）：

```python
import sys
from config import common, database, api, web, cache, worker

def validate_common_config():
    """共通設定の検証"""
    errors = []
    
    if not common.secret_key:
        errors.append("SECRET_KEY is required")
    
    if len(common.secret_key) < 32:
        errors.append("SECRET_KEY should be at least 32 characters")
    
    if common.environment not in ['development', 'staging', 'production']:
        errors.append("ENVIRONMENT must be development, staging, or production")
    
    return errors

def validate_database_config():
    """データベース設定の検証"""
    errors = []
    
    if not database.password:
        errors.append("Database PASSWORD is required")
    
    if not (1024 <= database.port <= 65535):
        errors.append("Database PORT must be between 1024 and 65535")
    
    if database.pool_size <= 0:
        errors.append("Database POOL_SIZE must be positive")
    
    return errors

def validate_api_config():
    """API設定の検証"""
    errors = []
    
    if not (1024 <= api.port <= 65535):
        errors.append("API PORT must be between 1024 and 65535")
    
    if api.workers <= 0:
        errors.append("API WORKERS must be positive")
    
    if api.rate_limit <= 0:
        errors.append("API RATE_LIMIT_PER_MINUTE must be positive")
    
    return errors

def main():
    """設定検証のメイン関数"""
    all_errors = []
    
    all_errors.extend(validate_common_config())
    all_errors.extend(validate_database_config())
    all_errors.extend(validate_api_config())
    
    if all_errors:
        print("❌ Configuration validation failed:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ All configurations are valid")
        
        # 設定サマリーを表示
        print(f"\n📋 Configuration Summary:")
        print(f"  Project: {common.project_name}")
        print(f"  Environment: {common.environment}")
        print(f"  Database: {database.host}:{database.port}/{database.name}")
        print(f"  API: {api.bind_address}")
        print(f"  Web: {web.host}:{web.port}")
        print(f"  Cache: {cache.host}:{cache.port}")

if __name__ == "__main__":
    main()
```

## マルチサービス設定管理のベストプラクティス

### 1. **設定の階層化**
```
共通設定 (common.env)
├── サービス固有設定 (service.env)
└── 環境固有設定 (production/service.env)
```

### 2. **設定の型安全性**
```python
# 型変換メソッドを提供
config.get_int("PORT", 8000)
config.get_bool("DEBUG", False)
config.get_list("CORS_ORIGINS")
```

### 3. **設定の検証**
```python
# 起動時に設定を検証
validate_config()
```

### 4. **環境固有の設定分離**
```bash
env/
├── development/
├── staging/
└── production/
```

### 5. **秘密情報の管理**
```python
# 秘密情報は別途管理
oneenv.env("secrets").load_dotenv("secrets.env")
```

## 次のステップ

マルチサービス設定管理を学びました。次は、独自のプロジェクトテンプレートの作成方法を学びましょう。

**→ [Step 5: プロジェクトテンプレートの作成](05-custom-templates.md)**

## よくある質問

### Q: サービス間で設定を共有したい場合は？
A: 共通設定ファイル（common.env）を使用し、各サービスで共通環境からフォールバックさせます。

### Q: 設定ファイルが多すぎて管理が大変です
A: 設定管理モジュールを作成し、プロパティベースのアクセスを提供することで管理を簡素化できます。

### Q: Docker環境で設定を動的に変更したい場合は？
A: 環境変数でオーバーライドするか、ボリュームマウントで設定ファイルを動的に変更できます。