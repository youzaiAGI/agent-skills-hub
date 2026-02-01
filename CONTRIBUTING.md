# Contributing to Agent Skills Hub

Thank you for your interest in contributing to Agent Skills Hub!

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Setup Development Environment

#### Windows

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
python -m venv venv
venv\Scripts\activate
pip install -e .
```

#### Linux / macOS

```bash
git clone https://github.com/youzaiAGI/agent-skills-hub.git
cd agent-skills-hub
python -m venv venv
source venv/bin/activate
pip install -e .
```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When creating a bug report, include:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Environment information (OS, Python version)
- Any relevant logs or screenshots

### Suggesting Enhancements

We welcome suggestions for new features or improvements:
- Use a clear and descriptive title
- Describe the enhancement in detail
- Explain why this enhancement would be useful
- Provide examples of how the enhancement would be used

### Adding New Agent Support

To add support for a new AI Agent, edit `skill_hub/utils/agent_cmd.py` and add the agent configuration:

```python
config_data = {
    # ... existing configs
    "NewAgent": [
        ".newagent/skills",
        "~/.newagent/skills"
    ],
}
```

### Submitting Code Changes

1. Fork the repository
2. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Run tests (if available)
5. Commit your changes with clear messages
6. Push to your fork
7. Create a Pull Request

### Code Style

- Follow PEP 8 style guide
- Keep functions focused and modular
- Add docstrings for new functions
- Use meaningful variable and function names

## Coding Standards

### Python Code

- Use 4 spaces for indentation
- Line length should not exceed 100 characters
- Use type hints where appropriate
- Add comments for complex logic

### Documentation

- Keep README.md updated with new features
- Update version numbers when making releases
- Add examples for new commands or features

## Testing

Before submitting a pull request:
- Test your changes on multiple platforms if possible (Windows, Linux, macOS)
- Ensure existing functionality is not broken
- Test edge cases

## Pull Request Process

1. Ensure your code follows the project's style guidelines
2. Update documentation if needed
3. Write a clear description of your changes in the PR
4. Reference related issues if applicable
5. Wait for code review feedback
6. Make requested changes

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the `question` label
- Contact the maintainers

## License

By contributing to Agent Skills Hub, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!**
