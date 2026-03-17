# Contributing to Object Detection System

First off, thank you for considering contributing to this project! 🎉

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)

## Code of Conduct

This project adheres to a simple code of conduct:
- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on what's best for the community

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When creating a bug report, include:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Error messages or logs
- Screenshots if applicable

Use the bug report template: `.github/ISSUE_TEMPLATE/bug_report.md`

### Suggesting Features

Feature suggestions are welcome! Please:
- Check if the feature has already been suggested
- Clearly describe the problem it solves
- Provide use case examples
- Indicate if you're willing to implement it

Use the feature request template: `.github/ISSUE_TEMPLATE/feature_request.md`

### Code Contributions

We welcome code contributions! Here are some areas that need help:

**Good First Issues:**
- Documentation improvements
- Adding unit tests
- Bug fixes for known issues
- Performance optimizations

**Larger Features:**
- Multi-camera support
- Database integration
- Object tracking across frames
- Custom model training integration
- REST API implementation

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- (Optional) Docker for containerized development

### Setup Steps

1. **Fork and clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/object-detection-system.git
cd object-detection-system
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run tests:**
```bash
python -m pytest tests/
```

5. **Create a branch:**
```bash
git checkout -b feature/your-feature-name
```

### Development Workflow

1. Make your changes
2. Add tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Commit with clear messages
6. Push to your fork
7. Create a pull request

## Pull Request Process

1. **Before Submitting:**
   - Update documentation for any new features
   - Add/update tests as needed
   - Ensure all tests pass
   - Follow code style guidelines
   - Update CHANGELOG.md if applicable

2. **PR Description:**
   - Use the PR template
   - Link to related issues
   - Describe changes clearly
   - Include screenshots for UI changes
   - Note any breaking changes

3. **Review Process:**
   - Maintainers will review your PR
   - Address review comments
   - Keep PR focused on one feature/fix
   - Be patient and respectful

4. **After Merge:**
   - Delete your branch
   - Close related issues
   - Update your fork

## Style Guidelines

### Python Code Style

We follow PEP 8 with some flexibility. Key points:

```python
# Use descriptive variable names
good: detection_confidence = 0.85
bad:  dc = 0.85

# Add docstrings to functions
def detect(self, frame):
    """
    Run detection on a single frame.
    
    Args:
        frame: Input image (BGR format)
        
    Returns:
        annotated_frame: Frame with bounding boxes
        detections: List of detection dictionaries
    """
    pass

# Use type hints when helpful
def process_detections(detections: List[Dict]) -> pd.DataFrame:
    pass

# Keep functions focused
# One function = one responsibility

# Add comments for complex logic
# Avoid obvious comments
```

### File Organization

```
New modules should follow this pattern:

my_module.py:
  - Imports (standard library, then third-party, then local)
  - Constants
  - Classes
  - Functions
  - If __name__ == "__main__" block (if applicable)
```

### Commit Messages

Format:
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add multi-camera support

Implement support for processing multiple camera feeds simultaneously.
Includes configuration options and UI updates.

Closes #42

---

fix: resolve memory leak in detection loop

Fixed memory leak caused by not releasing video capture resources.
Added proper cleanup in finally block.

Fixes #38
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_detector.py

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

### Writing Tests

```python
# tests/test_detector.py
import pytest
from detector import ObjectDetector

def test_detector_initialization():
    """Test that detector initializes correctly."""
    detector = ObjectDetector(confidence_threshold=0.5)
    assert detector.confidence_threshold == 0.5

def test_detection_on_valid_frame():
    """Test detection on a valid frame."""
    detector = ObjectDetector()
    frame = create_test_frame()  # Helper function
    
    annotated, detections = detector.detect(frame)
    
    assert annotated is not None
    assert isinstance(detections, list)
```

### Test Coverage Goals

- New features: 80%+ coverage
- Bug fixes: Add test that reproduces the bug
- Core modules: Aim for 90%+ coverage

## Documentation

### Code Documentation

- Add docstrings to all public functions/classes
- Include type hints
- Provide usage examples
- Document side effects

### README Updates

When adding features:
- Update feature list
- Add usage examples
- Update installation instructions if needed
- Add screenshots/demos

### Creating Examples

Add examples to `examples/` directory:
```python
# examples/custom_alert_example.py
"""
Example: Creating custom alert handlers

This example shows how to create a custom alert handler
for sending notifications to Slack.
"""

from alerts import AlertSystem

class SlackAlertSystem(AlertSystem):
    # Implementation here
    pass

# Usage
if __name__ == "__main__":
    # Demo code
    pass
```

## Getting Help

- 💬 Join discussions in GitHub Discussions
- 🐛 Report bugs via GitHub Issues
- 📧 Email: [maintainer email]
- 📚 Check existing documentation

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

---

Thank you for contributing! 🚀
