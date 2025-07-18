# Step 7: Plugin Development

**Duration:** 20-25 minutes  
**Difficulty:** Advanced

## Learning Objectives

- Understand how to create OneEnv plugins
- Learn how to utilize the Entry-points system
- Create distributable plugins as packages
- Practice plugin testing and debugging methods

## Plugin System Overview

OneEnv's plugin system uses Python's **Entry-points** mechanism to allow packages to automatically provide environment variable templates.

### What are Entry-points?
```toml
# pyproject.toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
web = "mypackage.templates:web_template"
```

This allows OneEnv to automatically discover templates just by installing the package.

## Hands-on Exercises

### Exercise 1: Creating a Simple Plugin

1. Create plugin project:
```bash
mkdir oneenv-database-plugin
cd oneenv-database-plugin
```

2. Create project structure:
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

3. Package configuration (`pyproject.toml`):
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

# Register as OneEnv plugin
[project.entry-points."oneenv.templates"]
postgresql = "oneenv_database.templates:postgresql_template"
mysql = "oneenv_database.templates:mysql_template"
redis = "oneenv_database.templates:redis_template"
mongodb = "oneenv_database.templates:mongodb_template"

[tool.hatch.build.targets.wheel]
packages = ["src/oneenv_database"]
```

4. Template implementation (`src/oneenv_database/templates.py`):
```python
"""
OneEnv Database Plugin Templates
Provides database-related environment variable templates
"""

