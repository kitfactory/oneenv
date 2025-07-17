# Step 3: Named Environments Basics

**Duration:** 10-15 minutes  
**Difficulty:** Beginner to Intermediate

## Learning Objectives

- Understand named environment concepts
- Practice configuration separation using namespaces
- Learn to leverage fallback functionality
- Understand real-world usage patterns

## Purpose & Benefits

**Why this step matters:**
- **Organization**: Separate configuration by service/component for clarity
- **Scalability**: Manage complex applications with multiple services
- **Flexibility**: Share common settings while allowing service-specific overrides
- **Maintainability**: Reduce configuration complexity and conflicts
- **Team Collaboration**: Clear boundaries between different service configurations

## Traditional Problems

### Configuration Mixing
```python
import os

# All settings mixed together, unclear which component they belong to
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
WEB_SERVER_HOST = os.getenv("WEB_HOST", "0.0.0.0")
API_SERVER_HOST = os.getenv("API_HOST", "localhost")
CACHE_HOST = os.getenv("CACHE_HOST", "localhost")
TIMEOUT = os.getenv("TIMEOUT", "30")  # Which component's timeout?
```

### Environment-Specific Configuration Complexity
```python
# Development, staging, production settings mixed together
if os.getenv("ENVIRONMENT") == "production":
    DATABASE_URL = os.getenv("PROD_DATABASE_URL")
    REDIS_URL = os.getenv("PROD_REDIS_URL")
elif os.getenv("ENVIRONMENT") == "staging":
    DATABASE_URL = os.getenv("STAGING_DATABASE_URL")
    REDIS_URL = os.getenv("STAGING_REDIS_URL")
# Configuration becomes complex...
```

## OneEnv Named Environments

### Core Concepts

OneEnv manages environment variables using **namespaces**:

- **Common Environment** (`oneenv.env()`): Shared settings across all components
- **Named Environments** (`oneenv.env("name")`): Component-specific settings
- **Intelligent Fallback**: Named environment → Common environment → OS environment

**Fallback Chain:**
```
oneenv.env("database").get("TIMEOUT") 
    ↓ 1. Look in "database" namespace
    ↓ 2. Fallback to common namespace  
    ↓ 3. Fallback to OS environment
    ↓ 4. Use provided default
```

## Practical Exercises

### Exercise 1: Basic Named Environments

1. Create project directory:
```bash
mkdir named-env-tutorial
cd named-env-tutorial
```

2. Create environment files:

**common.env:**
```bash
# Common settings shared across all services
TIMEOUT=30
LOG_LEVEL=INFO
ENVIRONMENT=development
```

**database.env:**
```bash
# Database-specific settings
HOST=localhost
PORT=5432
NAME=myapp_db
USER=dbuser
PASSWORD=dbpass
```

**web.env:**
```bash
# Web server settings
HOST=0.0.0.0
PORT=8000
WORKERS=4
```

**api.env:**
```bash
# API server settings
HOST=localhost
PORT=8080
RATE_LIMIT=100
```

3. Use named environments (`named_env_demo.py`):
```python
import oneenv

# Load settings into respective environments
oneenv.env().load_dotenv("common.env")
oneenv.env("database").load_dotenv("database.env")
oneenv.env("web").load_dotenv("web.env")
oneenv.env("api").load_dotenv("api.env")

print("=== Configuration Retrieval ===")

# Database configuration (from database environment)
db_config = {
    "host": oneenv.env("database").get("HOST"),
    "port": int(oneenv.env("database").get("PORT")),
    "name": oneenv.env("database").get("NAME"),
    "timeout": int(oneenv.env("database").get("TIMEOUT", "10"))  # Falls back to common
}
print(f"Database: {db_config}")

# Web server configuration (from web environment)
web_config = {
    "host": oneenv.env("web").get("HOST"),
    "port": int(oneenv.env("web").get("PORT")),
    "workers": int(oneenv.env("web").get("WORKERS")),
    "log_level": oneenv.env("web").get("LOG_LEVEL", "WARNING")  # Falls back to common
}
print(f"Web: {web_config}")

# API configuration (from api environment)
api_config = {
    "host": oneenv.env("api").get("HOST"),
    "port": int(oneenv.env("api").get("PORT")),
    "rate_limit": int(oneenv.env("api").get("RATE_LIMIT")),
    "environment": oneenv.env("api").get("ENVIRONMENT", "unknown")  # Falls back to common
}
print(f"API: {api_config}")
```

4. Run:
```bash
python named_env_demo.py
```

**Expected output:**
```
=== Configuration Retrieval ===
Database: {'host': 'localhost', 'port': 5432, 'name': 'myapp_db', 'timeout': 30}
Web: {'host': '0.0.0.0', 'port': 8000, 'workers': 4, 'log_level': 'INFO'}
API: {'host': 'localhost', 'port': 8080, 'rate_limit': 100, 'environment': 'development'}
```

### Exercise 2: Fallback Behavior Verification

Verify fallback behavior:

