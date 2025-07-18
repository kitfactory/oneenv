# Step 5: Custom Templates

**Duration:** 10-15 minutes  
**Difficulty:** Intermediate

## Learning Objectives

- Learn how to create custom project templates
- Understand when to use the new Groups format vs legacy format
- Design project-specific configuration templates
- Create reusable template structures

## Template Basic Structure

OneEnv supports two formats for defining templates:

### 1. **New Groups Format (v0.3.1+)**
```python
@oneenv
def webapp_template():
    return {
        "groups": {
            "Group Name": {
                "VARIABLE_NAME": {config}
            }
        }
    }
```

### 2. **Legacy Format**
```python
@oneenv
def legacy_template():
    return {
        "VARIABLE_NAME": {
            "group": "Group Name",
            # Other configuration
        }
    }
```

## Hands-on Exercises

### Exercise 1: Web Application Template

1. Create project directory:
```bash
mkdir custom-template-project
cd custom-template-project
```

2. Create custom template (`project_templates.py`):

```python
from oneenv import oneenv

@oneenv
def webapp_core_template():
    """
    Core web application configuration template
    Using the new Groups format
    """
    return {
        "groups": {
            "Application": {
                "APP_NAME": {
                    "description": "Application name\nSet to official service name in production",
                    "default": "My Web Application",
                    "required": True,
                    "importance": "critical"
                },
                "APP_VERSION": {
                    "description": "Application version",
                    "default": "1.0.0",
                    "required": False,
                    "importance": "important"
                },
                "ENVIRONMENT": {
                    "description": "Runtime environment\nMust be set to production in production",
                    "default": "development",
                    "required": True,
                    "choices": ["development", "staging", "production"],
                    "importance": "critical"
                }
            },
            
            "Security": {
                "SECRET_KEY": {
                    "description": "Application secret key\nUse a strong random string in production",
                    "default": "dev-secret-key-change-in-production",
                    "required": True,
                    "importance": "critical"
                },
                "JWT_SECRET": {
                    "description": "JWT authentication secret key",
                    "default": "jwt-secret-key",
                    "required": True,
                    "importance": "critical"
                },
                "SESSION_TIMEOUT": {
                    "description": "Session timeout in seconds",
                    "default": "3600",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Database": {
                "DATABASE_URL": {
                    "description": "Database connection URL\nExample: postgresql://user:pass@localhost:5432/dbname",
                    "default": "sqlite:///app.db",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "Database connection pool size",
                    "default": "20",
                    "required": False,
                    "importance": "important"
                },
                "DATABASE_TIMEOUT": {
                    "description": "Database connection timeout in seconds",
                    "default": "30",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Performance": {
                "WORKERS": {
                    "description": "Number of worker processes\nAdjust according to CPU cores",
                    "default": "4",
                    "required": False,
                    "choices": ["1", "2", "4", "8", "16"],
                    "importance": "important"
                },
                "MAX_REQUESTS": {
                    "description": "Maximum requests per worker",
                    "default": "1000",
                    "required": False,
                    "importance": "optional"
                }
            },
            
            "Logging": {
                "LOG_LEVEL": {
                    "description": "Log level\nINFO or higher recommended for production",
                    "default": "INFO",
                    "required": False,
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR"],
                    "importance": "optional"
                },
                "LOG_FORMAT": {
                    "description": "Log format",
                    "default": "json",
                    "required": False,
                    "choices": ["text", "json"],
                    "importance": "optional"
                }
            }
        }
    }

@oneenv
def external_services_template():
    """
    External services integration template
    Example of mixing legacy format with Groups format
    """
    return {
        # Direct variable definition (legacy format)
        "EXTERNAL_API_TIMEOUT": {
            "description": "External API call timeout in seconds",
            "default": "10",
            "required": False,
            "group": "External APIs",
            "importance": "important"
        },
        
        # Groups format
        "groups": {
            "Email Service": {
                "SMTP_HOST": {
                    "description": "SMTP server host",
                    "default": "localhost",
                    "required": True,
                    "importance": "important"
                },
                "SMTP_PORT": {
                    "description": "SMTP server port",
                    "default": "587",
                    "required": False,
                    "choices": ["25", "465", "587"],
                    "importance": "important"
                },
                "SMTP_USERNAME": {
                    "description": "SMTP authentication username",
                    "default": "",
                    "required": False,
                    "importance": "important"
                },
                "SMTP_PASSWORD": {
                    "description": "SMTP authentication password",
                    "default": "",
                    "required": False,
                    "importance": "critical"
                }
            },
            
            "File Storage": {
                "STORAGE_TYPE": {
                    "description": "File storage type",
                    "default": "local",
                    "required": False,
                    "choices": ["local", "s3", "gcs"],
                    "importance": "important"
                },
                "STORAGE_BUCKET": {
                    "description": "Storage bucket name (for S3/GCS)",
                    "default": "",
                    "required": False,
                    "importance": "important"
                },
                "STORAGE_REGION": {
                    "description": "Storage region",
                    "default": "us-east-1",
                    "required": False,
                    "importance": "optional"
                }
            },
            
            "Monitoring": {
                "SENTRY_DSN": {
                    "description": "Sentry error tracking DSN",
                    "default": "",
                    "required": False,
                    "importance": "important"
                },
                "HEALTH_CHECK_PATH": {
                    "description": "Health check endpoint",
                    "default": "/health",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    }

# Legacy format example
@oneenv  
def legacy_cache_template():
    """
    Cache configuration (legacy format example)
    """
    return {
        "REDIS_URL": {
            "description": "Redis connection URL\nExample: redis://localhost:6379/0",
            "default": "redis://localhost:6379/0",
            "required": True,
            "group": "Cache",
            "importance": "important"
        },
        "CACHE_DEFAULT_TIMEOUT": {
            "description": "Default cache timeout in seconds",
            "default": "300",
            "required": False,
            "group": "Cache",
            "importance": "optional"
        },
        "CACHE_KEY_PREFIX": {
            "description": "Cache key prefix",
            "default": "myapp:",
            "required": False,
            "group": "Cache",
            "importance": "optional"
        }
    }
```

