# Step 6: Production Best Practices

**Duration:** 15-20 minutes  
**Difficulty:** Intermediate to Advanced

## Learning Objectives

- Learn secure configuration management for production environments
- Understand proper secret information management methods
- Practice effective environment-specific configuration separation
- Apply security best practices

## Production Environment Challenges

### Differences from Development Environment
```bash
# Development environment (acceptable)
DEBUG=True
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///dev.db

# Production environment (requires attention)
DEBUG=False                           # Security requirement
SECRET_KEY=super-strong-random-key    # Strong secret key required
DATABASE_URL=postgresql://...        # Production database
```

### Secret Information Management
- **Environment variable encryption**
- **Access control**
- **Audit logs**
- **Regular rotation**

## Hands-on Exercises

### Exercise 1: Environment-Specific Configuration Separation

1. Create project structure:
```bash
mkdir production-setup
cd production-setup
mkdir -p env/{development,staging,production}
```

2. Environment-specific configuration file structure:

**env/development/common.env:**
```bash
# Development environment common settings
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG

# Relaxed settings for development
SESSION_TIMEOUT=86400
RATE_LIMIT_ENABLED=False
```

**env/staging/common.env:**
```bash
# Staging environment settings
ENVIRONMENT=staging
DEBUG=False
LOG_LEVEL=INFO

# Production-like settings
SESSION_TIMEOUT=3600
RATE_LIMIT_ENABLED=True
```

**env/production/common.env:**
```bash
# Production environment settings
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING

# Strict settings
SESSION_TIMEOUT=1800
RATE_LIMIT_ENABLED=True
FORCE_HTTPS=True
```

3. Security configuration separation (`env/production/security.env`):
```bash
# Production environment security settings
# Note: This file contains sensitive information and should be managed appropriately

# Strong secret keys (in reality, obtain from environment variables or secret management systems)
SECRET_KEY=${SECRET_KEY}
JWT_SECRET=${JWT_SECRET}
DATABASE_PASSWORD=${DATABASE_PASSWORD}

# Security header settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
```

### Exercise 2: Secure Configuration Management Class

Security-conscious configuration management (`secure_config.py`):

```python
import oneenv
import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path

class SecureConfig:
    """
    Secure configuration management class
    Provides safe configuration loading and validation for production environments
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
        """Safely load configuration files based on environment"""
        try:
            # Common settings
            common_file = self.config_dir / "common.env"
            if common_file.exists():
                oneenv.env().load_dotenv(str(common_file))
            
            # Security settings (production only)
            if self.environment == "production":
                security_file = self.config_dir / "security.env"
                if security_file.exists():
                    oneenv.env("security").load_dotenv(str(security_file))
            
            # Service-specific settings
            for service_file in self.config_dir.glob("*.env"):
                if service_file.name not in ["common.env", "security.env"]:
                    service_name = service_file.stem
                    oneenv.env(service_name).load_dotenv(str(service_file))
                    
        except Exception as e:
            logging.error(f"Configuration loading failed: {e}")
            raise
    
    def _validate_production_settings(self):
        """Validate required settings for production environment"""
        if self.environment != "production":
            return
        
        errors = []
        
        # Check required settings
        required_settings = {
            "SECRET_KEY": "Application secret key is required",
            "DATABASE_URL": "Production database URL is required",
        }
        
        for key, message in required_settings.items():
            if not self.get(key):
                errors.append(message)
        
        # Security settings validation
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
        """Safely retrieve configuration values"""
        try:
            if service:
                value = oneenv.env(service).get(key, default)
            else:
                # Priority retrieval from security settings
                if self.environment == "production":
                    value = oneenv.env("security").get(key)
                    if value:
                        return value
                value = oneenv.env().get(key, default)
            
            # Prevent logging sensitive information
            if self._is_sensitive_key(key) and value:
                logging.debug(f"Retrieved sensitive config: {key}=***")
            else:
                logging.debug(f"Retrieved config: {key}={value}")
            
            return value
        except Exception as e:
            logging.error(f"Error retrieving config {key}: {e}")
            return default
    
    def get_bool(self, key: str, default: bool = False, service: str = None) -> bool:
        """Safely retrieve boolean values"""
        value = self.get(key, str(default), service)
        return str(value).lower() in ('true', '1', 'yes', 'on')
    
    def get_int(self, key: str, default: int = 0, service: str = None) -> int:
        """Safely retrieve integer values"""
        try:
            value = self.get(key, str(default), service)
            return int(value)
        except ValueError:
            logging.warning(f"Invalid integer value for {key}: {value}, using default {default}")
            return default
    
    def _is_sensitive_key(self, key: str) -> bool:
        """Determine if a key contains sensitive information"""
        key_upper = key.upper()
        return any(sensitive in key_upper for sensitive in self._sensitive_keys)
    
    def get_database_url(self) -> str:
        """Safely construct database URL"""
        if self.environment == "production":
            # In production, retrieve directly from environment variables
            return os.getenv("DATABASE_URL") or self.get("DATABASE_URL", service="database")
        else:
            return self.get("DATABASE_URL", service="database")
    
    def validate_required_settings(self, required_keys: Dict[str, str]):
        """Validate existence of required settings"""
        missing = []
        for key, description in required_keys.items():
            if not self.get(key):
                missing.append(f"{key} ({description})")
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")

# Usage example
def create_config() -> SecureConfig:
    """Create configuration instance based on environment"""
    return SecureConfig()

# Application configuration class
class AppConfig:
    """Unified interface for application configuration"""
    
    def __init__(self):
        self.config = create_config()
        
        # Validate required settings
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

### Exercise 3: Docker Production Environment Configuration

Production Docker configuration (`docker-compose.prod.yml`):

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

Production Dockerfile (`Dockerfile.prod`):

```dockerfile
FROM python:3.10-slim

