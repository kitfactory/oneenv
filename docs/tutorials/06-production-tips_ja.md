# Step 6: 本番環境でのベストプラクティス

**所要時間:** 15-20分  
**難易度:** 中級〜上級

## 学習目標

- 本番環境での安全な設定管理を学ぶ
- 秘密情報の適切な管理方法を理解する
- 環境別設定の効果的な分離方法を実践する
- セキュリティベストプラクティスを適用する

## 本番環境での課題

### 開発環境との違い
```bash
# 開発環境（問題なし）
DEBUG=True
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///dev.db

# 本番環境（要注意）
DEBUG=False                           # セキュリティ上必須
SECRET_KEY=super-strong-random-key    # 強力な秘密鍵必須
DATABASE_URL=postgresql://...        # 本番用データベース
```

### 秘密情報の管理
- **環境変数の暗号化**
- **アクセス制御**
- **監査ログ**
- **定期的なローテーション**

## 実践演習

### 演習1: 環境別設定の分離

1. プロジェクト構造を作成：
```bash
mkdir production-setup
cd production-setup
mkdir -p env/{development,staging,production}
```

2. 環境別設定ファイルの構造：

**env/development/common.env:**
```bash
# 開発環境共通設定
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG

# 開発用の緩い設定
SESSION_TIMEOUT=86400
RATE_LIMIT_ENABLED=False
```

**env/staging/common.env:**
```bash
# ステージング環境設定
ENVIRONMENT=staging
DEBUG=False
LOG_LEVEL=INFO

# 本番に近い設定
SESSION_TIMEOUT=3600
RATE_LIMIT_ENABLED=True
```

**env/production/common.env:**
```bash
# 本番環境設定
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING

# 厳格な設定
SESSION_TIMEOUT=1800
RATE_LIMIT_ENABLED=True
FORCE_HTTPS=True
```

3. セキュリティ設定の分離（`env/production/security.env`）：
```bash
# 本番環境セキュリティ設定
# 注意: このファイルは機密情報を含むため、適切に管理する

# 強力な秘密鍵（実際は環境変数または秘密管理システムから取得）
SECRET_KEY=${SECRET_KEY}
JWT_SECRET=${JWT_SECRET}
DATABASE_PASSWORD=${DATABASE_PASSWORD}

# セキュリティヘッダー設定
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
```

### 演習2: 安全な設定管理クラス

セキュリティを考慮した設定管理（`secure_config.py`）：

