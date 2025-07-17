# Step 3: 名前付き環境の基本

**所要時間:** 10-15分  
**難易度:** 初級〜中級

## 学習目標

- 名前付き環境の概念を理解する
- 名前空間による設定分離の実践
- フォールバック機能の活用方法を学ぶ
- 実際のプロジェクトでの使用パターンを理解する

## 従来の問題点

### 設定の混在
```python
import os

# 全ての設定が混在し、どれがどのコンポーネント用かわからない
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
WEB_SERVER_HOST = os.getenv("WEB_HOST", "0.0.0.0")
API_SERVER_HOST = os.getenv("API_HOST", "localhost")
CACHE_HOST = os.getenv("CACHE_HOST", "localhost")
TIMEOUT = os.getenv("TIMEOUT", "30")  # どのコンポーネントのタイムアウト？
```

### 環境ごとの設定管理の困難
```python
# 開発・ステージング・本番の設定が混在
if os.getenv("ENVIRONMENT") == "production":
    DATABASE_URL = os.getenv("PROD_DATABASE_URL")
    REDIS_URL = os.getenv("PROD_REDIS_URL")
elif os.getenv("ENVIRONMENT") == "staging":
    DATABASE_URL = os.getenv("STAGING_DATABASE_URL")
    REDIS_URL = os.getenv("STAGING_REDIS_URL")
# 設定が複雑に...
```

## OneEnvの名前付き環境

### 基本概念

OneEnvでは環境変数を**名前空間**で分離管理できます：

- **共通環境** (`oneenv.env()`): 全体で共有される設定
- **名前付き環境** (`oneenv.env("名前")`): 特定コンポーネントの設定
- **インテリジェントフォールバック**: 名前付き環境 → 共通環境 → OS環境の順で検索

## 実践演習

### 演習1: 基本的な名前付き環境

1. プロジェクトディレクトリを作成：
```bash
mkdir named-env-tutorial
cd named-env-tutorial
```

2. 環境ファイルを作成：

**common.env:**
```bash
# 共通設定
TIMEOUT=30
LOG_LEVEL=INFO
ENVIRONMENT=development
```

**database.env:**
```bash
# データベース設定
HOST=localhost
PORT=5432
NAME=myapp_db
USER=dbuser
PASSWORD=dbpass
```

**web.env:**
```bash
# Webサーバー設定
HOST=0.0.0.0
PORT=8000
WORKERS=4
```

**api.env:**
```bash
# APIサーバー設定
HOST=localhost
PORT=8080
RATE_LIMIT=100
```

3. 名前付き環境を使用（`named_env_demo.py`）：
```python
import oneenv

# 各環境に設定をロード
oneenv.env().load_dotenv("common.env")
oneenv.env("database").load_dotenv("database.env")
oneenv.env("web").load_dotenv("web.env")
oneenv.env("api").load_dotenv("api.env")

print("=== 設定値の取得 ===")

# データベース設定（database環境から）
db_config = {
    "host": oneenv.env("database").get("HOST"),
    "port": int(oneenv.env("database").get("PORT")),
    "name": oneenv.env("database").get("NAME"),
    "timeout": int(oneenv.env("database").get("TIMEOUT", "10"))  # 共通環境からフォールバック
}
print(f"Database: {db_config}")

# Webサーバー設定（web環境から）
web_config = {
    "host": oneenv.env("web").get("HOST"),
    "port": int(oneenv.env("web").get("PORT")),
    "workers": int(oneenv.env("web").get("WORKERS")),
    "log_level": oneenv.env("web").get("LOG_LEVEL", "WARNING")  # 共通環境からフォールバック
}
print(f"Web: {web_config}")

# API設定（api環境から）
api_config = {
    "host": oneenv.env("api").get("HOST"),
    "port": int(oneenv.env("api").get("PORT")),
    "rate_limit": int(oneenv.env("api").get("RATE_LIMIT")),
    "environment": oneenv.env("api").get("ENVIRONMENT", "unknown")  # 共通環境からフォールバック
}
print(f"API: {api_config}")
```

4. 実行：
```bash
python named_env_demo.py
```

**期待される出力:**
```
=== 設定値の取得 ===
Database: {'host': 'localhost', 'port': 5432, 'name': 'myapp_db', 'timeout': 30}
Web: {'host': '0.0.0.0', 'port': 8000, 'workers': 4, 'log_level': 'INFO'}
API: {'host': 'localhost', 'port': 8080, 'rate_limit': 100, 'environment': 'development'}
```

### 演習2: フォールバック機能の確認

フォールバック動作を確認してみましょう：

```python
# fallback_demo.py
import oneenv

# 共通環境のみロード
oneenv.env().load_dotenv("common.env")

print("=== フォールバック動作の確認 ===")

# データベース環境から設定取得（database.envはロードしていない）
db_timeout = oneenv.env("database").get("TIMEOUT")  # 共通環境から取得
db_host = oneenv.env("database").get("HOST", "default-host")  # デフォルト値を使用

print(f"Database timeout (from common): {db_timeout}")
print(f"Database host (default): {db_host}")

# 共通環境から直接取得
common_timeout = oneenv.env().get("TIMEOUT")
print(f"Common timeout: {common_timeout}")
```

### 演習3: 環境別設定の動的切り替え

環境に応じて設定を動的に切り替える例：

