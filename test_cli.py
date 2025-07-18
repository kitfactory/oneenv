#!/usr/bin/env python3
"""
CLI機能テスト用スクリプト
"""

import sys
import os

# パスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from oneenv.core import _scaffolding_processor
from oneenv.models import EnvOption, EnvVarConfig

def setup_mock_data():
    """モックデータを設定"""
    mock_options = [
        EnvOption(
            category="Database",
            option="postgres",
            env={
                "DATABASE_URL": EnvVarConfig(
                    description="PostgreSQL connection URL",
                    default="postgresql://user:pass@localhost:5432/dbname",
                    required=True,
                    importance="critical"
                ),
                "DATABASE_POOL_SIZE": EnvVarConfig(
                    description="Connection pool size",
                    default="10",
                    required=False,
                    importance="optional"
                )
            }
        ),
        EnvOption(
            category="Database",
            option="sqlite",
            env={
                "DATABASE_URL": EnvVarConfig(
                    description="SQLite database URL",
                    default="sqlite:///app.db",
                    required=True,
                    importance="critical"
                )
            }
        ),
        EnvOption(
            category="VectorStore",
            option="chroma",
            env={
                "CHROMA_HOST": EnvVarConfig(
                    description="Chroma host",
                    default="localhost",
                    required=True,
                    importance="important"
                ),
                "CHROMA_PORT": EnvVarConfig(
                    description="Chroma port",
                    default="8000",
                    required=False,
                    importance="optional"
                )
            }
        )
    ]
    
    _scaffolding_processor.env_options = mock_options
    print("✅ Mock data loaded successfully")
    print(f"   - {len(mock_options)} options available")
    print(f"   - Categories: {list(_scaffolding_processor.get_template_structure().keys())}")

if __name__ == "__main__":
    setup_mock_data()
    
    # CLIのインポートと実行
    from oneenv.cli import main
    
    print("\n🚀 Testing CLI functionality with mock data...")
    print("=" * 50)
    
    # sys.argvを一時的に変更してCLIをテスト
    original_argv = sys.argv
    
    try:
        print("\n1. Testing --structure:")
        sys.argv = ["oneenv", "template", "--structure"]
        main()
        
        print("\n2. Testing --structure --json:")
        sys.argv = ["oneenv", "template", "--structure", "--json"]
        main()
        
        print("\n3. Testing --info Database:")
        sys.argv = ["oneenv", "template", "--info", "Database"]
        main()
        
        print("\n4. Testing --preview Database postgres:")
        sys.argv = ["oneenv", "template", "--preview", "Database", "postgres"]
        main()
        
    except SystemExit:
        pass  # CLIが正常終了した場合
    finally:
        sys.argv = original_argv