```python
import oneenv
import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path

class SecureConfig:
    """
    セキュアな設定管理クラス
    本番環境での安全な設定読み込みと検証を提供
    """
    
    def __init__(self, environment: str = None):
        self.environment = environment or os.getenv("ENVIRONMENT", "development")
        self.config_dir = Path("env") / self.environment
        self._sensitive_keys = {
            "SECRET_KEY", "JWT_SECRET", "DATABASE_PASSWORD", 
            "API_KEY", "PRIVATE_KEY", "TOKEN"
        }
        self._load_configuration()
        self._validate_production_settings()
    
    def _load_configuration(self):
        """環境に応じた設定ファイルを安全に読み込み"""
        try:
            # 共通設定
            common_file = self.config_dir / "common.env"
            if common_file.exists():
                oneenv.env().load_dotenv(str(common_file))
            
            # セキュリティ設定（本番環境のみ）
            if self.environment == "production":
                security_file = self.config_dir / "security.env"
                if security_file.exists():
                    oneenv.env("security").load_dotenv(str(security_file))
            
            # サービス別設定
            for service_file in self.config_dir.glob("*.env"):
                if service_file.name not in ["common.env", "security.env"]:
                    service_name = service_file.stem
                    oneenv.env(service_name).load_dotenv(str(service_file))
                    
        except Exception as e:
            logging.error(f"Configuration loading failed: {e}")
            raise
    
    def _validate_production_settings(self):
        """本番環境での必須設定を検証"""
        if self.environment != "production":
            return
        
        errors = []
        
        # 必須設定の確認
        required_settings = {
            "SECRET_KEY": "Application secret key is required",
            "DATABASE_URL": "Production database URL is required",
        }
        
        for key, message in required_settings.items():
            if not self.get(key):
                errors.append(message)
        
        # セキュリティ設定の確認
        security_checks = [
            (self.get_bool("DEBUG"), "DEBUG must be False in production"),
            (not self.get_bool("FORCE_HTTPS"), "HTTPS must be enforced in production"),
            (len(self.get("SECRET_KEY", "")) < 32, "SECRET_KEY must be at least 32 characters"),
        ]
        
        for check, message in security_checks:
            if check:
                errors.append(message)
        
        if errors:
            for error in errors:
                logging.error(f"Production validation error: {error}")
            raise ValueError(f"Production configuration is invalid: {errors}")
    
    def get(self, key: str, default: Any = None, service: str = None) -> Any:
        """設定値を安全に取得"""
        try:
            if service:
                value = oneenv.env(service).get(key, default)
            else:
                # セキュリティ設定から優先取得
                if self.environment == "production":
                    value = oneenv.env("security").get(key)
                    if value:
                        return value
                value = oneenv.env().get(key, default)
            
            # 機密情報のログ出力を防止
            if self._is_sensitive_key(key) and value:
                logging.debug(f"Retrieved sensitive config: {key}=***")
            else:
                logging.debug(f"Retrieved config: {key}={value}")
            
            return value
        except Exception as e:
            logging.error(f"Error retrieving config {key}: {e}")
            return default
    
    def get_bool(self, key: str, default: bool = False, service: str = None) -> bool:
        """真偽値を安全に取得"""
        value = self.get(key, str(default), service)
        return str(value).lower() in ('true', '1', 'yes', 'on')
    
    def get_int(self, key: str, default: int = 0, service: str = None) -> int:
        """整数値を安全に取得"""
        try:
            value = self.get(key, str(default), service)
            return int(value)
        except ValueError:
            logging.warning(f"Invalid integer value for {key}: {value}, using default {default}")
            return default
    
    def _is_sensitive_key(self, key: str) -> bool:
        """機密情報のキーかどうかを判定"""
        key_upper = key.upper()
        return any(sensitive in key_upper for sensitive in self._sensitive_keys)
    
    def get_database_url(self) -> str:
        """データベースURLを安全に構築"""
        if self.environment == "production":
            # 本番環境では環境変数から直接取得
            return os.getenv("DATABASE_URL") or self.get("DATABASE_URL", service="database")
        else:
            return self.get("DATABASE_URL", service="database")
    
    def validate_required_settings(self, required_keys: Dict[str, str]):
        """必須設定の存在を検証"""
        missing = []
        for key, description in required_keys.items():
            if not self.get(key):
                missing.append(f"{key} ({description})")
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")

# 使用例
def create_config() -> SecureConfig:
    """環境に応じた設定インスタンスを作成"""
    return SecureConfig()

# アプリケーション設定クラス
class AppConfig:
    """アプリケーション設定の統一インターface"""
    
    def __init__(self):
        self.config = create_config()
        
        # 必須設定の検証
        self.config.validate_required_settings({
            "SECRET_KEY": "Application secret key",
            "DATABASE_URL": "Database connection URL"
        })
    
    @property
    def debug(self) -> bool:
        return self.config.get_bool("DEBUG", False)
    
    @property
    def secret_key(self) -> str:
        return self.config.get("SECRET_KEY")
    
    @property
    def database_url(self) -> str:
        return self.config.get_database_url()
    
    @property
    def is_production(self) -> bool:
        return self.config.environment == "production"
    
    @property
    def log_level(self) -> str:
        return self.config.get("LOG_LEVEL", "INFO")
```

### 演習3: Docker本番環境設定

本番環境用Docker設定（`docker-compose.prod.yml`）：

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    environment:
      - ENVIRONMENT=production
    env_file:
      - ./env/production/common.env
      - ./env/production/app.env
    secrets:
      - db_password
      - secret_key
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  database:
    image: postgres:15
    environment:
      - POSTGRES_DB=${DATABASE_NAME}
      - POSTGRES_USER=${DATABASE_USER}
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backup:/backup
    restart: unless-stopped

secrets:
  db_password:
    external: true
  secret_key:
    external: true

volumes:
  postgres_data:
```

本番用Dockerfile（`Dockerfile.prod`）：

```dockerfile
FROM python:3.10-slim