```python
# dynamic_env.py
import oneenv
import os

# 環境を判定
env_name = os.getenv("APP_ENV", "development")

print(f"=== 現在の環境: {env_name} ===")

# 共通設定をロード
oneenv.env().load_dotenv("common.env")

# 環境に応じて設定ファイルを選択
if env_name == "production":
    oneenv.env("database").load_dotenv("production.env")
elif env_name == "staging":
    oneenv.env("database").load_dotenv("staging.env")
else:
    oneenv.env("database").load_dotenv("database.env")

# 設定を取得
config = {
    "database_host": oneenv.env("database").get("HOST"),
    "database_port": oneenv.env("database").get("PORT"),
    "log_level": oneenv.env("database").get("LOG_LEVEL"),  # 共通環境からフォールバック
    "environment": env_name
}

print(f"Configuration: {config}")
```

## 高度な使用パターン

### パターン1: コンポーネント別設定管理

```python
# components_config.py
import oneenv

class DatabaseConfig:
    def __init__(self):
        oneenv.env().load_dotenv("common.env")
        oneenv.env("database").load_dotenv("database.env")
        
    @property
    def connection_url(self):
        host = oneenv.env("database").get("HOST", "localhost")
        port = oneenv.env("database").get("PORT", "5432")
        name = oneenv.env("database").get("NAME", "myapp")
        user = oneenv.env("database").get("USER", "user")
        password = oneenv.env("database").get("PASSWORD", "pass")
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    
    @property
    def timeout(self):
        return int(oneenv.env("database").get("TIMEOUT", "30"))

class WebConfig:
    def __init__(self):
        oneenv.env().load_dotenv("common.env")
        oneenv.env("web").load_dotenv("web.env")
    
    @property
    def bind_address(self):
        host = oneenv.env("web").get("HOST", "0.0.0.0")
        port = oneenv.env("web").get("PORT", "8000")
        return f"{host}:{port}"
    
    @property
    def workers(self):
        return int(oneenv.env("web").get("WORKERS", "1"))

# 使用例
db_config = DatabaseConfig()
web_config = WebConfig()

print(f"Database URL: {db_config.connection_url}")
print(f"Web bind: {web_config.bind_address}")
```

### パターン2: 設定バリデーション

```python
# validated_config.py
import oneenv

def validate_database_config():
    """データベース設定をバリデーション"""
    required_vars = ["HOST", "PORT", "NAME"]
    
    for var in required_vars:
        value = oneenv.env("database").get(var)
        if not value:
            raise ValueError(f"Required database config {var} is missing")
    
    # ポート番号の検証
    try:
        port = int(oneenv.env("database").get("PORT"))
        if not (1 <= port <= 65535):
            raise ValueError(f"Invalid port number: {port}")
    except ValueError as e:
        raise ValueError(f"Invalid port format: {e}")
    
    return True

# 使用例
oneenv.env().load_dotenv("common.env")
oneenv.env("database").load_dotenv("database.env")

try:
    validate_database_config()
    print("✅ Database configuration is valid")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
```

## 名前付き環境のメリット

### 1. **設定の論理的分離**
```python
# 明確にどのコンポーネントの設定かわかる
db_host = oneenv.env("database").get("HOST")
web_host = oneenv.env("web").get("HOST")
cache_host = oneenv.env("cache").get("HOST")
```

### 2. **設定の再利用**
```python
# 共通設定は自動でフォールバック
timeout = oneenv.env("database").get("TIMEOUT")  # 共通設定から
log_level = oneenv.env("web").get("LOG_LEVEL")   # 共通設定から
```

### 3. **環境ごとの柔軟な設定**
```python
# 環境ごとに異なる設定ファイルを使用可能
oneenv.env("database").load_dotenv(f"{env_name}_database.env")
```

### 4. **テストの分離**
```python
# テスト用の環境を分離
oneenv.env("test").load_dotenv("test.env")
test_db = oneenv.env("test").get("DATABASE_URL")
```

## 名前付き環境のベストプラクティス

### 1. **命名規則の統一**
- **コンポーネント名**: `database`, `web`, `api`, `cache`
- **環境名**: `development`, `staging`, `production`
- **機能名**: `auth`, `payment`, `logging`

### 2. **共通設定の活用**
共通で使用する設定は共通環境に配置：
```bash
# common.env
TIMEOUT=30
LOG_LEVEL=INFO
ENVIRONMENT=development
DEBUG=True
```

### 3. **設定ファイルの構造化**
```
env/
├── common.env          # 共通設定
├── database.env        # データベース設定
├── web.env            # Webサーバー設定
├── api.env            # API設定
└── production/        # 本番環境用
    ├── database.env
    ├── web.env
    └── api.env
```

## 次のステップ

名前付き環境の基本を学びました。次は、実際のマルチサービスアプリケーションでの設定管理を学びましょう。

**→ [Step 4: マルチサービス設定管理](04-multi-service.md)**

## よくある質問

### Q: 環境名にはどのような文字を使用できますか？
A: 環境名には英数字、アンダースコア、ハイフンが使用できます。Python変数名と同様の規則です。

### Q: 共通環境の設定を上書きしたい場合は？
A: 名前付き環境で同名の変数を定義すると、そちらが優先されます。

### Q: 環境変数が見つからない場合の動作は？
A: 名前付き環境 → 共通環境 → OS環境変数 → デフォルト値の順で検索されます。

### Q: 複数の.envファイルを同じ環境にロードできますか？
A: はい。`load_dotenv()`を複数回呼び出すことで、複数のファイルをロードできます。