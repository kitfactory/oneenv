# Step 4: Multi-Service Management

**Duration:** 15-20 minutes  
**Difficulty:** Intermediate

## Learning Objectives

- Learn configuration management for multi-service applications
- Understand the balance between configuration sharing and separation across services
- Practice integration patterns with Docker Compose
- Experience configuration management in microservice environments

## Scenario

Configuration management for an e-commerce platform consisting of the following services:

- **Web Frontend** (React/Next.js)
- **API Backend** (FastAPI/Django)
- **Database** (PostgreSQL)
- **Cache** (Redis)
- **Worker** (Celery)
- **Monitoring** (Prometheus/Grafana)

## Project Structure

```
ecommerce-app/
├── docker-compose.yml
├── env/
│   ├── common.env          # Shared configuration
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
└── config.py              # Configuration management module
```

## Hands-on Exercises

### Exercise 1: Environment File Design

1. Create project directory:
```bash
mkdir ecommerce-app
cd ecommerce-app
mkdir env services
```

2. Common configuration file (`env/common.env`):
```bash
# Common settings
PROJECT_NAME=ECommerce Platform
ENVIRONMENT=development
LOG_LEVEL=INFO
TIMEZONE=UTC

# Security
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET=jwt-secret-key

# External services
SMTP_HOST=localhost
SMTP_PORT=587
```

3. Database configuration (`env/database.env`):
```bash
# PostgreSQL settings
HOST=localhost
PORT=5432
NAME=ecommerce_db
USER=postgres
PASSWORD=postgres_password

# Connection pool settings
POOL_SIZE=20
MAX_OVERFLOW=30
POOL_TIMEOUT=30

# Backup settings
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=7
```

4. API configuration (`env/api.env`):
```bash
# API server settings
HOST=0.0.0.0
PORT=8000
WORKERS=4

# API-specific settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
RATE_LIMIT_PER_MINUTE=60
API_VERSION=v1

# External APIs
PAYMENT_API_URL=https://api.stripe.com/v1
SHIPPING_API_URL=https://api.shipping.com/v2
```

5. Web configuration (`env/web.env`):
```bash
# Web server settings
HOST=0.0.0.0
PORT=3000

# Frontend settings
API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=ECommerce Platform
NEXT_PUBLIC_VERSION=1.0.0

# Asset settings
CDN_URL=https://cdn.example.com
STATIC_FILES_URL=/static
```

6. Cache configuration (`env/cache.env`):
```bash
# Redis settings
HOST=localhost
PORT=6379
DB=0
PASSWORD=redis_password

# Cache settings
DEFAULT_TIMEOUT=300
SESSION_TIMEOUT=3600
CART_TIMEOUT=1800

# Redis configuration
MAX_CONNECTIONS=50
```

7. Worker configuration (`env/worker.env`):
```bash
# Celery worker settings
CONCURRENCY=4
LOGLEVEL=INFO

# Queue settings
DEFAULT_QUEUE=default
EMAIL_QUEUE=email
REPORT_QUEUE=reports

# Task settings
EMAIL_RETRY_DELAY=60
REPORT_TIMEOUT=300
```

### Exercise 2: Configuration Management Module

Unified configuration management module (`config.py`):

```python
import oneenv
import os
from typing import Dict, Any

class ConfigBase:
    """Base configuration class"""
    
    def __init__(self, service_name: str = None):
        self.service_name = service_name
        self._load_env_files()
    
    def _load_env_files(self):
        """Load environment files"""
        # Load common configuration
        oneenv.env().load_dotenv("env/common.env")
        
        # Load service-specific configuration
        if self.service_name:
            oneenv.env(self.service_name).load_dotenv(f"env/{self.service_name}.env")
    
    def get(self, key: str, default: Any = None) -> str:
        """Get configuration value"""
        if self.service_name:
            return oneenv.env(self.service_name).get(key, default)
        return oneenv.env().get(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer configuration value"""
        value = self.get(key, str(default))
        return int(value)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean configuration value"""
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_list(self, key: str, separator: str = ',', default: list = None) -> list:
        """Get list configuration value"""
        if default is None:
            default = []
        value = self.get(key, separator.join(default))
        return [item.strip() for item in value.split(separator) if item.strip()]

class CommonConfig(ConfigBase):
    """Common configuration"""
    
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
    """Database configuration"""
    
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
        # Fallback to common configuration
        return self.get_int("TIMEOUT", 30)

class APIConfig(ConfigBase):
    """API configuration"""
    
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
    """Web configuration"""
    
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
    """Cache configuration"""
    
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
    """Worker configuration"""
    
    def __init__(self):
        super().__init__("worker")
    
    @property
    def concurrency(self) -> int:
        return self.get_int("CONCURRENCY", 4)
    
    @property
    def log_level(self) -> str:
        # Fallback to common configuration
        return self.get("LOGLEVEL", self.get("LOG_LEVEL", "INFO"))
    
    @property
    def default_queue(self) -> str:
        return self.get("DEFAULT_QUEUE", "default")

# Create configuration instances
common = CommonConfig()
database = DatabaseConfig()
api = APIConfig()
web = WebConfig()
cache = CacheConfig()
worker = WorkerConfig()
```

