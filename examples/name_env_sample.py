#!/usr/bin/env python3
"""
Named environment sample for OneEnv.
This example demonstrates the exact usage pattern from docs/name_env.md.
"""

import oneenv

def main():
    """
    Demonstrates the named environment functionality as described in docs/name_env.md.
    """
    
    print("=== OneEnv Named Environment Sample ===")
    print()
    
    # 使用例（docs/name_env.mdから）
    print("Loading environment files:")
    print("oneenv.env().load_dotenv('common.env')")
    print("oneenv.env('X').load_dotenv('X.env')")
    print("oneenv.env('Y').load_dotenv('Y.env')")
    print()
    
    # Load environment files
    oneenv.env().load_dotenv("examples/env_files/common.env")
    oneenv.env("X").load_dotenv("examples/env_files/X.env")
    oneenv.env("Y").load_dotenv("examples/env_files/Y.env")
    
    # 共通から取得
    print("=== 共通から取得 ===")
    timeout = oneenv.env().get("TIMEOUT", "30")
    print(f"oneenv.env().get('TIMEOUT', '30') = {timeout}")
    
    common_var = oneenv.env().get("COMMON_VAR", "default")
    print(f"oneenv.env().get('COMMON_VAR', 'default') = {common_var}")
    print()
    
    # 名前付き環境で取得（個別が優先、なければ共通から）
    print("=== 名前付き環境で取得（個別が優先、なければ共通から） ===")
    
    # X環境の例
    print("--- X環境 ---")
    x_api_key = oneenv.env("X").get("API_KEY", "default-x")
    print(f"oneenv.env('X').get('API_KEY', 'default-x') = {x_api_key}")
    
    # X環境でTIMEOUTを取得（共通からフォールバック）
    x_timeout = oneenv.env("X").get("TIMEOUT", "30")
    print(f"oneenv.env('X').get('TIMEOUT', '30') = {x_timeout} (共通からフォールバック)")
    
    # X環境でCOMMON_VARを取得（共通からフォールバック）
    x_common_var = oneenv.env("X").get("COMMON_VAR", "default")
    print(f"oneenv.env('X').get('COMMON_VAR', 'default') = {x_common_var} (共通からフォールバック)")
    print()
    
    # Y環境の例
    print("--- Y環境 ---")
    y_api_key = oneenv.env("Y").get("API_KEY", "default-y")
    print(f"oneenv.env('Y').get('API_KEY', 'default-y') = {y_api_key}")
    
    # Y環境でTIMEOUTを取得（共通からフォールバック）
    y_timeout = oneenv.env("Y").get("TIMEOUT", "30")
    print(f"oneenv.env('Y').get('TIMEOUT', '30') = {y_timeout} (共通からフォールバック)")
    
    # Y環境でCOMMON_VARを取得（共通からフォールバック）
    y_common_var = oneenv.env("Y").get("COMMON_VAR", "default")
    print(f"oneenv.env('Y').get('COMMON_VAR', 'default') = {y_common_var} (共通からフォールバック)")
    print()
    
    # 存在しないキーの例
    print("=== 存在しないキーの例 ===")
    nonexistent = oneenv.env("X").get("NONEXISTENT_VAR", "fallback_value")
    print(f"oneenv.env('X').get('NONEXISTENT_VAR', 'fallback_value') = {nonexistent}")
    print()
    
    # 優先順位の確認
    print("=== 優先順位の確認 ===")
    print("X環境:")
    print(f"  SERVICE_NAME (X固有): {oneenv.env('X').get('SERVICE_NAME', 'なし')}")
    print(f"  TIMEOUT (共通から): {oneenv.env('X').get('TIMEOUT', 'なし')}")
    print(f"  COMMON_VAR (共通から): {oneenv.env('X').get('COMMON_VAR', 'なし')}")
    print()
    
    print("Y環境:")
    print(f"  SERVICE_NAME (Y固有): {oneenv.env('Y').get('SERVICE_NAME', 'なし')}")
    print(f"  TIMEOUT (共通から): {oneenv.env('Y').get('TIMEOUT', 'なし')}")
    print(f"  COMMON_VAR (共通から): {oneenv.env('Y').get('COMMON_VAR', 'なし')}")


if __name__ == "__main__":
    main()