### Exercise 2: Project-Specific Templates

Templates specialized for specific project types:

```python
# specialized_templates.py
from oneenv import oneenv

@oneenv
def ecommerce_template():
    """
    E-commerce specialized template
    """
    return {
        "groups": {
            "Payment": {
                "STRIPE_PUBLIC_KEY": {
                    "description": "Stripe publishable key",
                    "default": "pk_test_...",
                    "required": True,
                    "importance": "critical"
                },
                "STRIPE_SECRET_KEY": {
                    "description": "Stripe secret key",
                    "default": "sk_test_...",
                    "required": True,
                    "importance": "critical"
                },
                "PAYMENT_CURRENCY": {
                    "description": "Payment currency",
                    "default": "USD",
                    "required": False,
                    "choices": ["USD", "EUR", "JPY"],
                    "importance": "important"
                }
            },
            
            "Inventory": {
                "INVENTORY_ALERT_THRESHOLD": {
                    "description": "Inventory alert threshold",
                    "default": "10",
                    "required": False,
                    "importance": "important"
                },
                "AUTO_REORDER_ENABLED": {
                    "description": "Enable automatic reordering",
                    "default": "False",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            },
            
            "Shipping": {
                "SHIPPING_API_URL": {
                    "description": "Shipping API URL",
                    "default": "https://api.shipping.com/v1",
                    "required": True,
                    "importance": "important"
                },
                "FREE_SHIPPING_THRESHOLD": {
                    "description": "Free shipping amount threshold",
                    "default": "50.00",
                    "required": False,
                    "importance": "important"
                }
            }
        }
    }

@oneenv
def blog_template():
    """
    Blog application specialized template
    """
    return {
        "groups": {
            "Content": {
                "POSTS_PER_PAGE": {
                    "description": "Number of posts per page",
                    "default": "10",
                    "required": False,
                    "choices": ["5", "10", "20", "50"],
                    "importance": "optional"
                },
                "ALLOW_COMMENTS": {
                    "description": "Enable comment functionality",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "important"
                },
                "COMMENT_MODERATION": {
                    "description": "Enable comment moderation",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "important"
                }
            },
            
            "SEO": {
                "SITE_NAME": {
                    "description": "Site name",
                    "default": "My Blog",
                    "required": True,
                    "importance": "critical"
                },
                "SITE_DESCRIPTION": {
                    "description": "Site description",
                    "default": "A technical blog",
                    "required": True,
                    "importance": "important"
                },
                "GOOGLE_ANALYTICS_ID": {
                    "description": "Google Analytics ID",
                    "default": "",
                    "required": False,
                    "importance": "optional"
                }
            },
            
            "Social": {
                "TWITTER_USERNAME": {
                    "description": "Twitter username",
                    "default": "",
                    "required": False,
                    "importance": "optional"
                },
                "FACEBOOK_PAGE_ID": {
                    "description": "Facebook page ID",
                    "default": "",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    }

@oneenv
def api_service_template():
    """
    API service specialized template
    """
    return {
        "groups": {
            "API Configuration": {
                "API_VERSION": {
                    "description": "API version",
                    "default": "v1",
                    "required": True,
                    "importance": "important"
                },
                "API_PREFIX": {
                    "description": "API path prefix",
                    "default": "/api",
                    "required": False,
                    "importance": "important"
                },
                "CORS_ORIGINS": {
                    "description": "CORS allowed origins (comma-separated)",
                    "default": "http://localhost:3000,http://localhost:8080",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Rate Limiting": {
                "RATE_LIMIT_PER_MINUTE": {
                    "description": "Request rate limit per minute",
                    "default": "60",
                    "required": False,
                    "importance": "important"
                },
                "RATE_LIMIT_PER_HOUR": {
                    "description": "Request rate limit per hour",
                    "default": "1000",
                    "required": False,
                    "importance": "important"
                }
            },
            
            "Documentation": {
                "ENABLE_DOCS": {
                    "description": "Enable API documentation",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                },
                "DOCS_URL": {
                    "description": "Documentation URL",
                    "default": "/docs",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    }
```

