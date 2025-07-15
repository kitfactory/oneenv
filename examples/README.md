# OneEnv Examples

This directory contains examples demonstrating OneEnv functionality.

## Named Environment Examples

### Basic Usage (`name_env_sample.py`)

Demonstrates the basic named environment functionality as described in `docs/name_env.md`:

```python
# Load environment files
oneenv.env().load_dotenv("common.env")
oneenv.env("X").load_dotenv("X.env")
oneenv.env("Y").load_dotenv("Y.env")

# Get values from common environment
oneenv.env().get("TIMEOUT", "30")

# Get values from named environments (with fallback to common)
oneenv.env("X").get("API_KEY", "default-x")
```

**Run:**
```bash
python examples/name_env_sample.py
```

### Practical Application Example (`practical_example.py`)

Shows how to use named environments in a real application with multiple services:

- Database configuration
- Web server configuration  
- API configuration
- Fallback to common settings

**Run:**
```bash
python examples/practical_example.py
```

### Advanced Usage (`named_env_example.py`)

More detailed example showing:
- Multiple environment loading
- Fallback behavior
- Override functionality

**Run:**
```bash
python examples/named_env_example.py
```

## Environment Files

The `env_files/` directory contains sample environment files:

- `common.env` - Shared configuration
- `X.env` - X environment specific settings
- `Y.env` - Y environment specific settings
- `database.env` - Database service configuration
- `web.env` - Web server configuration
- `api.env` - API service configuration

## Key Features Demonstrated

1. **Named Environments**: `oneenv.env(name)` creates isolated environment spaces
2. **Fallback Logic**: Named environments fall back to common environment, then OS environment
3. **Load Override**: Control whether to override existing values when loading
4. **Practical Usage**: Real-world application configuration patterns