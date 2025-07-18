# Tutorial 11: Practical Guide for Package Developers

**Time:** 15-20 minutes  
**Target:** Package developers, tool creators  
**Prerequisites:** Previous tutorials, real-world project experience

## Overview

Learn how to apply OneEnv templates and scaffolding tools in real-world scenarios. This tutorial covers practical examples from RAG systems to web frameworks, with insights on testing, CI/CD integration, and community distribution.

## What You'll Learn

- Real-world RAG system implementation
- Multi-package coordination strategies
- Testing and CI/CD integration
- Community distribution best practices
- Advanced troubleshooting techniques

## 1. RAG System Implementation (8 minutes)

### Complete RAG Stack Template

Let's create a comprehensive template for a RAG (Retrieval-Augmented Generation) system:

```python
# rag_package/templates.py
def rag_system_template():
    """Complete RAG system environment template"""
    return [
        # Database - Vector storage and metadata
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL connection for document metadata and user data",
                    "default": "postgresql://user:pass@localhost:5432/rag_db",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "Connection pool size for high-throughput operations",
                    "default": "20",
                    "required": False,
                    "importance": "important"
                },
                "DATABASE_TIMEOUT": {
                    "description": "Query timeout in seconds",
                    "default": "30",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # Vector Database - Embeddings storage
        {
            "category": "VectorStore",
            "option": "chroma",
            "env": {
                "CHROMA_HOST": {
                    "description": "Chroma vector database host",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "CHROMA_PORT": {
                    "description": "Chroma server port",
                    "default": "8000",
                    "required": False,
                    "importance": "important"
                },
                "CHROMA_COLLECTION": {
                    "description": "Default collection for document embeddings",
                    "default": "rag_documents",
                    "required": False,
                    "importance": "important"
                },
                "CHROMA_PERSIST_DIRECTORY": {
                    "description": "Directory for persistent storage",
                    "default": "./chroma_db",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # Alternative vector store
        {
            "category": "VectorStore",
            "option": "pinecone",
            "env": {
                "PINECONE_API_KEY": {
                    "description": "Pinecone API key for cloud vector storage",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "PINECONE_ENVIRONMENT": {
                    "description": "Pinecone environment (e.g., us-west1-gcp)",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "PINECONE_INDEX": {
                    "description": "Pinecone index name for embeddings",
                    "default": "rag-index",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        
        # LLM Provider
        {
            "category": "LLM",
            "option": "openai",
            "env": {
                "OPENAI_API_KEY": {
                    "description": "OpenAI API key for text generation",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "OPENAI_MODEL": {
                    "description": "Primary model for text generation",
                    "default": "gpt-4",
                    "required": False,
                    "importance": "important",
                    "choices": ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
                },
                "OPENAI_EMBEDDING_MODEL": {
                    "description": "Model for generating embeddings",
                    "default": "text-embedding-ada-002",
                    "required": False,
                    "importance": "important"
                },
                "OPENAI_MAX_TOKENS": {
                    "description": "Maximum tokens per response",
                    "default": "1000",
                    "required": False,
                    "importance": "optional"
                },
                "OPENAI_TEMPERATURE": {
                    "description": "Response creativity (0.0-1.0)",
                    "default": "0.7",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # Alternative LLM
        {
            "category": "LLM",
            "option": "anthropic",
            "env": {
                "ANTHROPIC_API_KEY": {
                    "description": "Anthropic API key for Claude models",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "ANTHROPIC_MODEL": {
                    "description": "Claude model version",
                    "default": "claude-3-sonnet-20240229",
                    "required": False,
                    "importance": "important",
                    "choices": ["claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
                }
            }
        },
        
        # Cache for performance
        {
            "category": "Cache",
            "option": "redis",
            "env": {
                "REDIS_URL": {
                    "description": "Redis cache for embeddings and responses",
                    "default": "redis://localhost:6379/0",
                    "required": False,
                    "importance": "important"
                },
                "REDIS_TTL": {
                    "description": "Cache TTL in seconds",
                    "default": "3600",
                    "required": False,
                    "importance": "optional"
                },
                "REDIS_MAX_CONNECTIONS": {
                    "description": "Maximum Redis connections",
                    "default": "10",
                    "required": False,
                    "importance": "optional"
                }
            }
        },
        
        # Monitoring and observability
        {
            "category": "Monitoring",
            "option": "basic",
            "env": {
                "LOG_LEVEL": {
                    "description": "Application logging level",
                    "default": "INFO",
                    "required": False,
                    "importance": "important",
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                },
                "METRICS_ENABLED": {
                    "description": "Enable performance metrics collection",
                    "default": "true",
                    "required": False,
                    "importance": "optional",
                    "choices": ["true", "false"]
                },
                "TRACE_QUERIES": {
                    "description": "Enable query tracing for debugging",
                    "default": "false",
                    "required": False,
                    "importance": "optional",
                    "choices": ["true", "false"]
                }
            }
        }
    ]
```

