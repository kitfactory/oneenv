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
oneenv template [-o OUTPUT_FILE]
```

### Comparing Environment Files

Compare two `.env` files to see what has changed:

```bash
oneenv diff previous.env current.env
```

### Example: Using the `@oneenv` Decorator

Below is an example of how to use the `@oneenv` decorator in your code:

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

Place the above code within your library or application to define environment variable templates.

**Note:** When implementing `get_template()`, it is sufficient to only provide the `description` attribute. Other attributes such as `default`, `required`, and `choices` are optional.

### Minimal Example: Simple Template Definition

For the simplest setup, you can create a function with just the required description:

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

This minimal example works perfectly and emphasizes the ease of use. The `@oneenv` decorator automatically registers this template function for environment variable management.

### Dotenv Integration 🔄

OneEnv wraps [python-dotenv](https://github.com/theskumar/python-dotenv), so you can use all dotenv functions directly through OneEnv.

#### Example: Loading Environment Variables Using OneEnv

You can use OneEnv to load environment variables from a `.env` file just like you would with python-dotenv:

```python
from oneenv import load_dotenv, dotenv_values

# Load environment variables into the current process
load_dotenv()

# Alternatively, get them as a dictionary
env_vars = dotenv_values(".env")
print(env_vars)
```

The integration allows you to manage your environment variables in one centralized place while benefiting from all the features of python-dotenv.

## Running Tests 🧪

Make sure your virtual environment is active, then run:

```bash
pytest tests
```

## Contributing 🤝

Contributions are welcome! Feel free to open issues or submit pull requests on GitHub.

## License ⚖️

This project is licensed under the MIT License.