### Exercise 3: Configuration Usage Examples

Configuration usage examples for each service:

**API Service (`services/api/app.py`):**
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

**Worker Service (`services/worker/worker.py`):**
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config import common, database, cache, worker
from celery import Celery

# Create Celery application
celery_app = Celery(
    common.project_name,
    broker=cache.url,
    backend=cache.url
)

# Apply configuration
celery_app.conf.update(
    worker_concurrency=worker.concurrency,
    worker_log_level=worker.log_level,
    task_default_queue=worker.default_queue,
    timezone=common.get("TIMEZONE", "UTC")
)

@celery_app.task
def send_email(to: str, subject: str, body: str):
    """Email sending task"""
    print(f"Sending email to {to}: {subject}")
    # Email sending logic
    return {"status": "sent", "to": to}

@celery_app.task
def generate_report(report_type: str):
    """Report generation task"""
    print(f"Generating {report_type} report")
    # Report generation logic
    return {"status": "generated", "type": report_type}
```

### Exercise 4: Docker Compose Integration

Docker Compose configuration (`docker-compose.yml`):

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

Startup script (`start.sh`):
```bash
#!/bin/bash

# Load environment variables from configuration files
export $(grep -v '^#' env/common.env | xargs)
export $(grep -v '^#' env/database.env | sed 's/^/DATABASE_/' | xargs)
export $(grep -v '^#' env/api.env | sed 's/^/API_/' | xargs)
export $(grep -v '^#' env/web.env | sed 's/^/WEB_/' | xargs)
export $(grep -v '^#' env/cache.env | sed 's/^/CACHE_/' | xargs)

# Start with Docker Compose
docker-compose up --build
```

### Exercise 5: Configuration Validation and Testing

Configuration validation script (`validate_config.py`):

```python
import sys
from config import common, database, api, web, cache, worker

def validate_common_config():
    """Validate common configuration"""
    errors = []
    
    if not common.secret_key:
        errors.append("SECRET_KEY is required")
    
    if len(common.secret_key) < 32:
        errors.append("SECRET_KEY should be at least 32 characters")
    
    if common.environment not in ['development', 'staging', 'production']:
        errors.append("ENVIRONMENT must be development, staging, or production")
    
    return errors

def validate_database_config():
    """Validate database configuration"""
    errors = []
    
    if not database.password:
        errors.append("Database PASSWORD is required")
    
    if not (1024 <= database.port <= 65535):
        errors.append("Database PORT must be between 1024 and 65535")
    
    if database.pool_size <= 0:
        errors.append("Database POOL_SIZE must be positive")
    
    return errors

def validate_api_config():
    """Validate API configuration"""
    errors = []
    
    if not (1024 <= api.port <= 65535):
        errors.append("API PORT must be between 1024 and 65535")
    
    if api.workers <= 0:
        errors.append("API WORKERS must be positive")
    
    if api.rate_limit <= 0:
        errors.append("API RATE_LIMIT_PER_MINUTE must be positive")
    
    return errors

def main():
    """Main function for configuration validation"""
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
        
        # Display configuration summary
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

## Multi-Service Configuration Management Best Practices

### 1. **Configuration Hierarchy**
```
Common configuration (common.env)
├── Service-specific configuration (service.env)
└── Environment-specific configuration (production/service.env)
```

### 2. **Type Safety in Configuration**
```python
# Provide type conversion methods
config.get_int("PORT", 8000)
config.get_bool("DEBUG", False)
config.get_list("CORS_ORIGINS")
```

### 3. **Configuration Validation**
```python
# Validate configuration at startup
validate_config()
```

### 4. **Environment-Specific Configuration Separation**
```bash
env/
├── development/
├── staging/
└── production/
```

### 5. **Secret Management**
```python
# Manage secrets separately
oneenv.env("secrets").load_dotenv("secrets.env")
```

## Next Steps

You've learned multi-service configuration management. Next, let's learn how to create custom project templates.

**→ [Step 5: Custom Templates](05-custom-templates.md)**

## Frequently Asked Questions

### Q: How do I share configuration between services?
A: Use a common configuration file (common.env) and configure fallback from the common environment in each service.

### Q: Too many configuration files are difficult to manage
A: Create a configuration management module and provide property-based access to simplify management.

### Q: How do I dynamically change configuration in Docker environments?
A: You can override with environment variables or dynamically change configuration files through volume mounts.