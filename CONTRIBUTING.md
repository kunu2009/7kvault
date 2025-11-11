# Contributing to 7K Vault

First off, thank you for considering contributing to 7K Vault! It's people like you that make 7K Vault such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Please be kind and constructive.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**System Info:**
 - OS: [e.g. Windows 11]
 - Python Version: [e.g. 3.12]
 - 7K Vault Version: [e.g. 1.0.0]

**Additional context**
Any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title** and description
- **Step-by-step description** of the suggested enhancement
- **Explain why** this enhancement would be useful
- **List similar features** in other applications if applicable

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** following the coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Write descriptive commit messages**
6. **Submit your pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/7kvault.git
cd 7kvault

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pylint black pytest

# Run the app
python vault_app.py
```

## Coding Standards

### Python Style Guide

- Follow **PEP 8** style guide
- Use **4 spaces** for indentation (not tabs)
- Maximum line length: **100 characters**
- Use descriptive variable names
- Add docstrings to all functions and classes

### Code Formatting

```bash
# Format code with black
black vault_app.py

# Check with pylint
pylint vault_app.py
```

### Example Good Code:

```python
def encrypt_file(self, file_path: Path) -> bytes:
    """
    Encrypt a file using Fernet encryption.
    
    Args:
        file_path: Path to the file to encrypt
        
    Returns:
        Encrypted file data as bytes
        
    Raises:
        FileNotFoundError: If file doesn't exist
        EncryptionError: If encryption fails
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    return self.cipher.encrypt(data)
```

## Testing

Before submitting a pull request:

1. **Test all existing features** - make sure nothing broke
2. **Test your new feature** thoroughly
3. **Test on Windows 10 and 11** if possible
4. **Test with different file types**
5. **Test edge cases** (empty vault, wrong password, etc.)

## Project Structure

```
7kvault/
├── vault_app.py              # Main application
├── reset_password.py          # Password reset utility
├── requirements.txt           # Python dependencies
├── LaunchVault.bat           # Windows launcher
├── ResetPassword.bat         # Password reset launcher
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── CONTRIBUTING.md           # This file
├── .gitignore               # Git ignore rules
└── docs/                    # Website files
    ├── index.html
    ├── style.css
    └── script.js
```

## Feature Development Checklist

When adding a new feature:

- [ ] Feature works as intended
- [ ] No breaking changes to existing features
- [ ] Code follows style guidelines
- [ ] Added comments for complex logic
- [ ] Updated README.md if needed
- [ ] Tested on Windows
- [ ] No security vulnerabilities
- [ ] No performance regressions

## Security Guidelines

**IMPORTANT:** When contributing to security-related code:

1. **Never** commit passwords, keys, or sensitive data
2. **Always** use proper encryption libraries
3. **Test** security features thoroughly
4. **Document** security implications
5. **Follow** best practices for cryptography

## Commit Message Guidelines

Good commit messages help others understand changes:

```
feat: Add shuffle mode to media player
fix: Fix fullscreen mode not resizing properly
docs: Update README with new shortcuts
style: Format code with black
refactor: Simplify folder navigation logic
test: Add tests for encryption functions
```

Prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code formatting
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## Documentation

When adding features:

1. Update README.md with new information
2. Add keyboard shortcuts to documentation
3. Update FAQ if needed
4. Add code comments for complex logic
5. Update website docs/ if UI changes

## Getting Help

- **Questions**: Open a GitHub issue with the `question` label
- **Discussions**: Use GitHub Discussions
- **Bugs**: Open an issue with the `bug` label

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (coming soon)
- Mentioned in release notes
- Thanked in the README.md

Thank you for making 7K Vault better! 🎉