def postgresql_template():
    """PostgreSQL database configuration template"""
    return {
        "groups": {
            "PostgreSQL Database": {
                "POSTGRES_HOST": {
                    "description": "PostgreSQL server host\nExample: localhost, db.example.com",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "POSTGRES_PORT": {
                    "description": "PostgreSQL server port",
                    "default": "5432",
                    "required": False,
                    "choices": ["5432", "5433", "5434"],
                    "importance": "important"
                },
                "POSTGRES_DB": {
                    "description": "Database name",
                    "default": "myapp",
                    "required": True,
                    "importance": "critical"
                },
                "POSTGRES_USER": {
                    "description": "Database username",
                    "default": "postgres",
                    "required": True,
                    "importance": "critical"
                },
                "POSTGRES_PASSWORD": {
                    "description": "Database password\nUse strong passwords in production",
                    "default": "password",
                    "required": True,
                    "importance": "critical"
                }
            },
            
            "PostgreSQL Connection": {
                "POSTGRES_POOL_SIZE": {
                    "description": "Connection pool size\nAdjust based on application load",
                    "default": "20",
                    "required": False,
                    "importance": "important"
                },
                "POSTGRES_MAX_OVERFLOW": {
                    "description": "Maximum overflow connections",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                },
                "POSTGRES_TIMEOUT": {
                    "description": "Connection timeout in seconds",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    }

def mysql_template():
    """MySQL/MariaDB database configuration template"""
    return {
        "groups": {
            "MySQL Database": {
                "MYSQL_HOST": {
                    "description": "MySQL server host",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "MYSQL_PORT": {
                    "description": "MySQL server port",
                    "default": "3306",
                    "required": False,
                    "importance": "important"
                },
                "MYSQL_DATABASE": {
                    "description": "Database name",
                    "default": "myapp",
                    "required": True,
                    "importance": "critical"
                },
                "MYSQL_USER": {
                    "description": "Database username",
                    "default": "mysql",
                    "required": True,
                    "importance": "critical"
                },
                "MYSQL_PASSWORD": {
                    "description": "Database password",
                    "default": "password",
                    "required": True,
                    "importance": "critical"
                },
                "MYSQL_CHARSET": {
                    "description": "Character set",
                    "default": "utf8mb4",
                    "required": False,
                    "choices": ["utf8", "utf8mb4", "latin1"],
                    "importance": "important"
                }
            }
        }
    }

def redis_template():
    """Redis cache configuration template"""
    return {
        "groups": {
            "Redis Cache": {
                "REDIS_HOST": {
                    "description": "Redis server host",
                    "default": "localhost",
                    "required": True,
                    "importance": "important"
                },
                "REDIS_PORT": {
                    "description": "Redis server port",
                    "default": "6379",
                    "required": False,
                    "importance": "important"
                },
                "REDIS_DB": {
                    "description": "Redis database number",
                    "default": "0",
                    "required": False,
                    "choices": ["0", "1", "2", "3", "4"],
                    "importance": "optional"
                },
                "REDIS_PASSWORD": {
                    "description": "Redis authentication password",
                    "default": "",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Redis Settings": {
                "REDIS_MAX_CONNECTIONS": {
                    "description": "Maximum connections",
                    "default": "50",
                    "required": False,
                    "importance": "optional"
                },
                "REDIS_SOCKET_TIMEOUT": {
                    "description": "Socket timeout in seconds",
                    "default": "5",
                    "required": False,
                    "importance": "optional"
                },
                "REDIS_DECODE_RESPONSES": {
                    "description": "Decode responses",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            }
        }
    }

def mongodb_template():
    """MongoDB database configuration template"""
    return {
        "groups": {
            "MongoDB Database": {
                "MONGODB_HOST": {
                    "description": "MongoDB server host",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "MONGODB_PORT": {
                    "description": "MongoDB server port",
                    "default": "27017",
                    "required": False,
                    "importance": "important"
                },
                "MONGODB_DATABASE": {
                    "description": "Database name",
                    "default": "myapp",
                    "required": True,
                    "importance": "critical"
                },
                "MONGODB_USERNAME": {
                    "description": "Database username",
                    "default": "",
                    "required": False,
                    "importance": "important"
                },
                "MONGODB_PASSWORD": {
                    "description": "Database password",
                    "default": "",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "MongoDB Options": {
                "MONGODB_AUTH_SOURCE": {
                    "description": "Authentication database",
                    "default": "admin",
                    "required": False,
                    "importance": "optional"
                },
                "MONGODB_REPLICA_SET": {
                    "description": "Replica set name",
                    "default": "",
                    "required": False,
                    "importance": "optional"
                },
                "MONGODB_SSL": {
                    "description": "Enable SSL connection",
                    "default": "False",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            }
        }
    }
```

5. Package initialization (`src/oneenv_database/__init__.py`):
```python
"""
OneEnv Database Plugin

Provides database configuration templates for OneEnv.
Supports PostgreSQL, MySQL, Redis, and MongoDB.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Make templates available for import
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

### Exercise 2: Plugin Testing

1. Create test file (`tests/test_templates.py`):
```python
import pytest
from oneenv_database.templates import (
    postgresql_template,
    mysql_template,
    redis_template,
    mongodb_template
)

class TestDatabaseTemplates:
    """Test database template functions"""
    
    def test_postgresql_template_structure(self):
        """Test PostgreSQL template structure"""
        template = postgresql_template()
        
        # Check basic structure
        assert "groups" in template
        assert "PostgreSQL Database" in template["groups"]
        assert "PostgreSQL Connection" in template["groups"]
        
        # Check critical variables
        db_group = template["groups"]["PostgreSQL Database"]
        assert "POSTGRES_HOST" in db_group
        assert "POSTGRES_DB" in db_group
        assert "POSTGRES_USER" in db_group
        assert "POSTGRES_PASSWORD" in db_group
        
        # Check variable properties
        host_config = db_group["POSTGRES_HOST"]
        assert host_config["required"] is True
        assert host_config["importance"] == "critical"
        assert host_config["default"] == "localhost"
    
    def test_mysql_template_structure(self):
        """Test MySQL template structure"""
        template = mysql_template()
        
        assert "groups" in template
        assert "MySQL Database" in template["groups"]
        
        db_group = template["groups"]["MySQL Database"]
        assert "MYSQL_HOST" in db_group
        assert "MYSQL_DATABASE" in db_group
        assert "MYSQL_USER" in db_group
        assert "MYSQL_PASSWORD" in db_group
        
        # Test charset choices
        charset_config = db_group["MYSQL_CHARSET"]
        assert "choices" in charset_config
        assert "utf8mb4" in charset_config["choices"]
    
    def test_redis_template_structure(self):
        """Test Redis template structure"""
        template = redis_template()
        
        assert "groups" in template
        assert "Redis Cache" in template["groups"]
        assert "Redis Settings" in template["groups"]
        
        cache_group = template["groups"]["Redis Cache"]
        assert "REDIS_HOST" in cache_group
        assert "REDIS_PORT" in cache_group
        assert "REDIS_DB" in cache_group
        
        # Test database number choices
        db_config = cache_group["REDIS_DB"]
        assert "choices" in db_config
        assert "0" in db_config["choices"]
    
    def test_mongodb_template_structure(self):
        """Test MongoDB template structure"""
        template = mongodb_template()
        
        assert "groups" in template
        assert "MongoDB Database" in template["groups"]
        assert "MongoDB Options" in template["groups"]
        
        db_group = template["groups"]["MongoDB Database"]
        assert "MONGODB_HOST" in db_group
        assert "MONGODB_DATABASE" in db_group
        
        # Test SSL option
        options_group = template["groups"]["MongoDB Options"]
        ssl_config = options_group["MONGODB_SSL"]
        assert ssl_config["choices"] == ["True", "False"]
    
    def test_all_templates_have_required_fields(self):
        """Test that all templates have required fields"""
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
                    # Check required fields
                    assert "description" in var_config
                    assert "default" in var_config
                    assert "required" in var_config
                    assert "importance" in var_config
                    
                    # Check importance values
                    assert var_config["importance"] in ["critical", "important", "optional"]
                    
                    # Check required field type
                    assert isinstance(var_config["required"], bool)

    def test_template_integration(self):
        """Test template integration with OneEnv"""
        # This test would require OneEnv to be installed
        try:
            import oneenv
            
            # Test that templates can be collected
            # Note: This would only work if the plugin is installed
            templates = oneenv.collect_templates()
            assert isinstance(templates, dict)
            
        except ImportError:
            pytest.skip("OneEnv not installed")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

2. Run tests:
```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/ -v
```

### Exercise 3: Plugin Installation and Testing

1. Install plugin in development mode:
```bash
pip install -e .
```

2. Test plugin discovery:
```python
# test_discovery.py
import oneenv

# Test template discovery
print("=== OneEnv Template Discovery Test ===")

# Check if our templates are discovered
try:
    template_content = oneenv.template(debug=True)
    print("Template generation successful!")
    print("\nGenerated content preview:")
    print(template_content[:500] + "...")
    
except Exception as e:
    print(f"Error: {e}")

# Test specific entry points
import pkg_resources

print("\n=== Entry Points Discovery ===")
for entry_point in pkg_resources.iter_entry_points('oneenv.templates'):
    print(f"Found entry point: {entry_point.name} -> {entry_point.module_name}:{entry_point.attrs[0]}")
    
    try:
        template_func = entry_point.load()
        template_data = template_func()
        print(f"  Template loaded successfully: {len(template_data.get('groups', {}))} groups")
    except Exception as e:
        print(f"  Error loading template: {e}")
```

3. Run discovery test:
```bash
python test_discovery.py
```

### Exercise 4: Advanced Plugin Features

1. Create configuration validation (`src/oneenv_database/validators.py`):
```python
"""
Plugin-specific validation functions
"""

def validate_postgresql_config(config: dict) -> list:
    """Validate PostgreSQL configuration"""
    errors = []
    
    # Check for required fields
    required_fields = ["POSTGRES_HOST", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
    for field in required_fields:
        if not config.get(field):
            errors.append(f"{field} is required for PostgreSQL")
    
    # Validate port number
    port = config.get("POSTGRES_PORT", "5432")
    try:
        port_num = int(port)
        if not (1024 <= port_num <= 65535):
            errors.append("POSTGRES_PORT must be between 1024 and 65535")
    except ValueError:
        errors.append("POSTGRES_PORT must be a valid number")
    
    # Validate pool size
    pool_size = config.get("POSTGRES_POOL_SIZE", "20")
    try:
        pool_num = int(pool_size)
        if pool_num <= 0:
            errors.append("POSTGRES_POOL_SIZE must be positive")
        elif pool_num > 100:
            errors.append("POSTGRES_POOL_SIZE should not exceed 100")
    except ValueError:
        errors.append("POSTGRES_POOL_SIZE must be a valid number")
    
    return errors

def validate_redis_config(config: dict) -> list:
    """Validate Redis configuration"""
    errors = []
    
    # Validate database number
    db_num = config.get("REDIS_DB", "0")
    try:
        db = int(db_num)
        if not (0 <= db <= 15):
            errors.append("REDIS_DB must be between 0 and 15")
    except ValueError:
        errors.append("REDIS_DB must be a valid number")
    
    # Validate max connections
    max_conn = config.get("REDIS_MAX_CONNECTIONS", "50")
    try:
        max_num = int(max_conn)
        if max_num <= 0:
            errors.append("REDIS_MAX_CONNECTIONS must be positive")
    except ValueError:
        errors.append("REDIS_MAX_CONNECTIONS must be a valid number")
    
    return errors
```

2. Create utility functions (`src/oneenv_database/utils.py`):
```python
"""
Database plugin utility functions
"""

def build_postgresql_url(config: dict) -> str:
    """Build PostgreSQL connection URL from config"""
    host = config.get("POSTGRES_HOST", "localhost")
    port = config.get("POSTGRES_PORT", "5432")
    database = config.get("POSTGRES_DB", "myapp")
    user = config.get("POSTGRES_USER", "postgres")
    password = config.get("POSTGRES_PASSWORD", "password")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def build_mysql_url(config: dict) -> str:
    """Build MySQL connection URL from config"""
    host = config.get("MYSQL_HOST", "localhost")
    port = config.get("MYSQL_PORT", "3306")
    database = config.get("MYSQL_DATABASE", "myapp")
    user = config.get("MYSQL_USER", "mysql")
    password = config.get("MYSQL_PASSWORD", "password")
    charset = config.get("MYSQL_CHARSET", "utf8mb4")
    
    return f"mysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"

def build_redis_url(config: dict) -> str:
    """Build Redis connection URL from config"""
    host = config.get("REDIS_HOST", "localhost")
    port = config.get("REDIS_PORT", "6379")
    db = config.get("REDIS_DB", "0")
    password = config.get("REDIS_PASSWORD", "")
    
    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    else:
        return f"redis://{host}:{port}/{db}"

def build_mongodb_url(config: dict) -> str:
    """Build MongoDB connection URL from config"""
    host = config.get("MONGODB_HOST", "localhost")
    port = config.get("MONGODB_PORT", "27017")
    database = config.get("MONGODB_DATABASE", "myapp")
    username = config.get("MONGODB_USERNAME", "")
    password = config.get("MONGODB_PASSWORD", "")
    auth_source = config.get("MONGODB_AUTH_SOURCE", "admin")
    replica_set = config.get("MONGODB_REPLICA_SET", "")
    ssl = config.get("MONGODB_SSL", "False").lower() == "true"
    
    url = "mongodb://"
    
    if username and password:
        url += f"{username}:{password}@"
    
    url += f"{host}:{port}/{database}"
    
    params = []
    if auth_source and username:
        params.append(f"authSource={auth_source}")
    if replica_set:
        params.append(f"replicaSet={replica_set}")
    if ssl:
        params.append("ssl=true")
    
    if params:
        url += "?" + "&".join(params)
    
    return url

# Configuration helper
class DatabaseConfig:
    """Helper class for database configuration"""
    
    def __init__(self, config: dict):
        self.config = config
    
    def get_postgresql_url(self) -> str:
        return build_postgresql_url(self.config)
    
    def get_mysql_url(self) -> str:
        return build_mysql_url(self.config)
    
    def get_redis_url(self) -> str:
        return build_redis_url(self.config)
    
    def get_mongodb_url(self) -> str:
        return build_mongodb_url(self.config)
    
    def validate_all(self) -> dict:
        """Validate all database configurations"""
        from .validators import validate_postgresql_config, validate_redis_config
        
        results = {}
        
        # PostgreSQL validation
        pg_errors = validate_postgresql_config(self.config)
        if pg_errors:
            results["postgresql"] = pg_errors
        
        # Redis validation
        redis_errors = validate_redis_config(self.config)
        if redis_errors:
            results["redis"] = redis_errors
        
        return results
```

### Exercise 5: Plugin Documentation

1. Create comprehensive README (`README.md`):
```markdown
# OneEnv Database Plugin

A comprehensive database configuration plugin for OneEnv that provides templates for PostgreSQL, MySQL, Redis, and MongoDB.

## Installation

```bash
pip install oneenv-database-plugin
```

## Features

- **PostgreSQL**: Complete PostgreSQL configuration with connection pooling
- **MySQL/MariaDB**: MySQL database configuration with charset options
- **Redis**: Redis cache configuration with connection settings
- **MongoDB**: MongoDB database configuration with authentication and SSL

## Usage

After installation, the templates are automatically available in OneEnv:

```bash
# List available templates
oneenv template -d

# Generate environment file
oneenv template
```

## Templates

### PostgreSQL Template
- Connection settings (host, port, database, user, password)
- Connection pool configuration
- Timeout settings

### MySQL Template  
- Basic connection settings
- Character set configuration
- Port customization

### Redis Template
- Server connection settings
- Database selection
- Connection pooling options

### MongoDB Template
- Server configuration
- Authentication settings
- Replica set and SSL options

## Configuration Validation

The plugin includes validation functions to ensure configuration correctness:

```python
from oneenv_database.validators import validate_postgresql_config
from oneenv_database.utils import DatabaseConfig

# Validate configuration
config = {"POSTGRES_HOST": "localhost", ...}
errors = validate_postgresql_config(config)

# Build connection URLs
db_config = DatabaseConfig(config)
postgres_url = db_config.get_postgresql_url()
```

## Development

```bash
# Clone repository
git clone https://github.com/yourusername/oneenv-database-plugin

# Install in development mode
pip install -e .

# Run tests
pytest tests/ -v
```

## License

MIT License
```

## Plugin Best Practices

### 1. **Template Design**
- Use clear, descriptive variable names
- Provide comprehensive descriptions
- Set appropriate importance levels
- Include reasonable default values

### 2. **Entry Points**
- Use descriptive entry point names
- Follow consistent naming conventions
- Organize templates logically

### 3. **Testing**
- Test template structure
- Validate all required fields
- Test integration with OneEnv
- Include performance tests

### 4. **Documentation**
- Provide clear usage examples
- Document all configuration options
- Include troubleshooting guides
- Maintain changelog

### 5. **Distribution**
- Use semantic versioning
- Include proper metadata
- Test installation process
- Provide support channels

## Next Steps

You've learned how to create distributable OneEnv plugins. Next, let's learn about CI/CD integration.

**→ [Step 8: CI/CD Integration](08-cicd-integration.md)**

## Frequently Asked Questions

### Q: How do I debug plugin discovery issues?
A: Use `oneenv template -d` to see debug information about template discovery and loading.

### Q: Can I create plugins for specific frameworks?
A: Yes! Create entry points that target specific use cases like Django, Flask, FastAPI, etc.

### Q: How do I version my plugin releases?
A: Use semantic versioning and tag releases in your repository. Update the version in `pyproject.toml`.

### Q: Can plugins depend on other plugins?
A: Yes, but be careful about circular dependencies. List plugin dependencies in your `pyproject.toml`.