### RAG System Scaffolding Tool

Create a specialized tool for RAG system setup:

```python
# rag_package/rag_scaffold.py
import oneenv
import sys
from typing import Dict, List

class RAGSystemScaffold:
    def __init__(self):
        self.selections = []
        self.vector_store = None
        self.llm_provider = None
        self.use_cache = False
        
    def welcome(self):
        """Display RAG system setup welcome"""
        print("🤖 RAG System Environment Setup")
        print("=" * 40)
        print("This wizard will configure your Retrieval-Augmented Generation system.")
        print("We'll set up vector storage, LLM provider, and optional components.\n")
    
    def select_vector_store(self):
        """Choose vector storage solution"""
        print("🔍 Vector Store Selection")
        print("Choose your vector database for embeddings storage:")
        
        if not oneenv.has_category("VectorStore"):
            print("❌ No vector store templates found!")
            return False
        
        options = oneenv.get_options("VectorStore")
        
        print("\nAvailable options:")
        for i, option in enumerate(options, 1):
            description = {
                "chroma": "Local/self-hosted, good for development",
                "pinecone": "Cloud-hosted, production-ready, requires API key",
                "weaviate": "Open-source, GraphQL API",
                "qdrant": "High-performance, written in Rust"
            }.get(option, "Vector database option")
            
            print(f"  {i}. {option} - {description}")
        
        while True:
            try:
                choice = int(input(f"\nSelect vector store (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    self.vector_store = options[choice - 1]
                    self.selections.append({
                        "category": "VectorStore",
                        "option": self.vector_store
                    })
                    print(f"✅ Selected: {self.vector_store}")
                    return True
                else:
                    print(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("Please enter a valid number")
    
    def select_llm_provider(self):
        """Choose LLM provider"""
        print("\n🧠 LLM Provider Selection")
        print("Choose your language model provider:")
        
        if not oneenv.has_category("LLM"):
            print("❌ No LLM templates found!")
            return False
        
        options = oneenv.get_options("LLM")
        
        print("\nAvailable options:")
        for i, option in enumerate(options, 1):
            description = {
                "openai": "GPT models, most popular, requires API key",
                "anthropic": "Claude models, good reasoning, requires API key",
                "local": "Local models via Ollama/LMStudio, no API key needed",
                "azure": "Azure OpenAI, enterprise features"
            }.get(option, "LLM provider option")
            
            print(f"  {i}. {option} - {description}")
        
        while True:
            try:
                choice = int(input(f"\nSelect LLM provider (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    self.llm_provider = options[choice - 1]
                    self.selections.append({
                        "category": "LLM",
                        "option": self.llm_provider
                    })
                    print(f"✅ Selected: {self.llm_provider}")
                    return True
                else:
                    print(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("Please enter a valid number")
    
    def select_optional_components(self):
        """Choose optional components"""
        print("\n⚡ Optional Components")
        
        # Database
        if oneenv.has_category("Database"):
            use_db = input("Add database for metadata storage? (y/n): ").lower().startswith('y')
            if use_db:
                db_options = oneenv.get_options("Database")
                if "postgres" in db_options:
                    self.selections.append({
                        "category": "Database",
                        "option": "postgres"
                    })
                    print("✅ Added PostgreSQL for metadata")
        
        # Cache
        if oneenv.has_category("Cache"):
            use_cache = input("Add Redis cache for performance? (y/n): ").lower().startswith('y')
            if use_cache:
                self.use_cache = True
                cache_options = oneenv.get_options("Cache")
                if "redis" in cache_options:
                    self.selections.append({
                        "category": "Cache",
                        "option": "redis"
                    })
                    print("✅ Added Redis cache")
        
        # Monitoring
        if oneenv.has_category("Monitoring"):
            use_monitoring = input("Add monitoring and logging? (y/n): ").lower().startswith('y')
            if use_monitoring:
                monitoring_options = oneenv.get_options("Monitoring")
                if "basic" in monitoring_options:
                    self.selections.append({
                        "category": "Monitoring",
                        "option": "basic"
                    })
                    print("✅ Added basic monitoring")
    
    def show_summary(self):
        """Display configuration summary"""
        print("\n📋 RAG System Configuration Summary")
        print("=" * 40)
        
        for selection in self.selections:
            print(f"• {selection['category']}: {selection['option']}")
        
        print(f"\n🎯 Your RAG system will use:")
        print(f"  - Vector Store: {self.vector_store}")
        print(f"  - LLM Provider: {self.llm_provider}")
        if self.use_cache:
            print(f"  - Caching: Enabled")
        
        print(f"\n💡 Next steps after generation:")
        if self.llm_provider in ["openai", "anthropic"]:
            print(f"  1. Set your {self.llm_provider.upper()}_API_KEY")
        if self.vector_store == "pinecone":
            print(f"  2. Set your PINECONE_API_KEY and PINECONE_ENVIRONMENT")
        print(f"  3. Review and customize other settings")
        print(f"  4. Copy .env.example to .env")
    
    def generate_config(self):
        """Generate the final configuration"""
        if not self.selections:
            print("❌ No components selected!")
            return False
        
        try:
            filename = input("\nOutput file (default: .env.rag): ").strip() or ".env.rag"
            oneenv.generate_template(filename, self.selections)
            print(f"\n🎉 Generated RAG system configuration: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error generating configuration: {e}")
            return False
    
    def run(self):
        """Run the RAG scaffolding wizard"""
        self.welcome()
        
        if not self.select_vector_store():
            return
        
        if not self.select_llm_provider():
            return
        
        self.select_optional_components()
        self.show_summary()
        
        confirm = input("\n✅ Generate this configuration? (y/n): ").lower().startswith('y')
        if confirm:
            self.generate_config()
        else:
            print("Configuration cancelled.")

if __name__ == "__main__":
    scaffold = RAGSystemScaffold()
    scaffold.run()
```

