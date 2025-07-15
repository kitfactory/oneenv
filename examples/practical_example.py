#!/usr/bin/env python3
"""
Practical example of OneEnv named environments.
This example shows how to use named environments in a real application scenario.
"""

import oneenv
import os

def setup_application_environments():
    """
    Setup application environments for different services.
    """
    print("=== 実際のアプリケーションでの使用例 ===")
    print()
    
    # 共通設定を読み込み
    print("1. 共通設定を読み込み")
    oneenv.env().load_dotenv("examples/env_files/common.env")
    print("   oneenv.env().load_dotenv('common.env')")
    print()
    
    # サービス別の設定を読み込み
    print("2. サービス別の設定を読み込み")
    oneenv.env("database").load_dotenv("examples/env_files/database.env")
    oneenv.env("web").load_dotenv("examples/env_files/web.env")
    oneenv.env("api").load_dotenv("examples/env_files/api.env")
    print("   oneenv.env('database').load_dotenv('database.env')")
    print("   oneenv.env('web').load_dotenv('web.env')")
    print("   oneenv.env('api').load_dotenv('api.env')")
    print()

def get_database_config():
    """
    Get database configuration using named environment.
    """
    print("=== データベース設定の取得 ===")
    db_env = oneenv.env("database")
    
    config = {
        "host": db_env.get("DATABASE_HOST", "localhost"),
        "port": int(db_env.get("DATABASE_PORT", "5432")),
        "name": db_env.get("DATABASE_NAME", "myapp"),
        "user": db_env.get("DATABASE_USER", "user"),
        "password": db_env.get("DATABASE_PASSWORD", "password"),
        "timeout": int(db_env.get("TIMEOUT", "30"))  # 共通設定からフォールバック
    }
    
    print(f"Database config: {config}")
    return config

def get_web_config():
    """
    Get web server configuration using named environment.
    """
    print("=== Webサーバー設定の取得 ===")
    web_env = oneenv.env("web")
    
    config = {
        "host": web_env.get("WEB_HOST", "0.0.0.0"),
        "port": int(web_env.get("WEB_PORT", "8000")),
        "debug": web_env.get("WEB_DEBUG", "false").lower() == "true",
        "log_level": web_env.get("LOG_LEVEL", "INFO"),  # 共通設定からフォールバック
        "static_dir": web_env.get("STATIC_DIR", "/static")
    }
    
    print(f"Web config: {config}")
    return config

def get_api_config():
    """
    Get API configuration using named environment.
    """
    print("=== API設定の取得 ===")
    api_env = oneenv.env("api")
    
    config = {
        "host": api_env.get("API_HOST", "localhost"),
        "port": int(api_env.get("API_PORT", "8080")),
        "key": api_env.get("API_KEY", "default-key"),
        "timeout": int(api_env.get("TIMEOUT", "30")),  # 共通設定からフォールバック
        "rate_limit": int(api_env.get("RATE_LIMIT", "100"))
    }
    
    print(f"API config: {config}")
    return config

def create_sample_env_files():
    """
    Create sample environment files for the practical example.
    """
    os.makedirs("examples/env_files", exist_ok=True)
    
    # Database environment file
    with open("examples/env_files/database.env", "w") as f:
        f.write("# データベース設定\n")
        f.write("DATABASE_HOST=db.example.com\n")
        f.write("DATABASE_PORT=5432\n")
        f.write("DATABASE_NAME=production_db\n")
        f.write("DATABASE_USER=db_user\n")
        f.write("DATABASE_PASSWORD=db_secret\n")
    
    # Web environment file
    with open("examples/env_files/web.env", "w") as f:
        f.write("# Webサーバー設定\n")
        f.write("WEB_HOST=0.0.0.0\n")
        f.write("WEB_PORT=8000\n")
        f.write("WEB_DEBUG=false\n")
        f.write("STATIC_DIR=/var/www/static\n")
    
    # API environment file
    with open("examples/env_files/api.env", "w") as f:
        f.write("# API設定\n")
        f.write("API_HOST=api.example.com\n")
        f.write("API_PORT=8080\n")
        f.write("API_KEY=prod_api_key_123\n")
        f.write("RATE_LIMIT=1000\n")

def main():
    """
    Main function demonstrating practical usage.
    """
    # Create sample environment files
    create_sample_env_files()
    
    # Setup environments
    setup_application_environments()
    
    # Get configurations for different services
    db_config = get_database_config()
    print()
    
    web_config = get_web_config()
    print()
    
    api_config = get_api_config()
    print()
    
    # Show fallback behavior
    print("=== フォールバック動作の確認 ===")
    print("全ての環境で共通設定のTIMEOUTが使用されています:")
    print(f"  database timeout: {oneenv.env('database').get('TIMEOUT')}")
    print(f"  web timeout: {oneenv.env('web').get('TIMEOUT')}")
    print(f"  api timeout: {oneenv.env('api').get('TIMEOUT')}")
    print()
    
    # Show priority
    print("=== 優先順位の確認 ===")
    print("LOG_LEVELの取得:")
    print(f"  共通環境: {oneenv.env().get('LOG_LEVEL')}")
    print(f"  web環境: {oneenv.env('web').get('LOG_LEVEL')} (共通から継承)")
    print(f"  database環境: {oneenv.env('database').get('LOG_LEVEL')} (共通から継承)")

if __name__ == "__main__":
    main()