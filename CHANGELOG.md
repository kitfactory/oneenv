# Changelog

All notable changes to OneEnv will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-15

### 🎉 Major Release: Revolutionary Plugin System

This release introduces a complete overhaul of OneEnv with revolutionary new features that make environment variable management incredibly simple.

### ✨ Added
- **🔌 Entry-points Plugin System**: Packages can now automatically provide environment variable templates via `[project.entry-points."oneenv.templates"]`
- **🎨 Smart Duplicate Variable Handling**: When multiple packages define the same variable, OneEnv intelligently merges descriptions while maintaining configuration consistency
- **🛡️ Pydantic Model Integration**: Type-safe environment variable templates with runtime validation
- **⚡ Zero Configuration Setup**: Automatic discovery of templates from installed packages - no imports or manual registration needed
- **📋 Enhanced CLI with Debug Mode**: `-d/--debug` flag shows discovered plugins and duplicate variables
- **🔄 Improved Template Generation**: Variables are now sorted alphabetically and grouped by source
- **📚 Comprehensive Documentation**: Completely rewritten README with detailed examples and best practices

### 🔧 Enhanced
- **Backward Compatibility**: Existing `@oneenv` decorators work seamlessly alongside the new plugin system
- **Better Error Messages**: Pydantic validation provides clear error messages for invalid templates
- **Source Tracking**: Each variable shows which packages define it
- **Description Merging**: Multiple package descriptions are intelligently combined

### 🐛 Fixed
- **CLI Parameter Issue**: Fixed `generate_env_example()` function to properly accept debug parameter
- **Python Version Support**: Updated to support Python 3.10+
- **Import Path Issues**: Resolved module import conflicts in the new system

### 📦 Dependencies
- Added `pydantic>=2.0.0` for type-safe models
- Added `typing-extensions>=4.0.0` for Python <3.10 compatibility

### 🏗️ Internal Changes
- **New Core Architecture**: `src/oneenv/core.py` - Enhanced system with plugin support
- **Pydantic Models**: `src/oneenv/models.py` - Type-safe template definitions
- **Enhanced Testing**: `tests/test_enhanced_system.py` - Comprehensive tests for new features
- **Integration Layer**: Updated `src/oneenv/__init__.py` to provide unified API

### 📖 Documentation
- **Complete README Rewrite**: Both English and Japanese versions updated with new features
- **Plugin Development Guide**: Detailed instructions for creating OneEnv plugins
- **Real-world Examples**: Django + FastAPI + Redis integration examples
- **Migration Guide**: Smooth transition path from v0.1.x to v0.2.0

### 🎯 Breaking Changes
- **Minimum Python Version**: Now requires Python 3.10+ (was 3.11+)
- **New Dependencies**: Requires `pydantic` and `typing-extensions`

### 🚀 Migration Guide

**For End Users:**
No changes needed! Your existing `@oneenv` decorators continue to work.

**For Package Developers:**
Consider migrating to the new plugin system for automatic discovery:

```toml
# Add to your pyproject.toml
[project.entry-points."oneenv.templates"]
myfeature = "mypackage.templates:my_template_function"
```

---

## [0.1.6] - Previous Release

### Features
- Basic `@oneenv` decorator functionality
- Template collection and `.env.example` generation
- Diff functionality for environment files
- Command-line interface

### Requirements
- Python 3.11+
- python-dotenv>=1.0.1