# Security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . .

# Set permissions for sensitive files
RUN chmod 600 env/production/*.env

USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

### Exercise 4: Configuration Auditing and Monitoring

Configuration audit script (`audit_config.py`):

```python
import oneenv
import logging
import json
from datetime import datetime
from secure_config import SecureConfig

class ConfigAuditor:
    """Configuration audit class"""
    
    def __init__(self):
        self.config = SecureConfig()
        self.audit_log = []
    
    def audit_security_settings(self) -> Dict[str, Any]:
        """Audit security settings"""
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "environment": self.config.environment,
            "checks": [],
            "warnings": [],
            "errors": []
        }
        
        # Security check items
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
        """Generate audit report"""
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
        """Save audit log"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audit_log_{timestamp}.json"
        
        results = self.audit_security_settings()
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filename

# Audit execution script
def main():
    logging.basicConfig(level=logging.INFO)
    
    auditor = ConfigAuditor()
    
    # Generate audit report
    report = auditor.generate_audit_report()
    print(report)
    
    # Save log file
    log_file = auditor.save_audit_log()
    print(f"Audit log saved to: {log_file}")
    
    # Exit with code 1 if there are errors
    results = auditor.audit_security_settings()
    if results['errors']:
        exit(1)

if __name__ == "__main__":
    main()
```

### Exercise 5: Continuous Configuration Management

Configuration change tracking script (`config_diff.py`):

```python
import oneenv
import json
import hashlib
from pathlib import Path
from datetime import datetime

class ConfigTracker:
    """Configuration change tracking class"""
    
    def __init__(self, tracking_file: str = "config_tracking.json"):
        self.tracking_file = Path(tracking_file)
        self.current_config = self._collect_current_config()
    
    def _collect_current_config(self) -> dict:
        """Collect current configuration"""
        # Generate template to get current configuration
        template_content = oneenv.template()
        
        # Calculate hash value
        config_hash = hashlib.sha256(template_content.encode()).hexdigest()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "hash": config_hash,
            "content": template_content
        }
    
    def track_changes(self):
        """Track configuration changes"""
        history = self._load_tracking_history()
        
        # Compare with previous configuration
        if history and history[-1]["hash"] == self.current_config["hash"]:
            print("No configuration changes detected.")
            return False
        
        # Record change
        history.append(self.current_config)
        
        # Save history (keep only latest 10 entries)
        history = history[-10:]
        self._save_tracking_history(history)
        
        print(f"Configuration change detected and tracked at {self.current_config['timestamp']}")
        return True
    
    def _load_tracking_history(self) -> list:
        """Load tracking history"""
        if not self.tracking_file.exists():
            return []
        
        try:
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading tracking history: {e}")
            return []
    
    def _save_tracking_history(self, history: list):
        """Save tracking history"""
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error saving tracking history: {e}")
    
    def show_diff(self):
        """Show latest change diff"""
        history = self._load_tracking_history()
        
        if len(history) < 2:
            print("Not enough history to show diff.")
            return
        
        previous = history[-2]
        current = history[-1]
        
        print(f"Configuration diff between {previous['timestamp']} and {current['timestamp']}:")
        print("="*80)
        
        # Simple line-based diff display
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

# Execution script
if __name__ == "__main__":
    import sys
    
    tracker = ConfigTracker()
    
    if len(sys.argv) > 1 and sys.argv[1] == "diff":
        tracker.show_diff()
    else:
        tracker.track_changes()
```

## Production Environment Best Practices

### 1. **Secret Information Management**
- Use environment variables or secret management systems
- Never store sensitive information directly in configuration files
- Regular secret key rotation

### 2. **Access Control**
```bash
# Proper permissions for configuration files
chmod 600 env/production/*.env
chown app:app env/production/*.env
```

### 3. **Auditing and Logging**
- Track configuration changes
- Regular security audits
- Log configuration access

### 4. **Backup**
```bash
# Configuration backup
backup_config() {
    timestamp=$(date +%Y%m%d_%H%M%S)
    tar -czf "config_backup_${timestamp}.tar.gz" env/
}
```

### 5. **Deployment Validation**
```bash
# Configuration validation before deployment
python audit_config.py
if [ $? -ne 0 ]; then
    echo "Configuration validation failed!"
    exit 1
fi
```

## Next Steps

You've learned production environment best practices. Next, let's learn how to create your own plugins.

**→ [Step 7: Plugin Development](07-plugin-development.md)**

## Frequently Asked Questions

### Q: Where should I store secret information?
A: We recommend using secret management systems like AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault.

### Q: Should I manage configuration files with Git?
A: Manage template files (.env.example) with Git, but add actual configuration files (.env) to .gitignore and don't manage them.

### Q: How do I dynamically change configuration in production?
A: Application restart is required after configuration changes. Use rolling updates to avoid downtime.

### Q: When should configuration validation be performed?
A: We recommend performing validation at application startup, deployment time, and during regular audits.