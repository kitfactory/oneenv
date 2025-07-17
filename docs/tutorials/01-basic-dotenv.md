# Step 1: Basic dotenv Usage

**Duration:** 5-10 minutes  
**Difficulty:** Beginner

## Learning Objectives

- Understand basic environment variable concepts
- Learn how to create and use `.env` files
- Practice basic environment variable loading with OneEnv

## Purpose & Benefits

**Why this step matters:**
- **Foundation Building**: Master environment variable fundamentals before advanced features
- **Best Practices**: Learn secure configuration management from the start  
- **Immediate Value**: Replace hardcoded values with flexible configuration
- **Team Collaboration**: Enable consistent development environments across team members

## Traditional Problems

### 1. Hardcoding Issues

```python
# Bad example: hardcoded configuration
def connect_to_database():
    host = "localhost"
    port = 5432
    database = "myapp"
    username = "admin"
    password = "secret123"
    # Different settings needed for production...
```

### 2. OS Environment Variable Issues

```python
import os

# Scattered settings, difficult to manage
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/myapp")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

## OneEnv Solutions

### Step 1: Install OneEnv

```bash
pip install oneenv
```

### Step 2: Create .env file

Create a `.env` file in your project root directory:

```bash
# .env
DATABASE_URL=postgresql://localhost:5432/myapp
SECRET_KEY=your-secret-key-here
DEBUG=True
API_KEY=your-api-key
LOG_LEVEL=INFO
```

### Step 3: Load with OneEnv

```python
# app.py
import oneenv
import os

# Load environment variables
oneenv.load_dotenv()

# Get configuration
database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG", "False").lower() == "true"

print(f"Database URL: {database_url}")
print(f"Debug mode: {debug}")
```

## Practical Exercises

### Exercise 1: Basic Configuration Management

1. Create a new directory:
```bash
mkdir oneenv-tutorial
cd oneenv-tutorial
```

2. Create `.env` file:
```bash
APP_NAME=My Tutorial App
PORT=8000
DATABASE_URL=sqlite:///tutorial.db
SECRET_KEY=tutorial-secret-key
DEBUG=True
```

3. Create Python script (`basic_config.py`):
```python
import oneenv
import os

# Load environment variables
oneenv.load_dotenv()

# Display configuration
print("=== Application Configuration ===")
print(f"App Name: {os.getenv('APP_NAME')}")
print(f"Port: {os.getenv('PORT')}")
print(f"Database: {os.getenv('DATABASE_URL')}")
print(f"Debug Mode: {os.getenv('DEBUG')}")
```

4. Run:
```bash
python basic_config.py
```

### Exercise 2: Default Values

Add default values to your configuration:

```python
# config_with_defaults.py
import oneenv
import os

oneenv.load_dotenv()

# Get configuration with defaults
app_name = os.getenv("APP_NAME", "Default App")
port = int(os.getenv("PORT", "3000"))
debug = os.getenv("DEBUG", "False").lower() == "true"
log_level = os.getenv("LOG_LEVEL", "INFO")

print("=== Configuration with Defaults ===")
print(f"App Name: {app_name}")
print(f"Port: {port}")
print(f"Debug: {debug}")
print(f"Log Level: {log_level}")
```

### Exercise 3: Get Configuration as Dictionary

```python
# config_as_dict.py
import oneenv

# Get configuration as dictionary
config = oneenv.dotenv_values()

print("=== All Configuration ===")
for key, value in config.items():
    print(f"{key}: {value}")
```

## OneEnv Benefits

### 1. Simplicity
```python
# Traditional approach
from dotenv import load_dotenv
load_dotenv()

# OneEnv approach
import oneenv
oneenv.load_dotenv()
```

### 2. Type Safety
OneEnv provides type safety features with Pydantic support in future versions.

### 3. Extensibility
Prepares you for the automatic template generation features you'll learn next.

## Key Takeaways

**What you've learned:**
- ✅ **Environment Variables**: Core concepts and .env file structure
- ✅ **OneEnv Basics**: Simple loading and configuration access
- ✅ **Default Values**: Fallback strategies for missing configuration
- ✅ **Best Practices**: Separation of code and configuration

**Why this matters:**
- **Security**: No hardcoded secrets in source code
- **Flexibility**: Easy configuration changes without code modification
- **Team Collaboration**: Consistent development environments
- **Production Ready**: Foundation for environment-specific configuration

## Next Steps

You've mastered basic dotenv usage with OneEnv. Next, discover OneEnv's powerful automatic template generation feature.

**→ [Step 2: Auto Template Generation](02-template-generation.md)**

## Reference Materials

- [python-dotenv documentation](https://github.com/theskumar/python-dotenv)
- [12-Factor App: Config](https://12factor.net/config)
- [OneEnv Main Documentation](../../README.md)

## Frequently Asked Questions

### Q: Should .env files be committed to Git?
A: No. `.env` files contain sensitive information and should be added to `.gitignore`. Instead, commit `.env.example` files.

### Q: What if environment variables aren't loading?
A: Ensure the `.env` file is in the same directory as your Python script. For different locations, specify the path: `oneenv.load_dotenv("path/to/.env")`.

### Q: How do I handle different environments (dev/staging/prod)?
A: Use different `.env` files for each environment, which you'll learn more about in the Named Environments tutorial.