### Exercise 3: Template Testing and Generation

1. Create a script that incorporates templates (`test_templates.py`):

```python
# Import templates to register them
import project_templates
import specialized_templates

import oneenv

# Generate templates
print("=== Custom Template Testing ===")

# Generate in debug mode
print("Debug mode output:")
print(oneenv.template(debug=True))

print("\n" + "="*50)
print("Generated .env.example:")
print("="*50)
print(oneenv.template())
```

2. Run:
```bash
python test_templates.py
```

### Exercise 4: Conditional Templates

Dynamic templates that change based on environment or configuration:

```python
# conditional_templates.py
from oneenv import oneenv
import os

@oneenv
def conditional_template():
    """
    Template that changes dynamically based on environment
    """
    environment = os.getenv("ENVIRONMENT", "development")
    
    base_template = {
        "groups": {
            "Application": {
                "APP_NAME": {
                    "description": "Application name",
                    "default": "My App",
                    "required": True,
                    "importance": "critical"
                }
            }
        }
    }
    
    # Production-only settings
    if environment == "production":
        base_template["groups"]["Production"] = {
            "SSL_CERT_PATH": {
                "description": "SSL certificate path",
                "default": "/etc/ssl/cert.pem",
                "required": True,
                "importance": "critical"
            },
            "SSL_KEY_PATH": {
                "description": "SSL private key path",
                "default": "/etc/ssl/key.pem",
                "required": True,
                "importance": "critical"
            }
        }
    
    # Development-only settings
    if environment == "development":
        base_template["groups"]["Development"] = {
            "DEBUG_MODE": {
                "description": "Debug mode",
                "default": "True",
                "required": False,
                "choices": ["True", "False"],
                "importance": "optional"
            },
            "HOT_RELOAD": {
                "description": "Hot reload functionality",
                "default": "True",
                "required": False,
                "choices": ["True", "False"],
                "importance": "optional"
            }
        }
    
    return base_template

@oneenv
def feature_flags_template():
    """
    Template including feature flags
    """
    return {
        "groups": {
            "Feature Flags": {
                "FEATURE_NEW_UI": {
                    "description": "Enable new UI feature",
                    "default": "False",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                },
                "FEATURE_BETA_PAYMENT": {
                    "description": "Enable beta payment feature",
                    "default": "False",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                },
                "FEATURE_ANALYTICS": {
                    "description": "Enable detailed analytics",
                    "default": "True",
                    "required": False,
                    "choices": ["True", "False"],
                    "importance": "optional"
                }
            }
        }
    }
```

## Template Design Best Practices

### 1. **Logical Grouping**
```python
# Good example: Group by functionality
"groups": {
    "Database": {...},
    "Cache": {...},
    "Security": {...}
}
```

### 2. **Clear Descriptions**
```python
"description": "Database connection URL\nExample: postgresql://user:pass@localhost:5432/dbname\nUse strong passwords in production"
```

### 3. **Appropriate Default Values**
```python
"default": "development",  # Safe default value
"choices": ["development", "staging", "production"]  # Explicitly show valid choices
```

### 4. **Importance Settings**
```python
"importance": "critical"  # critical/important/optional
```

### 5. **Clear Required Fields**
```python
"required": True  # Clearly mark required fields
```

## Template Reuse

### Creating Common Templates
```python
# common_templates.py
from oneenv import oneenv

@oneenv
def database_template():
    """Reusable database template"""
    return {
        "groups": {
            "Database": {
                # Common database settings
            }
        }
    }
```

### Project-Specific Extensions
```python
# project_specific.py
import common_templates  # Import common templates

@oneenv
def project_specific_template():
    """Project-specific additional settings"""
    return {
        "groups": {
            "Project Specific": {
                # Project-specific settings
            }
        }
    }
```

## Next Steps

You've learned how to create custom templates. Next, let's learn about production best practices.

**→ [Step 6: Production Best Practices](06-production-tips.md)**

## Frequently Asked Questions

### Q: Should I use Groups format or legacy format?
A: We recommend the Groups format for new projects. It's easier to group related variables and improves readability.

### Q: Can I split templates across multiple files?
A: Yes. You can define templates in multiple Python files and import each of them.

### Q: How can I dynamically change templates?
A: You can check environment variables or other conditions within the template function and dynamically build the dictionary.

### Q: What if my template settings aren't being applied?
A: Use `oneenv template -d` debug mode to verify that your templates are being discovered correctly.