```python
# fallback_demo.py
import oneenv

# Load only common environment
oneenv.env().load_dotenv("common.env")

print("=== Fallback Behavior Verification ===")

# Get settings from database environment (database.env not loaded)
db_timeout = oneenv.env("database").get("TIMEOUT")  # Retrieved from common
db_host = oneenv.env("database").get("HOST", "default-host")  # Uses default

print(f"Database timeout (from common): {db_timeout}")
print(f"Database host (default): {db_host}")

# Get directly from common environment
common_timeout = oneenv.env().get("TIMEOUT")
print(f"Common timeout: {common_timeout}")
```

### Exercise 3: Dynamic Environment Switching

Switch configuration based on environment:

```python
# dynamic_env.py
import oneenv
import os

# Determine environment
env_name = os.getenv("APP_ENV", "development")

print(f"=== Current Environment: {env_name} ===")

# Load common settings
oneenv.env().load_dotenv("common.env")

# Select configuration file based on environment
if env_name == "production":
    oneenv.env("database").load_dotenv("production.env")
elif env_name == "staging":
    oneenv.env("database").load_dotenv("staging.env")
else:
    oneenv.env("database").load_dotenv("database.env")

# Retrieve configuration
config = {
    "database_host": oneenv.env("database").get("HOST"),
    "database_port": oneenv.env("database").get("PORT"),
    "log_level": oneenv.env("database").get("LOG_LEVEL"),  # Falls back to common
    "environment": env_name
}

print(f"Configuration: {config}")
```

## Advanced Usage Patterns

### Pattern 1: Component-Based Configuration Management

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

# Usage example
db_config = DatabaseConfig()
web_config = WebConfig()

print(f"Database URL: {db_config.connection_url}")
print(f"Web bind: {web_config.bind_address}")
```

### Pattern 2: Configuration Validation

```python
# validated_config.py
import oneenv

def validate_database_config():
    """Validate database configuration"""
    required_vars = ["HOST", "PORT", "NAME"]
    
    for var in required_vars:
        value = oneenv.env("database").get(var)
        if not value:
            raise ValueError(f"Required database config {var} is missing")
    
    # Validate port number
    try:
        port = int(oneenv.env("database").get("PORT"))
        if not (1 <= port <= 65535):
            raise ValueError(f"Invalid port number: {port}")
    except ValueError as e:
        raise ValueError(f"Invalid port format: {e}")
    
    return True

# Usage example
oneenv.env().load_dotenv("common.env")
oneenv.env("database").load_dotenv("database.env")

try:
    validate_database_config()
    print("✅ Database configuration is valid")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
```

## Named Environment Benefits

### 1. **Logical Configuration Separation**
```python
# Clear component association
db_host = oneenv.env("database").get("HOST")
web_host = oneenv.env("web").get("HOST")
cache_host = oneenv.env("cache").get("HOST")
```

### 2. **Configuration Reuse**
```python
# Common settings automatically fallback
timeout = oneenv.env("database").get("TIMEOUT")  # From common
log_level = oneenv.env("web").get("LOG_LEVEL")   # From common
```

### 3. **Flexible Environment-Specific Settings**
```python
# Different config files per environment
oneenv.env("database").load_dotenv(f"{env_name}_database.env")
```

### 4. **Test Isolation**
```python
# Separate test environment
oneenv.env("test").load_dotenv("test.env")
test_db = oneenv.env("test").get("DATABASE_URL")
```

## Named Environment Best Practices

### 1. **Consistent Naming Conventions**
- **Component names**: `database`, `web`, `api`, `cache`
- **Environment names**: `development`, `staging`, `production`
- **Feature names**: `auth`, `payment`, `logging`

### 2. **Common Settings Utilization**
Place shared settings in common environment:
```bash
# common.env
TIMEOUT=30
LOG_LEVEL=INFO
ENVIRONMENT=development
DEBUG=True
```

### 3. **Structured Configuration Files**
```
env/
├── common.env          # Common settings
├── database.env        # Database settings
├── web.env            # Web server settings
├── api.env            # API settings
└── production/        # Production environment
    ├── database.env
    ├── web.env
    └── api.env
```

## Key Takeaways

**What you've learned:**
- ✅ **Namespace Separation**: Organize configuration by component/service
- ✅ **Intelligent Fallback**: Automatic fallback from specific to common to OS environment
- ✅ **Configuration Patterns**: Component classes and validation strategies
- ✅ **Best Practices**: Naming conventions and file organization

**Benefits gained:**
- **Clarity**: Clear ownership and purpose of each configuration variable
- **Scalability**: Easily manage complex multi-service applications
- **Flexibility**: Share common settings while allowing specific overrides
- **Maintainability**: Reduce configuration conflicts and complexity

## Next Steps

You've mastered named environments basics. Next, learn how to manage configuration in real multi-service applications.

**→ [Step 4: Multi-Service Management](04-multi-service.md)**

## Frequently Asked Questions

### Q: What characters can be used in environment names?
A: Environment names can use alphanumeric characters, underscores, and hyphens, similar to Python variable name rules.

### Q: How can I override common environment settings?
A: Define the same variable in a named environment, and it will take precedence over the common environment.

### Q: What happens when a variable is not found?
A: OneEnv searches in this order: named environment → common environment → OS environment → default value.

### Q: Can I load multiple .env files into the same environment?
A: Yes, you can call `load_dotenv()` multiple times to load multiple files into the same environment.