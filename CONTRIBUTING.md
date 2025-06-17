# Contributing to RapidApply

First off, thank you for considering contributing to RapidApply! It's people like you that make RapidApply such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Screenshots if applicable
- Your environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- A clear and descriptive title
- A detailed description of the proposed functionality
- Any possible drawbacks
- Mock-ups or examples if applicable

### Pull Requests

1. Fork the repo and create your branch from `develop`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Issue that pull request!

## Development Process

### Branch Naming Convention

- `feature/` - New features (e.g., `feature/add-indeed-support`)
- `bugfix/` - Bug fixes (e.g., `bugfix/fix-login-error`)
- `hotfix/` - Urgent fixes for production (e.g., `hotfix/critical-security-patch`)
- `release/` - Release preparation (e.g., `release/v2.0.0`)

### Commit Messages

Follow conventional commits format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Changes to build process or auxiliary tools

Example:
```
feat(apply): add support for cover letter customization

- Implement AI-powered cover letter generation
- Add configuration options for cover letter templates
- Update UI to include cover letter preview

Closes #123
```

### Code Style Guidelines

#### Python
- Follow PEP 8
- Use type hints where applicable
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use meaningful variable names

Example:
```python
def calculate_match_score(job_description: str, resume_text: str) -> float:
    """
    Calculate the match score between a job description and resume.
    
    Args:
        job_description: The job posting description
        resume_text: The candidate's resume content
        
    Returns:
        A float between 0 and 1 representing the match percentage
    """
    # Implementation here
    return score
```

### Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Aim for at least 80% code coverage
- Test edge cases and error scenarios

### Documentation

- Update README.md if needed
- Add docstrings to new functions/classes
- Update wiki for significant features
- Include inline comments for complex logic

## Review Process

1. All submissions require review before merging
2. Reviewers will check for:
   - Code quality and style
   - Test coverage
   - Documentation
   - Performance implications
   - Security considerations

## Community

- **Discord**: Connect with Nickalus on Discord
- **GitHub Discussions**: For general questions and discussions
- **Issues**: For bug reports and feature requests

## Recognition

Contributors will be recognized in:
- The README.md contributors section
- Release notes
- Our Discord community

Thank you for contributing to RapidApply! 🚀