# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OneEnv is a Python package that simplifies environment variable management through a decorator-based system. It wraps `python-dotenv` and allows libraries to declare their environment variable templates using the `@oneenv` decorator, then generates consolidated `.env.example` files.

## Architecture

### Core Components

- **Decorator System**: The `@oneenv` decorator registers functions that return environment variable templates
- **Template Registry**: Global `_TEMPLATE_REGISTRY` list stores all decorated functions
- **Template Collection**: `collect_templates()` processes all registered functions and handles duplicates
- **CLI Interface**: `cli.py` provides command-line access to template generation and diff functionality

### Key Files

- `src/oneenv/__init__.py`: Core functionality, decorators, template processing
- `src/oneenv/cli.py`: Command-line interface
- `tests/test_oneenv.py`: Comprehensive test suite
- `examples/example_usage.py`: Usage demonstration

## Development Commands

### Testing
```bash
pytest tests
```

### Installation (Development)
```bash
pip install -e .
```

### CLI Usage
```bash
# Generate .env.example file
oneenv template [-o OUTPUT_FILE] [-d]

# Compare environment files
oneenv diff previous.env current.env
```

## Enhanced Architecture (v0.1.6+)

### Entry-points Plugin System
OneEnv now supports plugin-based template discovery via entry-points:

```toml
# In external package's pyproject.toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
web = "mypackage.templates:web_template"
```

### Pydantic Models for Type Safety
The system now uses Pydantic models for type-safe template processing:

- `EnvVarConfig`: Individual environment variable configuration
- `EnvTemplate`: Template containing multiple variables with source tracking
- `TemplateCollection`: Collection of templates with conflict resolution

### Backward Compatibility
The existing `@oneenv` decorator continues to work unchanged:

```python
@oneenv
def my_template():
    return {
        "MY_VAR": {
            "description": "Required field",
            "default": "optional",
            "required": False,
            "choices": ["optional", "list"]
        }
    }
```

### Enhanced CLI
The CLI now supports debug output to show plugin discovery:

```bash
oneenv template -d  # Shows discovered plugins and legacy templates
```

### New Core Files
- `src/oneenv/models.py`: Pydantic model definitions
- `src/oneenv/core.py`: Enhanced core system with plugin support
- `tests/test_enhanced_system.py`: Tests for new functionality

### Migration Notes
- All existing code continues to work without changes
- New plugin system runs alongside legacy decorator system
- Type validation is now performed on all templates
- Entry-points are automatically discovered from installed packages