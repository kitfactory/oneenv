# Tutorial 9: New Template Creation Method

**Time:** 15-20 minutes  
**Target:** Package developers  
**Prerequisites:** Basic Python, package development knowledge

## Overview

Learn how to create OneEnv templates using the new Scaffolding format, which provides better structure and flexibility compared to the legacy groups format.

## What You'll Learn

- Understand the Scaffolding format structure
- Create category-based templates with multiple options
- Use importance levels and validation features
- Register templates via entry-points
- Test and validate your templates

## 1. Understanding the Scaffolding Format (5 minutes)

### Key Concepts

The new Scaffolding format organizes templates around **categories** and **options**:

- **Category**: High-level grouping (e.g., "Database", "VectorStore")
- **Option**: Specific implementation (e.g., "postgres", "sqlite")
- **Environment Variables**: Configuration for each option

### Basic Structure

```python
def my_template():
    return [
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL connection URL",
                    "default": "postgresql://user:pass@localhost:5432/db",
                    "required": True,
                    "importance": "critical"
                }
            }
        }
    ]
```

### Importance Levels

- **critical**: Essential for application operation
- **important**: Should be configured for production
- **optional**: Fine-tuning settings (defaults sufficient)

## 2. Creating Your First Template (5 minutes)

Let's create a simple database template for your package.

### Step 1: Create the Template File

Create `my_package/templates.py`:

```python
def database_template():
    """Database configuration templates for MyPackage"""
    return [
        {
            "category": "Database",
            "option": "sqlite",
            "env": {
                "DATABASE_URL": {
                    "description": "SQLite database file path",
                    "default": "sqlite:///app.db",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_TIMEOUT": {
                    "description": "Database connection timeout in seconds",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL connection URL",
                    "default": "postgresql://user:pass@localhost:5432/mydb",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "Connection pool size",
                    "default": "10",
                    "required": False,
                    "importance": "important"
                },
                "DATABASE_SSL_MODE": {
                    "description": "SSL mode for connections",
                    "default": "prefer",
                    "required": False,
                    "importance": "optional",
                    "choices": ["require", "prefer", "disable"]
                }
            }
        }
    ]
```

### Step 2: Test Your Template

Create a test script to validate your template:

```python
# test_template.py
from my_package.templates import database_template
from oneenv.models import validate_scaffolding_format

def test_template():
    template_data = database_template()
    
    try:
        validate_scaffolding_format(template_data)
        print("✅ Template validation successful!")
        
        # Show structure
        categories = {}
        for item in template_data:
            category = item["category"]
            option = item["option"]
            if category not in categories:
                categories[category] = []
            categories[category].append(option)
        
        print(f"📊 Template structure: {categories}")
        
    except Exception as e:
        print(f"❌ Template validation failed: {e}")

if __name__ == "__main__":
    test_template()
```

## 3. Advanced Template Features (5 minutes)

### Multiple Categories

Create templates that span multiple technology categories:

```python
def full_stack_template():
    """Complete application stack template"""
    return [
        # Database options
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "Primary database connection",
                    "default": "postgresql://user:pass@localhost:5432/app",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        
        # Cache options
        {
            "category": "Cache",
            "option": "redis",
            "env": {
                "REDIS_URL": {
                    "description": "Redis server connection",
                    "default": "redis://localhost:6379/0",
                    "required": False,
                    "importance": "important"
                },
                "REDIS_MAX_CONNECTIONS": {
                    "description": "Maximum Redis connections",
                    "default": "50",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # API options
        {
            "category": "API",
            "option": "fastapi",
            "env": {
                "API_HOST": {
                    "description": "API server host",
                    "default": "0.0.0.0",
                    "required": False,
                    "importance": "important"
                },
                "API_PORT": {
                    "description": "API server port",
                    "default": "8000",
                    "required": False,
                    "importance": "important"
                },
                "API_WORKERS": {
                    "description": "Number of worker processes",
                    "default": "4",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    ]
```

### Validation and Choices

Use validation features for better user experience:

```python
def api_template():
    return [
        {
            "category": "API",
            "option": "production",
            "env": {
                "LOG_LEVEL": {
                    "description": "Application log level",
                    "default": "INFO",
                    "required": False,
                    "importance": "important",
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                },
                "ENVIRONMENT": {
                    "description": "Deployment environment",
                    "default": "production",
                    "required": True,
                    "importance": "critical",
                    "choices": ["development", "staging", "production"]
                }
            }
        }
    ]
```

## 4. Entry-points Registration (3 minutes)

### Step 1: Update pyproject.toml

Add your template to the OneEnv entry-points:

```toml
[project.entry-points."oneenv.templates"]
database = "my_package.templates:database_template"
fullstack = "my_package.templates:full_stack_template"
api = "my_package.templates:api_template"
```

### Step 2: Test Registration

After installing your package, test the registration:

```bash
# Install your package in development mode
pip install -e .

# Check if OneEnv can find your templates
oneenv template --structure
```

You should see your categories listed in the output.

## 5. Practical Exercise (2 minutes)

Create a template for your own package:

1. **Identify categories** your package needs (Database, Cache, API, etc.)
2. **Define options** for each category (postgres/mysql, redis/memcached, etc.)
3. **List environment variables** each option requires
4. **Set importance levels** (critical/important/optional)
5. **Add validation** using choices where appropriate

### Example Exercise

Create a template for a web scraping package:

```python
def scraper_template():
    return [
        {
            "category": "Storage",
            "option": "filesystem",
            "env": {
                "STORAGE_PATH": {
                    "description": "Directory for storing scraped data",
                    "default": "./scraped_data",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        {
            "category": "Storage", 
            "option": "s3",
            "env": {
                "AWS_BUCKET": {
                    "description": "S3 bucket for scraped data",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "AWS_ACCESS_KEY_ID": {
                    "description": "AWS access key",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        {
            "category": "Rate_Limiting",
            "option": "basic",
            "env": {
                "REQUESTS_PER_SECOND": {
                    "description": "Maximum requests per second",
                    "default": "1",
                    "required": False,
                    "importance": "important"
                },
                "DELAY_BETWEEN_REQUESTS": {
                    "description": "Delay between requests in seconds",
                    "default": "1.0",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    ]
```

## Benefits of the New Format

✅ **Better Organization**: Categories and options provide clear structure  
✅ **Flexible Selection**: Users can choose specific combinations  
✅ **Importance Hierarchy**: Critical settings are highlighted  
✅ **Validation Support**: Choices and required fields prevent errors  
✅ **Discoverability**: Easy to explore options with CLI tools  

## Next Steps

- **Tutorial 10**: Learn how to create scaffolding tools that use your templates
- **Tutorial 11**: See practical examples in real-world projects
- Explore existing templates for inspiration: `oneenv template --structure`

## Quick Reference

### Template Structure
```python
{
    "category": "CategoryName",
    "option": "option_name", 
    "env": {
        "VAR_NAME": {
            "description": "Variable description",
            "default": "default_value",
            "required": True|False,
            "importance": "critical"|"important"|"optional",
            "choices": ["choice1", "choice2"]  # optional
        }
    }
}
```

### Entry-points Registration
```toml
[project.entry-points."oneenv.templates"]
template_name = "package.module:function_name"
```

---

**🎉 Congratulations!** You now know how to create OneEnv templates using the new Scaffolding format. Your templates will be automatically discoverable by users and scaffolding tools.