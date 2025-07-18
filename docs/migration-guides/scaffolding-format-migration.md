# Scaffolding Format Migration Guide

## Overview

This guide helps you migrate from the legacy template format to the new **Scaffolding format** introduced in OneEnv v0.3.0+. The new format provides better organization, flexibility, and user experience while maintaining backward compatibility.

## Why Migrate?

### 🎯 Benefits of the New Format

| Feature | Legacy Format | New Scaffolding Format |
|---|---|---|
| **Organization** | Flat dictionary structure | Hierarchical categories and options |
| **Flexibility** | Single template per function | Multiple options per category |
| **User Experience** | Manual variable selection | Intelligent category-based selection |
| **Importance Levels** | Basic support | Enhanced Critical/Important/Optional |
| **Tooling** | Limited | Rich APIs for custom tools |
| **Scalability** | Difficult to manage | Easy to extend and maintain |

### 📈 Migration Impact

- **Backward Compatibility**: Legacy format continues to work
- **Enhanced Features**: New format provides additional capabilities
- **Tool Integration**: Better support for custom scaffolding tools
- **Future-Proof**: New format is the foundation for future features

## Migration Timeline

### 🗓️ Recommended Migration Schedule

| Phase | Duration | Actions |
|---|---|---|
| **Evaluation** | 1-2 weeks | Assess current templates, plan migration |
| **Development** | 2-4 weeks | Convert templates, test new format |
| **Testing** | 1-2 weeks | Validate migration, run tests |
| **Deployment** | 1 week | Deploy new templates, monitor |

### ⚠️ Important Notes

- **No Rush**: Legacy format will be supported indefinitely
- **Gradual Migration**: Migrate templates incrementally
- **Mixed Usage**: Legacy and new formats can coexist
- **Testing**: Always test new templates before deployment

## Format Comparison

### Legacy Format (Still Supported)

```python
@oneenv
def database_template():
    return {
        "DATABASE_URL": {
            "description": "Database connection URL",
            "default": "postgresql://user:pass@localhost:5432/db",
            "required": True
        },
        "DATABASE_POOL_SIZE": {
            "description": "Connection pool size",
            "default": "10",
            "required": False
        }
    }
```

### New Scaffolding Format

```python
def database_template():
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
                },
                "DATABASE_POOL_SIZE": {
                    "description": "Connection pool size",
                    "default": "10",
                    "required": False,
                    "importance": "important"
                }
            }
        },
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
                    "description": "Database connection timeout",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    ]
```

## Step-by-Step Migration

### Step 1: Analyze Current Templates

#### 1.1 Inventory Your Templates
```python
# List all current templates
from oneenv import collect_templates

templates = collect_templates()
print(f"Found {len(templates)} legacy templates")
for var_name, config in templates.items():
    print(f"  {var_name}: {config.get('description', 'No description')}")
```

#### 1.2 Identify Categories
Group your current templates by logical categories:

```python
# Example categorization
template_categories = {
    "Database": ["DATABASE_URL", "DATABASE_POOL_SIZE", "DATABASE_TIMEOUT"],
    "Cache": ["REDIS_URL", "REDIS_TTL", "REDIS_MAX_CONNECTIONS"],
    "API": ["API_KEY", "API_ENDPOINT", "API_TIMEOUT"],
    "Monitoring": ["LOG_LEVEL", "METRICS_ENABLED", "TRACE_ENABLED"]
}
```

### Step 2: Create New Format Templates

#### 2.1 Basic Conversion Pattern
```python
# Legacy template
@oneenv
def old_template():
    return {
        "DATABASE_URL": {
            "description": "Database connection",
            "default": "postgresql://localhost:5432/db",
            "required": True
        }
    }

# New format equivalent
def new_template():
    return [
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "Database connection",
                    "default": "postgresql://localhost:5432/db",
                    "required": True,
                    "importance": "critical"  # NEW: Add importance
                }
            }
        }
    ]
```

#### 2.2 Enhanced Conversion with Multiple Options
```python
# Legacy: Single template for all database types
@oneenv
def legacy_db_template():
    return {
        "DATABASE_URL": {
            "description": "Database connection URL",
            "default": "postgresql://user:pass@localhost:5432/db",
            "required": True
        },
        "DATABASE_TYPE": {
            "description": "Database type",
            "default": "postgresql",
            "required": True,
            "choices": ["postgresql", "mysql", "sqlite"]
        }
    }

# New: Separate options for each database type
def new_db_template():
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
                },
                "DATABASE_POOL_SIZE": {
                    "description": "Connection pool size",
                    "default": "10",
                    "required": False,
                    "importance": "important"
                }
            }
        },
        {
            "category": "Database",
            "option": "mysql",
            "env": {
                "DATABASE_URL": {
                    "description": "MySQL connection URL",
                    "default": "mysql://user:pass@localhost:3306/db",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_CHARSET": {
                    "description": "Database character set",
                    "default": "utf8mb4",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
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
                    "description": "Database connection timeout",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    ]
```

