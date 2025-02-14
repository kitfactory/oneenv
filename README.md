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

Compare two `.env`