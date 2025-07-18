#!/usr/bin/env python3
"""
Tutorial Examples: Basic Templates
チュートリアル用の基本的なテンプレート例
"""

def database_template():
    """Tutorial 9: Database template example"""
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

def cache_template():
    """Tutorial examples: Cache template"""
    return [
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
        {
            "category": "Cache",
            "option": "memcached",
            "env": {
                "MEMCACHED_SERVERS": {
                    "description": "Memcached server addresses",
                    "default": "127.0.0.1:11211",
                    "required": False,
                    "importance": "important"
                },
                "MEMCACHED_TIMEOUT": {
                    "description": "Connection timeout in seconds",
                    "default": "60",
                    "required": False,
                    "importance": "optional"
                }
            }
        }
    ]

def rag_system_template():
    """Tutorial 11: RAG system template example"""
    return [
        # Database
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL connection for document metadata",
                    "default": "postgresql://user:pass@localhost:5432/rag_db",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        # Vector Store
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
                }
            }
        },
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
        # LLM
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
                }
            }
        },
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
        }
    ]

if __name__ == "__main__":
    # テンプレートの検証
    from oneenv.models import validate_scaffolding_format
    
    templates = [
        ("database_template", database_template()),
        ("cache_template", cache_template()),
        ("rag_system_template", rag_system_template())
    ]
    
    for name, template_data in templates:
        try:
            validate_scaffolding_format(template_data)
            print(f"✅ {name}: 検証成功")
        except Exception as e:
            print(f"❌ {name}: 検証失敗 - {e}")
    
    # 構造情報の表示
    print("\n📊 テンプレート構造:")
    for name, template_data in templates:
        categories = {}
        for item in template_data:
            category = item["category"]
            option = item["option"]
            if category not in categories:
                categories[category] = []
            categories[category].append(option)
        
        print(f"{name}: {categories}")