### Step 3: Add Importance Levels

Map your existing variables to importance levels:

```python
# Importance mapping guidelines
importance_mapping = {
    "critical": [
        "DATABASE_URL", "API_KEY", "SECRET_KEY", 
        "OPENAI_API_KEY", "ANTHROPIC_API_KEY"
    ],
    "important": [
        "DATABASE_POOL_SIZE", "REDIS_URL", "API_ENDPOINT",
        "LOG_LEVEL", "ENVIRONMENT"
    ],
    "optional": [
        "DATABASE_TIMEOUT", "REDIS_TTL", "DEBUG_MODE",
        "METRICS_ENABLED", "TRACE_ENABLED"
    ]
}

def add_importance_to_template(template_data):
    """Add importance levels to template variables"""
    for item in template_data:
        for var_name, var_config in item["env"].items():
            # Determine importance based on variable name
            if var_name in importance_mapping["critical"]:
                var_config["importance"] = "critical"
            elif var_name in importance_mapping["important"]:
                var_config["importance"] = "important"
            else:
                var_config["importance"] = "optional"
    
    return template_data
```

### Step 4: Update Entry Points

#### 4.1 Update pyproject.toml
```toml
# Remove old entry point (if using entry points)
[project.entry-points."oneenv.templates"]
# old_template = "mypackage.old_templates:old_template"  # REMOVE

# Add new entry point
new_template = "mypackage.templates:new_template"  # ADD
```

#### 4.2 Update Package Structure
```
mypackage/
├── __init__.py
├── templates.py          # NEW: New format templates
├── old_templates.py      # KEEP: Legacy templates (for compatibility)
└── ...
```

### Step 5: Testing and Validation

#### 5.1 Validate New Templates
```python
# Test your new templates
from oneenv.models import validate_scaffolding_format

def test_new_template():
    template_data = new_template()
    
    try:
        validate_scaffolding_format(template_data)
        print("✅ Template validation successful")
        
        # Test structure
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

test_new_template()
```

#### 5.2 Test with OneEnv APIs
```python
# Test with new APIs
import oneenv

# Test structure discovery
structure = oneenv.get_all_template_structure()
print(f"Discovered structure: {structure}")

# Test specific category
if oneenv.has_category("Database"):
    options = oneenv.get_options("Database")
    print(f"Database options: {options}")

# Test template generation
selections = [
    {"category": "Database", "option": "postgres"}
]
content = oneenv.generate_template("test.env", selections)
print("Template generation successful!")
```

## Complex Migration Scenarios

### Scenario 1: Large Monolithic Template

**Before:**
```python
@oneenv
def large_template():
    return {
        "DATABASE_URL": {"description": "DB URL", "default": "postgresql://..."},
        "REDIS_URL": {"description": "Cache URL", "default": "redis://..."},
        "API_KEY": {"description": "API Key", "default": ""},
        "LOG_LEVEL": {"description": "Log level", "default": "INFO"},
        "METRICS_ENABLED": {"description": "Metrics", "default": "true"},
        # ... 20+ more variables
    }
```

**After:**
```python
def comprehensive_template():
    return [
        # Database category
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
        },
        # Cache category
        {
            "category": "Cache",
            "option": "redis",
            "env": {
                "REDIS_URL": {
                    "description": "Redis cache URL",
                    "default": "redis://localhost:6379/0",
                    "required": False,
                    "importance": "important"
                }
            }
        },
        # API category
        {
            "category": "API",
            "option": "standard",
            "env": {
                "API_KEY": {
                    "description": "API authentication key",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        # Monitoring category
        {
            "category": "Monitoring",
            "option": "basic",
            "env": {
                "LOG_LEVEL": {
                    "description": "Application log level",
                    "default": "INFO",
                    "required": False,
                    "importance": "important",
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR"]
                },
                "METRICS_ENABLED": {
                    "description": "Enable metrics collection",
                    "default": "true",
                    "required": False,
                    "importance": "optional",
                    "choices": ["true", "false"]
                }
            }
        }
    ]
```

### Scenario 2: Multiple Legacy Templates