## 2. Web Framework Integration (7 minutes)

### Django/FastAPI Template

```python
# web_framework/templates.py
def web_framework_template():
    """Web framework environment template"""
    return [
        # Database options
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "Primary database connection",
                    "default": "postgresql://user:pass@localhost:5432/webapp",
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
        
        # Web server configuration
        {
            "category": "WebServer",
            "option": "fastapi",
            "env": {
                "WEB_HOST": {
                    "description": "Server host address",
                    "default": "0.0.0.0",
                    "required": False,
                    "importance": "important"
                },
                "WEB_PORT": {
                    "description": "Server port",
                    "default": "8000",
                    "required": False,
                    "importance": "important"
                },
                "WEB_WORKERS": {
                    "description": "Number of worker processes",
                    "default": "4",
                    "required": False,
                    "importance": "optional"
                },
                "WEB_RELOAD": {
                    "description": "Enable auto-reload in development",
                    "default": "false",
                    "required": False,
                    "importance": "optional",
                    "choices": ["true", "false"]
                }
            }
        },
        
        # Authentication
        {
            "category": "Auth",
            "option": "jwt",
            "env": {
                "JWT_SECRET_KEY": {
                    "description": "Secret key for JWT token signing",
                    "default": "",
                    "required": True,
                    "importance": "critical"
                },
                "JWT_EXPIRATION": {
                    "description": "Token expiration time in seconds",
                    "default": "3600",
                    "required": False,
                    "importance": "important"
                },
                "JWT_ALGORITHM": {
                    "description": "JWT signing algorithm",
                    "default": "HS256",
                    "required": False,
                    "importance": "optional",
                    "choices": ["HS256", "RS256", "ES256"]
                }
            }
        }
    ]
```

## 3. Testing and CI/CD Integration (3 minutes)

### Test Configuration

```python
# tests/test_templates.py
import pytest
import oneenv
from oneenv.models import validate_scaffolding_format

def test_rag_template_validation():
    """Test that RAG templates are valid"""
    from rag_package.templates import rag_system_template
    
    template_data = rag_system_template()
    
    # Should not raise any validation errors
    validate_scaffolding_format(template_data)
    
    # Check required categories are present
    categories = {item["category"] for item in template_data}
    assert "VectorStore" in categories
    assert "LLM" in categories

def test_template_generation():
    """Test template generation with selections"""
    selections = [
        {"category": "VectorStore", "option": "chroma"},
        {"category": "LLM", "option": "openai"}
    ]
    
    # Should generate without errors
    content = oneenv.generate_template("test.env", selections)
    assert content
    assert "CHROMA_HOST" in content
    assert "OPENAI_API_KEY" in content

def test_api_functions():
    """Test OneEnv API functions work correctly"""
    # Test structure retrieval
    structure = oneenv.get_all_template_structure()
    assert isinstance(structure, dict)
    
    # Test category checking
    if "VectorStore" in structure:
        assert oneenv.has_category("VectorStore")
        options = oneenv.get_options("VectorStore")
        assert isinstance(options, list)
        assert len(options) > 0

@pytest.mark.parametrize("category,expected_options", [
    ("VectorStore", ["chroma", "pinecone"]),
    ("LLM", ["openai", "anthropic"]),
])
def test_expected_options(category, expected_options):
    """Test that expected options are available"""
    if oneenv.has_category(category):
        actual_options = oneenv.get_options(category)
        for expected in expected_options:
            assert expected in actual_options, f"{expected} not found in {category}"
```

