# OneEnv 🌟　[![PyPI Downloads](https://static.pepy.tech/badge/oneenv)](https://pepy.tech/projects/oneenv)

OneEnv is an environment variable management and generation tool for Python applications. It wraps [`python-dotenv`](https://github.com/theskumar/python-dotenv) to simplify handling of environment variable templates and `.env` files.

## What Problems Does OneEnv Solve? 🛠️

Managing environment variables for multiple libraries can be tedious and error-prone, especially when each library requires its own configuration. OneEnv streamlines the process by consolidating environment variable templates into a single `.env.example` file, reducing manual work and ensuring consistency across projects.

## Features 🚀

- **Template Collection**: Use the `@oneenv` decorator to declare environment variable templates.
- **Team-Friendly**: Perfect for microservices and modular development where multiple small libraries need to manage their own environment variables.
- **Decentralized Configuration**: Each library can define its own environment variables independently, making it easy to maintain and scale in team development.
- **Generated `.env.example`**: Automatically creates a consolidated `.env.example` file from registered templates.
- **Diff Functionality**: Compare changes between different versions of your `.env.example` file.
- **Duplicate Key Detection**: Identify duplicate environment variable definitions across modules.
- **Command Line Tool**: Easily run commands like `oneenv template` and `oneenv diff` from your terminal.

## Supported Environments 🖥️

- **Python**: ≥ 3.11
- **Operating Systems**: Windows, macOS, Linux

## Installation 📦

You can install OneEnv easily via pip:

```bash
pip install oneenv
```

For development mode, install from the source using:

```bash
pip install -e .
```

## Usage 🚀

### Generating Environment Template

Generate a consolidated `.env.example` file using the registered templates:

```bash
oneenv template [-o OUTPUT_FILE] [-d]
```

Use the `-d` or `--debug` option to see which modules and templates are discovered:

```bash
oneenv template -d
```

### Comparing Environment Files

Compare changes between two `.env` files:

```bash
oneenv diff previous.env current.env
```

### Example: Using the `@oneenv` Decorator

Here's an example of declaring environment variable templates using the `@oneenv` decorator:

```python
from oneenv import oneenv

@oneenv
def my_env_template():
    return {
        "MY_API_KEY": {
            "description": "API key for accessing the service.",
            "default": "",
            "required": True,
            "choices": []
        },
        "MODE": {
            "description": "Application mode setting.",
            "default": "development",
            "required": False,
            "choices": ["development", "production"]
        }
    }
```

🚨 **IMPORTANT WARNING**: 
Template modules **MUST** be imported for the templates to be discovered. The `@oneenv` decorator works by scanning imported modules for decorated functions. If you don't import your template module, **your templates will not be included** in the generated `.env.example` file.

Example structure:
```
your_package/
  __init__.py      # Import your template modules here
  template.py      # Define your @oneenv decorated functions here
```

Example `__init__.py`:
```python
from . import template  # Without this import, templates in template.py will NOT be discovered
```

You can use the `@oneenv` decorator in your code to declare environment variable templates as shown above. After defining your templates and ensuring the modules are imported, you can generate the template file using:

```bash
oneenv template -o .env.template
```

**Note:** When implementing the `@oneenv` decorator, only the `description` attribute is required. Other attributes (`default`, `required`, `choices`) are optional.

### Simple Example: Basic Template Definition

For the simplest use case, you can specify just the required `description` attribute:

```python
from oneenv import oneenv

@oneenv
def simple_config():
    return {
        "SIMPLE_VAR": {
            "description": "A simple environment variable."
        }
    }
```

## Integration with dotenv 🔄

OneEnv wraps [python-dotenv](https://github.com/theskumar/python-dotenv), so you can use all dotenv features directly.

## Running Tests 🧪

With your virtual environment activated, run:

```bash
pytest tests
```

## Contributing 🤝

Contributions are welcome!  
Feel free to open an issue or submit a Pull Request on GitHub.

## License ⚖️

This project is released under the MIT License.