**Before:**
```python
@oneenv
def db_template():
    return {"DATABASE_URL": {...}}

@oneenv
def cache_template():
    return {"REDIS_URL": {...}}

@oneenv
def api_template():
    return {"API_KEY": {...}}
```

**After:**
```python
def unified_template():
    return [
        {
            "category": "Database",
            "option": "postgres",
            "env": {"DATABASE_URL": {...}}
        },
        {
            "category": "Cache",
            "option": "redis",
            "env": {"REDIS_URL": {...}}
        },
        {
            "category": "API",
            "option": "standard",
            "env": {"API_KEY": {...}}
        }
    ]
```

## Migration Checklist

### 📋 Pre-Migration Checklist

- [ ] **Inventory current templates** - List all existing templates
- [ ] **Identify categories** - Group related variables
- [ ] **Plan options** - Determine multiple options per category
- [ ] **Assess importance levels** - Classify variables by importance
- [ ] **Review dependencies** - Check package dependencies
- [ ] **Create test plan** - Define testing strategy

### 🔄 During Migration Checklist

- [ ] **Convert templates** - Transform to new format
- [ ] **Add importance levels** - Assign critical/important/optional
- [ ] **Update entry points** - Modify pyproject.toml
- [ ] **Validate format** - Test with validation functions
- [ ] **Test APIs** - Verify new API functions work
- [ ] **Update documentation** - Document new templates

### ✅ Post-Migration Checklist

- [ ] **Functional testing** - Test all new templates
- [ ] **Integration testing** - Test with OneEnv APIs
- [ ] **Performance testing** - Check generation speed
- [ ] **Documentation update** - Update user guides
- [ ] **Team training** - Educate team on new format
- [ ] **Monitor usage** - Track adoption and issues

## Common Migration Issues

### Issue 1: Template Not Discovered

**Problem:** New templates not appearing in `oneenv template --structure`

**Solutions:**
```python
# Check entry points registration
# In pyproject.toml:
[project.entry-points."oneenv.templates"]
mytemplate = "mypackage.templates:template_function"

# Verify installation
pip install -e .  # Reinstall in development mode

# Debug discovery
import oneenv
structure = oneenv.get_all_template_structure()
print(structure)
```

### Issue 2: Validation Errors

**Problem:** `validate_scaffolding_format()` fails

**Solutions:**
```python
# Common validation issues:
# 1. Missing required fields
{
    "category": "Database",  # Required
    "option": "postgres",    # Required
    "env": {                # Required
        "VAR_NAME": {
            "description": "...",  # Required
            "default": "...",      # Required
            "required": True,      # Required
            "importance": "critical"  # Required
        }
    }
}

# 2. Invalid importance levels
# Use: "critical", "important", "optional"
# Not: "high", "medium", "low"

# 3. Empty categories or options
# Ensure all strings are non-empty
```

### Issue 3: Duplicate Variables

**Problem:** Same variable appears in multiple options

**Solutions:**
```python
# This is actually allowed and expected!
# Different options can have the same variable name
[
    {
        "category": "Database",
        "option": "postgres",
        "env": {
            "DATABASE_URL": {  # Same variable name
                "description": "PostgreSQL connection URL",
                "default": "postgresql://...",
                "required": True,
                "importance": "critical"
            }
        }
    },
    {
        "category": "Database",
        "option": "mysql",
        "env": {
            "DATABASE_URL": {  # Same variable name, different default
                "description": "MySQL connection URL",
                "default": "mysql://...",
                "required": True,
                "importance": "critical"
            }
        }
    }
]
```

## Migration Tools

### Automated Migration Script

