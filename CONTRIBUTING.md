# Contributing to Heatmap Generator

Thank you for considering contributing to the Heatmap Generator project! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant code samples or error messages

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you might have

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Add tests** for any new functionality

4. **Ensure all tests pass**
   ```bash
   python -m unittest discover -s tests -v
   ```

5. **Update documentation** as needed

6. **Commit your changes** with clear, descriptive commit messages
   ```bash
   git commit -m "Add feature: description of feature"
   ```

7. **Push to your fork** and submit a pull request
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints for function parameters and return values

### Documentation

- Add docstrings to all functions, classes, and modules
- Use Google-style docstring format
- Update README.md for significant changes

### Testing

- Write unit tests for all new functionality
- Maintain or improve code coverage
- Tests should be clear and well-documented

### Example Code Style

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    More detailed description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When and why this is raised
    """
    # Implementation
    return True
```

## Development Setup

1. Clone the repository
   ```bash
   git clone https://github.com/dot-gabriel-ferrer/heatmap.git
   cd heatmap
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run tests to verify setup
   ```bash
   python -m unittest discover -s tests -v
   ```

## Project Structure

```
heatmap/
├── heatmap/           # Core heatmap generation
├── motion/            # Motion simulation
├── animation/         # Animation utilities
├── utils/             # Utility functions
├── tests/             # Unit tests
├── examples/          # Example scripts
├── cli.py             # Command-line interface
└── simulation.py      # Simulation script
```

## Questions?

If you have questions about contributing, feel free to:
- Open an issue on GitHub
- Ask in pull request discussions

Thank you for contributing to Heatmap Generator!
