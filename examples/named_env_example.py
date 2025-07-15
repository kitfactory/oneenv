#!/usr/bin/env python3
"""
Named environment example for OneEnv.
This demonstrates the new named environment functionality.
"""

import oneenv

# Example usage as documented in docs/name_env.md
def example_usage():
    """
    Demonstrates the named environment functionality with examples.
    """
    
    # Load environments from different files
    oneenv.env().load_dotenv("examples/env_files/common.env")
    oneenv.env("X").load_dotenv("examples/env_files/X.env")
    oneenv.env("Y").load_dotenv("examples/env_files/Y.env")
    
    # Get values from common environment
    timeout = oneenv.env().get("TIMEOUT", "30")
    print(f"Common timeout: {timeout}")
    
    # Get values from named environments (with fallback to common)
    x_api_key = oneenv.env("X").get("API_KEY", "default-x")
    y_api_key = oneenv.env("Y").get("API_KEY", "default-y")
    
    print(f"X API Key: {x_api_key}")
    print(f"Y API Key: {y_api_key}")
    
    # Named environments fall back to common environment
    x_timeout = oneenv.env("X").get("TIMEOUT", "30")
    y_timeout = oneenv.env("Y").get("TIMEOUT", "30")
    
    print(f"X timeout (from common): {x_timeout}")
    print(f"Y timeout (from common): {y_timeout}")


if __name__ == "__main__":
    import os
    
    # Create example env files directory
    env_dir = "examples/env_files"
    os.makedirs(env_dir, exist_ok=True)
    
    # Create example .env files
    with open(f"{env_dir}/common.env", "w") as f:
        f.write("TIMEOUT=30\n")
        f.write("COMMON_VAR=shared_value\n")
    
    with open(f"{env_dir}/X.env", "w") as f:
        f.write("API_KEY=x_secret_key\n")
        f.write("SERVICE_NAME=service_x\n")
    
    with open(f"{env_dir}/Y.env", "w") as f:
        f.write("API_KEY=y_secret_key\n")
        f.write("SERVICE_NAME=service_y\n")
    
    print("=== Named Environment Example ===")
    example_usage()
    
    print("\n=== Demonstrating fallback behavior ===")
    # Show fallback behavior
    print(f"X service name: {oneenv.env('X').get('SERVICE_NAME')}")
    print(f"X common var (fallback): {oneenv.env('X').get('COMMON_VAR')}")
    print(f"X nonexistent var: {oneenv.env('X').get('NONEXISTENT', 'default')}")