# セキュリティアップデート
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 非rootユーザーで実行
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# 依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションをコピー
COPY --chown=appuser:appuser . .

# 機密ファイルの権限設定
RUN chmod 600 env/production/*.env

USER appuser

EXPOSE 8000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

### 演習4: 設定監査とモニタリング

設定監査スクリプト（`audit_config.py`）：

```python
import oneenv
import logging
import json
from datetime import datetime
from secure_config import SecureConfig

class ConfigAuditor:
    """設定監査クラス"""
    
    def __init__(self):
        self.config = SecureConfig()
        self.audit_log = []
    
    def audit_security_settings(self) -> Dict[str, Any]:
        """セキュリティ設定の監査"""
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "environment": self.config.environment,
            "checks": [],
            "warnings": [],
            "errors": []
        }
        
        # セキュリティチェック項目
        checks = [
            {
                "name": "Debug Mode",
                "check": lambda: not self.config.get_bool("DEBUG"),
                "severity": "error",
                "message": "DEBUG mode must be disabled in production"
            },
            {
                "name": "Secret Key Length",
                "check": lambda: len(self.config.get("SECRET_KEY", "")) >= 32,
                "severity": "error",
                "message": "SECRET_KEY must be at least 32 characters"
            },
            {
                "name": "HTTPS Enforcement",
                "check": lambda: self.config.get_bool("FORCE_HTTPS") if self.config.environment == "production" else True,
                "severity": "warning",
                "message": "HTTPS should be enforced in production"
            },
            {
                "name": "Session Timeout",
                "check": lambda: self.config.get_int("SESSION_TIMEOUT", 3600) <= 3600,
                "severity": "warning",
                "message": "Session timeout should be reasonable (≤ 1 hour)"
            }
        ]
        
        for check in checks:
            try:
                passed = check["check"]()
                result = {
                    "name": check["name"],
                    "passed": passed,
                    "severity": check["severity"],
                    "message": check["message"]
                }
                
                audit_results["checks"].append(result)
                
                if not passed:
                    if check["severity"] == "error":
                        audit_results["errors"].append(result)
                    else:
                        audit_results["warnings"].append(result)
                        
            except Exception as e:
                error_result = {
                    "name": check["name"],
                    "passed": False,
                    "severity": "error",
                    "message": f"Check failed: {e}"
                }
                audit_results["errors"].append(error_result)
        
        return audit_results
    
    def generate_audit_report(self) -> str:
        """監査レポートを生成"""
        results = self.audit_security_settings()
        
        report = f"""
OneEnv Configuration Audit Report
==================================
Environment: {results['environment']}
Timestamp: {results['timestamp']}

Summary:
- Total Checks: {len(results['checks'])}
- Errors: {len(results['errors'])}
- Warnings: {len(results['warnings'])}

"""
        
        if results['errors']:
            report += "🔴 ERRORS (Must be fixed):\n"
            for error in results['errors']:
                report += f"  - {error['name']}: {error['message']}\n"
            report += "\n"
        
        if results['warnings']:
            report += "🟡 WARNINGS (Should be reviewed):\n"
            for warning in results['warnings']:
                report += f"  - {warning['name']}: {warning['message']}\n"
            report += "\n"
        
        if not results['errors'] and not results['warnings']:
            report += "✅ All security checks passed!\n"
        
        return report
    
    def save_audit_log(self, filename: str = None):
        """監査ログを保存"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audit_log_{timestamp}.json"
        
        results = self.audit_security_settings()
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filename

# 監査実行スクリプト
def main():
    logging.basicConfig(level=logging.INFO)
    
    auditor = ConfigAuditor()
    
    # 監査レポート生成
    report = auditor.generate_audit_report()
    print(report)
    
    # ログファイル保存
    log_file = auditor.save_audit_log()
    print(f"Audit log saved to: {log_file}")
    
    # エラーがある場合は終了コード1で終了
    results = auditor.audit_security_settings()
    if results['errors']:
        exit(1)

if __name__ == "__main__":
    main()
```

### 演習5: 継続的な設定管理

設定変更の追跡スクリプト（`config_diff.py`）：

```python
import oneenv
import json
import hashlib
from pathlib import Path
from datetime import datetime

class ConfigTracker:
    """設定変更追跡クラス"""
    
    def __init__(self, tracking_file: str = "config_tracking.json"):
        self.tracking_file = Path(tracking_file)
        self.current_config = self._collect_current_config()
    
    def _collect_current_config(self) -> dict:
        """現在の設定を収集"""
        # テンプレートを生成して現在の設定を取得
        template_content = oneenv.template()
        
        # ハッシュ値を計算
        config_hash = hashlib.sha256(template_content.encode()).hexdigest()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "hash": config_hash,
            "content": template_content
        }
    
    def track_changes(self):
        """設定変更を追跡"""
        history = self._load_tracking_history()
        
        # 前回の設定と比較
        if history and history[-1]["hash"] == self.current_config["hash"]:
            print("No configuration changes detected.")
            return False
        
        # 変更を記録
        history.append(self.current_config)
        
        # 履歴を保存（最新10件のみ）
        history = history[-10:]
        self._save_tracking_history(history)
        
        print(f"Configuration change detected and tracked at {self.current_config['timestamp']}")
        return True
    
    def _load_tracking_history(self) -> list:
        """追跡履歴を読み込み"""
        if not self.tracking_file.exists():
            return []
        
        try:
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading tracking history: {e}")
            return []
    
    def _save_tracking_history(self, history: list):
        """追跡履歴を保存"""
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error saving tracking history: {e}")
    
    def show_diff(self):
        """最新の変更差分を表示"""
        history = self._load_tracking_history()
        
        if len(history) < 2:
            print("Not enough history to show diff.")
            return
        
        previous = history[-2]
        current = history[-1]
        
        print(f"Configuration diff between {previous['timestamp']} and {current['timestamp']}:")
        print("="*80)
        
        # 簡単な行ベースの差分表示
        prev_lines = previous['content'].split('\n')
        curr_lines = current['content'].split('\n')
        
        import difflib
        diff = difflib.unified_diff(
            prev_lines, 
            curr_lines, 
            fromfile=f"Previous ({previous['timestamp']})",
            tofile=f"Current ({current['timestamp']})",
            lineterm=''
        )
        
        for line in diff:
            print(line)

# 実行スクリプト
if __name__ == "__main__":
    import sys
    
    tracker = ConfigTracker()
    
    if len(sys.argv) > 1 and sys.argv[1] == "diff":
        tracker.show_diff()
    else:
        tracker.track_changes()
```

## 本番環境ベストプラクティス

### 1. **秘密情報の管理**
- 環境変数または秘密管理システムを使用
- 設定ファイルには機密情報を直接記載しない
- 定期的な秘密鍵のローテーション

### 2. **アクセス制御**
```bash
# 設定ファイルの適切な権限設定
chmod 600 env/production/*.env
chown app:app env/production/*.env
```

### 3. **監査とログ**
- 設定変更の追跡
- 定期的なセキュリティ監査
- 設定アクセスのログ記録

### 4. **バックアップ**
```bash
# 設定のバックアップ
backup_config() {
    timestamp=$(date +%Y%m%d_%H%M%S)
    tar -czf "config_backup_${timestamp}.tar.gz" env/
}
```

### 5. **デプロイ時の検証**
```bash
# デプロイ前の設定検証
python audit_config.py
if [ $? -ne 0 ]; then
    echo "Configuration validation failed!"
    exit 1
fi
```

## 次のステップ

本番環境でのベストプラクティスを学びました。次は、自分でプラグインを作成する方法を学びましょう。

**→ [Step 7: プラグインの作成](07-plugin-development.md)**

## よくある質問

### Q: 秘密情報はどこに保存すべきですか？
A: AWS Secrets Manager、Azure Key Vault、HashiCorp Vaultなどの秘密管理システムを使用することを推奨します。

### Q: 設定ファイルをGitで管理すべきですか？
A: テンプレートファイル（.env.example）はGitで管理し、実際の設定ファイル（.env）は.gitignoreに追加して管理しないでください。

### Q: 本番環境で設定を動的に変更したい場合は？
A: 設定変更後はアプリケーションの再起動が必要です。ダウンタイムを避けるため、ローリングアップデートを使用してください。

### Q: 設定の検証はいつ行うべきですか？
A: アプリケーション起動時、デプロイ時、定期的な監査のタイミングで実行することを推奨します。