"""
Test scaffolding template for verifying the generate command
"""

def database_template():
    """Database configuration template"""
    return [
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "POSTGRES_HOST": {
                    "description": "PostgreSQL server host",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "POSTGRES_PORT": {
                    "description": "PostgreSQL server port",
                    "default": "5432",
                    "required": False,
                    "importance": "important",
                    "choices": ["5432", "5433", "5434"]
                },
                "POSTGRES_DB": {
                    "description": "Database name",
                    "default": "myapp",
                    "required": True,
                    "importance": "critical"
                }
            }
        },
        {
            "category": "Database",
            "option": "mysql",
            "env": {
                "MYSQL_HOST": {
                    "description": "MySQL server host",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "MYSQL_PORT": {
                    "description": "MySQL server port",
                    "default": "3306",
                    "required": False,
                    "importance": "important"
                }
            }
        }
    ]

def vectorstore_template():
    """Vector store configuration template"""
    return [
        {
            "category": "VectorStore",
            "option": "chroma",
            "env": {
                "CHROMA_HOST": {
                    "description": "Chroma server host",
                    "default": "localhost",
                    "required": True,
                    "importance": "critical"
                },
                "CHROMA_PORT": {
                    "description": "Chroma server port",
                    "default": "8000",
                    "required": False,
                    "importance": "important"
                }
            }
        }
    ]