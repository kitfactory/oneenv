# Step 2: Auto Template Generation

**Duration:** 5-10 minutes  
**Difficulty:** Beginner

## Learning Objectives

- Understand OneEnv's automatic template generation feature
- Experience package-based environment variable discovery
- Learn template field configuration methods
- Verify the process using debug mode

## Purpose & Benefits

**Why this step matters:**
- **Automation**: Eliminate manual `.env.example` file creation and maintenance
- **Consistency**: Ensure all required environment variables are documented
- **Discovery**: Automatically find settings from installed packages
- **Team Productivity**: Reduce onboarding time for new developers
- **Maintenance**: Keep configuration documentation up-to-date automatically

## Traditional Problems

### Manual Template Creation
```bash
# Traditional approach: manually create .env.example
echo "DATABASE_URL=postgresql://localhost:5432/mydb" > .env.example
echo "SECRET_KEY=your-secret-key" >> .env.example
echo "REDIS_URL=redis://localhost:6379" >> .env.example
# Manually research and add required variables for each package...
```

**Pain Points:**
- 😓 Time-consuming research for each package's requirements
- 😤 Easily miss critical configuration variables
- 😱 Inconsistent documentation across projects
- 🤯 Manual updates when dependencies change

## OneEnv Automatic Template Generation

### Step 1: Basic Template Generation

```bash
# Run in your project directory
oneenv template
```

**What happens:**
- 🔍 **Package Discovery**: Scans installed packages for environment templates
- 📝 **Template Collection**: Gathers all environment variable definitions
- 🔄 **Smart Merging**: Handles duplicate variables intelligently
- 📋 **Generation**: Creates comprehensive `.env.example` file

### Step 2: Debug Mode for Detailed Insight

```bash
# Show detailed discovery process
oneenv template -d
```

**Example output:**
```
=== OneEnv Template Generation (Debug Mode) ===
🔍 Discovering plugins via entry-points...
📦 Found plugin: myproject.config -> my_template
📦 Found plugin: database-lib -> db_template

🔍 Scanning legacy @oneenv decorators...
📝 Found decorator: custom_app_config

🔄 Processing templates...
⚠️  Duplicate variable detected: DATABASE_URL
    - Defined in: myproject.config, database-lib
    - Using configuration from: myproject.config

✅ Generated template with 8 variables across 3 groups
```

### Step 3: Custom Output File

```bash
# Generate to different filename
oneenv template -o custom.env.example
```

## Practical Exercises

### Exercise 1: Project Template Creation

1. Create project directory:
```bash
mkdir template-tutorial
cd template-tutorial
```

2. Create custom template (`project_config.py`):
```python
from oneenv import oneenv

@oneenv
def app_template():
    return {
        "groups": {
            "Application": {
                "APP_NAME": {
                    "description": "Application name",
                    "default": "Tutorial App",
                    "required": True,
                    "importance": "critical"
                },
                "APP_VERSION": {
                    "description": "Application version",
                    "default": "1.0.0",
                    "importance": "important"
                }
            },
            "Database": {
                "DATABASE_URL": {
                    "description": "Database connection URL",
                    "default": "sqlite:///app.db",
                    "required": True,
                    "importance": "critical"
                }
            },
            "Settings": {
                "DEBUG": {
                    "description": "Debug mode",
                    "default": "False",
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            }
        }
    }
```

3. Import template to register:
```python
# Import to register the template
import project_config
```

4. Generate template:
```bash
python -c "import project_config" && oneenv template
```

### Exercise 2: Mixed Template Formats

Try both new and legacy formats:

```python
# legacy_config.py
from oneenv import oneenv

@oneenv
def legacy_template():
    return {
        "LOG_LEVEL": {
            "description": "Logging level setting",
            "default": "INFO",
            "choices": ["DEBUG", "INFO", "WARNING", "ERROR"],
            "group": "Logging",
            "importance": "optional"
        },
        "MAX_WORKERS": {
            "description": "Number of workers",
            "default": "4",
            "group": "Performance",
            "importance": "important"
        }
    }
```

## Template Field Reference

### Basic Fields (Required)
- **`description`**: Variable description (required)

### Optional Fields
- **`default`**: Default value
- **`required`**: Whether required (true/false)
- **`choices`**: List of valid options
- **`group`**: Group name (for legacy format)
- **`importance`**: Importance level

### Importance Levels
- **`critical`**: Essential for application operation
- **`important`**: Should be configured for production
- **`optional`**: Fine-tuning settings (defaults sufficient)

### Groups Format (v0.3.1+)
```python
{
    "groups": {
        "Group Name": {
            "VARIABLE_NAME": {
                "description": "Description",
                "default": "value",
                "importance": "critical"
            }
        }
    }
}
```

## Generated Template Structure

```bash
# Auto-generated by OneEnv

# ========== CRITICAL: Essential Settings for Application Operation ==========

# ----- Application -----

# Application name
# Required
APP_NAME=Tutorial App

# ----- Database -----

# Database connection URL
# Required
DATABASE_URL=sqlite:///app.db

# ========== IMPORTANT: Settings to Configure for Production Use ==========

# ----- Performance -----

# Number of workers
MAX_WORKERS=4

# ========== OPTIONAL: Fine-tuning Settings (Defaults are Sufficient) ==========

# ----- Settings -----

# Debug mode
# Choices: True, False
DEBUG=False
```

## Smart Duplicate Handling

When multiple packages define the same variable:

```bash
# (Defined in: myproject.config, database-lib)
# myproject.config: Application database URL
# database-lib: Database library connection settings
# Required
DATABASE_URL=sqlite:///app.db
```

**How it works:**
- ✅ **Single entry**: Each variable appears only once
- 📝 **Merged descriptions**: All package descriptions combined
- ⚙️ **First wins**: Configuration values use first package's settings
- 📋 **Source tracking**: Shows which packages define each variable

## CLI Options Detail

### `-d, --debug`
Shows discovery process and template generation details

### `-o, --output`
Specify output filename (default: `.env.example`)

```bash
# Usage examples
oneenv template -d -o my-template.env
```

## Key Takeaways

**What you've learned:**
- ✅ **Automatic Discovery**: OneEnv finds templates from installed packages
- ✅ **Template Generation**: Single command creates comprehensive documentation
- ✅ **Smart Merging**: Intelligent handling of duplicate variables
- ✅ **Debug Process**: Understanding how templates are discovered and processed

**Benefits gained:**
- **Time Savings**: No more manual template creation
- **Completeness**: Never miss required environment variables
- **Consistency**: Standardized documentation across projects
- **Maintenance**: Automatic updates when dependencies change

## Next Steps

You've mastered automatic template generation. Next, learn OneEnv's powerful namespace management feature.

**→ [Step 3: Named Environments Basics](03-named-environments.md)**

## Frequently Asked Questions

### Q: What if no template is generated?
A: Use `oneenv template -d` for debug mode to check if plugins are being discovered.

### Q: How can I change duplicate variable priority?
A: Currently, the first discovered package takes precedence. You can adjust this by modifying entry-points order in pyproject.toml.

### Q: Can I use custom group names?
A: Yes, use the groups format to set any group names you prefer.