### GitHub Actions Workflow

```yaml
# .github/workflows/test-templates.yml
name: Test OneEnv Templates

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-templates:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install oneenv pytest
        pip install -e .
    
    - name: Test template validation
      run: |
        pytest tests/test_templates.py -v
    
    - name: Test scaffolding tools
      run: |
        # Test that scaffolding tools can be imported and run
        python -c "from rag_package.rag_scaffold import RAGSystemScaffold; print('Import successful')"
    
    - name: Generate sample configurations
      run: |
        # Test template generation
        python -c "
        import oneenv
        selections = [
            {'category': 'VectorStore', 'option': 'chroma'},
            {'category': 'LLM', 'option': 'openai'}
        ]
        content = oneenv.generate_template('.env.test', selections)
        print('Generated test configuration successfully')
        "
```

## 4. Community Distribution (2 minutes)

### Package Structure

```
my_rag_package/
├── pyproject.toml
├── README.md
├── src/
│   └── my_rag_package/
│       ├── __init__.py
│       ├── templates.py
│       └── scaffold.py
├── tests/
│   ├── test_templates.py
│   └── test_scaffold.py
├── examples/
│   ├── basic_setup.py
│   └── advanced_setup.py
└── docs/
    └── configuration.md
```

### pyproject.toml for Distribution

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-rag-package"
version = "0.1.0"
description = "RAG system with OneEnv templates"
authors = [{name = "Your Name", email = "you@example.com"}]
dependencies = [
    "oneenv>=0.3.0",
    "pydantic>=2.0",
]
keywords = ["rag", "environment", "configuration", "templates"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

[project.optional-dependencies]
dev = ["pytest", "black", "isort", "mypy"]

[project.urls]
Homepage = "https://github.com/yourusername/my-rag-package"
Documentation = "https://my-rag-package.readthedocs.io"
Repository = "https://github.com/yourusername/my-rag-package"
Issues = "https://github.com/yourusername/my-rag-package/issues"

[project.scripts]
rag-setup = "my_rag_package.scaffold:main"

# OneEnv template registration
[project.entry-points."oneenv.templates"]
rag = "my_rag_package.templates:rag_system_template"
web = "my_rag_package.templates:web_framework_template"

[tool.hatch.build.targets.wheel]
packages = ["src/my_rag_package"]
```

### Distribution README

```markdown
# My RAG Package

A complete RAG (Retrieval-Augmented Generation) system with OneEnv integration for easy environment configuration.

## Quick Start

1. Install the package:
   ```bash
   pip install my-rag-package
   ```

2. Run the setup wizard:
   ```bash
   rag-setup
   ```

3. Or use OneEnv directly:
   ```bash
   oneenv template --info VectorStore
   oneenv template --preview LLM openai
   ```

## Templates Included

- **VectorStore**: Chroma, Pinecone, Weaviate
- **LLM**: OpenAI, Anthropic, Local models
- **Database**: PostgreSQL, SQLite
- **Cache**: Redis, Memcached
- **Monitoring**: Basic logging and metrics

## Contributing

See our [contribution guide](CONTRIBUTING.md) for details on adding new templates or improving existing ones.
```

## Best Practices Summary

### 🏗️ Template Design
- **Logical grouping**: Organize by technology categories
- **Clear naming**: Use descriptive category and option names
- **Comprehensive defaults**: Provide sensible default values
- **Importance levels**: Mark critical vs optional settings

### 🧪 Testing Strategy
- **Validation tests**: Ensure templates pass schema validation
- **Integration tests**: Test with actual OneEnv API
- **CI/CD automation**: Run tests on multiple Python versions
- **Example verification**: Ensure examples work as documented

### 📦 Distribution
- **Clear documentation**: Explain what each template does
- **Entry-points registration**: Make templates auto-discoverable
- **Semantic versioning**: Use proper version management
- **Community engagement**: Provide issue templates and contribution guides

### 🔧 Tooling
- **Custom scaffolds**: Create domain-specific setup wizards
- **Configuration validation**: Validate user inputs thoroughly
- **Error handling**: Provide helpful error messages
- **User experience**: Make tools intuitive and informative

## Next Steps

1. **Apply to Your Project**: Use these patterns in your own packages
2. **Community Contribution**: Share useful templates with the community
3. **Advanced Integration**: Explore CI/CD and deployment automation
4. **Monitoring**: Add observability to your templates and tools

---

**🎉 Congratulations!** You now have the knowledge to create, test, and distribute professional-grade OneEnv templates and scaffolding tools. Your packages can now provide excellent developer experience right out of the box!