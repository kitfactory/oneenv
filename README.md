# OneEnv 🌟

[![PyPI Downloads](https://static.pepy.tech/badge/oneenv)](https://pepy.tech/projects/oneenv)

**Python environment variable management made simple.**

OneEnv automatically discovers environment variable templates from your installed packages and manages them with namespaces.

## Core Features 🎯

### 1. Package Environment Variable Discovery 📦
Automatically collect environment variable templates from all installed packages - no manual configuration required.

### 2. Namespace Management 🏷️
Organize environment variables by service/component with intelligent fallback.

## Installation 📦

```bash
pip install oneenv
```

## Quick Start 🚀

### Generate Environment Template
```bash
oneenv template
```

### Use Named Environments
```python
import oneenv

# Load different environments
oneenv.env().load_dotenv("common.env")
oneenv.env("database").load_dotenv("database.env")
oneenv.env("web").load_dotenv("web.env")

# Get values with namespace fallback
db_host = oneenv.env("database").get("HOST", "localhost")
web_port = oneenv.env("web").get("PORT", "8000")
timeout = oneenv.env("database").get("TIMEOUT", "30")  # Falls back to common
```

## Example: Before vs After

**Before OneEnv:**
```python
# Scattered environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
WEB_HOST = os.getenv("WEB_HOST")
API_KEY = os.getenv("API_KEY")
```

**After OneEnv:**
```python
# Organized by namespace
db_url = oneenv.env("database").get("URL")
web_host = oneenv.env("web").get("HOST")
api_key = oneenv.env("api").get("KEY")
```

## How It Works

1. **Discovery**: OneEnv finds environment variable templates from installed packages
2. **Generation**: Creates consolidated `.env.example` files
3. **Namespace**: Loads variables into separate namespaces with fallback to common settings

## For Package Developers 📦

Create templates that users automatically discover:

```python
# mypackage/templates.py
def database_template():
    return {
        "groups": {
            "Database": {
                "DATABASE_URL": {
                    "description": "Database connection URL",
                    "default": "sqlite:///app.db",
                    "required": True
                }
            }
        }
    }
```

Register in `pyproject.toml`:
```toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
```

## Learn More 📚

### Step-by-Step Tutorials

#### 🌱 **Basics** (5-10 min each)
1. **[Basic dotenv Usage](docs/tutorials/01-basic-dotenv.md)** - Learn environment variable fundamentals and OneEnv basics
2. **[Auto Template Generation](docs/tutorials/02-template-generation.md)** - Discover how OneEnv automatically finds and generates environment templates  
3. **[Named Environments](docs/tutorials/03-named-environments.md)** - Master namespace management with intelligent fallback

#### 🚀 **Practical** (10-15 min each)
4. **[Multi-Service Management](docs/tutorials/04-multi-service.md)** - Configure complex applications with multiple services
5. **[Custom Templates](docs/tutorials/05-custom-templates.md)** - Create reusable project-specific templates
6. **[Production Best Practices](docs/tutorials/06-production-tips.md)** - Secure configuration management for production environments

#### ⚡ **Advanced** (15-20 min each)
7. **[Plugin Development](docs/tutorials/07-plugin-development.md)** - Build distributable OneEnv plugins for the community
8. **[CI/CD Integration](docs/tutorials/08-cicd-integration.md)** - Automate configuration management in your deployment pipeline

**Start here:** [Step 1: Basic dotenv Usage](docs/tutorials/01-basic-dotenv.md)

## License ⚖️

MIT License