```python
#!/usr/bin/env python3
"""
OneEnv Legacy to Scaffolding Migration Tool
"""

import inspect
import ast
from typing import Dict, List, Any

def migrate_legacy_template(legacy_function) -> List[Dict]:
    """
    Convert legacy template function to scaffolding format
    """
    # Get the template data
    template_data = legacy_function()
    
    # Simple migration - creates single option per category
    # You may need to customize this based on your specific needs
    
    migrated = []
    
    # Group variables by category (you'll need to define this mapping)
    category_mapping = {
        "DATABASE": "Database",
        "REDIS": "Cache",
        "API": "API",
        "LOG": "Monitoring",
        # Add more mappings as needed
    }
    
    # Default importance mapping
    importance_mapping = {
        "URL": "critical",
        "KEY": "critical",
        "SECRET": "critical",
        "HOST": "important",
        "PORT": "important",
        "LEVEL": "important",
        "TIMEOUT": "optional",
        "DEBUG": "optional",
        "ENABLED": "optional"
    }
    
    # Group variables by category
    categories = {}
    for var_name, var_config in template_data.items():
        # Determine category based on variable name
        category = "Misc"  # Default category
        for prefix, cat in category_mapping.items():
            if var_name.startswith(prefix):
                category = cat
                break
        
        if category not in categories:
            categories[category] = {}
        
        # Add importance level
        var_config = dict(var_config)
        importance = "optional"  # Default
        for suffix, imp in importance_mapping.items():
            if var_name.endswith(suffix):
                importance = imp
                break
        var_config["importance"] = importance
        
        categories[category][var_name] = var_config
    
    # Create scaffolding format
    for category, variables in categories.items():
        migrated.append({
            "category": category,
            "option": "default",  # You may want to customize this
            "env": variables
        })
    
    return migrated

# Example usage
if __name__ == "__main__":
    # Import your legacy template
    from mypackage.old_templates import legacy_template
    
    # Migrate
    new_template_data = migrate_legacy_template(legacy_template)
    
    # Print new format
    print("New scaffolding format:")
    import json
    print(json.dumps(new_template_data, indent=2))
```

## Testing Your Migration

### Comprehensive Test Suite

```python
import pytest
import oneenv
from oneenv.models import validate_scaffolding_format

class TestMigration:
    def test_template_validation(self):
        """Test that migrated templates are valid"""
        from mypackage.templates import new_template
        
        template_data = new_template()
        
        # Should not raise any validation errors
        validate_scaffolding_format(template_data)
        
        # Check structure
        categories = set()
        for item in template_data:
            categories.add(item["category"])
        
        assert len(categories) > 0, "Should have at least one category"
    
    def test_api_integration(self):
        """Test that new templates work with OneEnv APIs"""
        # Test structure discovery
        structure = oneenv.get_all_template_structure()
        assert isinstance(structure, dict)
        
        # Test category checking
        for category in structure.keys():
            assert oneenv.has_category(category)
            options = oneenv.get_options(category)
            assert len(options) > 0
    
    def test_template_generation(self):
        """Test template generation with new format"""
        structure = oneenv.get_all_template_structure()
        
        if structure:
            # Test with first available option
            first_category = next(iter(structure.keys()))
            first_option = structure[first_category][0]
            
            selections = [{"category": first_category, "option": first_option}]
            content = oneenv.generate_template("test.env", selections)
            
            assert content, "Generated content should not be empty"
            assert first_category.upper() in content.upper(), "Should contain category name"
    
    def test_importance_levels(self):
        """Test that importance levels are properly assigned"""
        from mypackage.templates import new_template
        
        template_data = new_template()
        
        importance_levels = set()
        for item in template_data:
            for var_config in item["env"].values():
                importance_levels.add(var_config["importance"])
        
        # Should have at least one importance level
        assert len(importance_levels) > 0
        
        # Should only use valid importance levels
        valid_levels = {"critical", "important", "optional"}
        assert importance_levels.issubset(valid_levels)
```

## Best Practices for Migration

### 1. **Incremental Migration**
- Migrate one category at a time
- Test each category before moving to the next
- Keep legacy templates working during migration

### 2. **Clear Category Design**
- Use logical, intuitive category names
- Group related variables together
- Avoid overly broad or narrow categories

### 3. **Meaningful Options**
- Create options that represent real choices
- Use descriptive option names
- Consider user workflow when designing options

### 4. **Proper Importance Levels**
- **Critical**: Application won't work without it
- **Important**: Needed for production use
- **Optional**: Fine-tuning and optimization

### 5. **Comprehensive Testing**
- Test with validation functions
- Test with OneEnv APIs
- Test actual template generation
- Test in different environments

## Getting Help

### 🆘 Support Resources

- **Documentation**: [OneEnv Documentation](../../README.md)
- **Tutorials**: [Template Creation Tutorial](../tutorials/09-new-template-creation.md)
- **API Reference**: [Scaffolding API](../api-reference/scaffolding-api.md)
- **Examples**: [Practical Examples](../tutorials/11-practical-guide.md)

### 📧 Community Support

- **Issues**: Report migration issues on GitHub
- **Discussions**: Join community discussions
- **Examples**: Share your migration experiences

---

**🎉 Congratulations!** You now have a comprehensive understanding of how to migrate from legacy templates to the new Scaffolding format. The migration process may seem complex, but the benefits in terms of organization, flexibility, and user experience make it worthwhile.

Remember: **Legacy templates will continue to work**, so you can migrate at your own pace and comfort level.