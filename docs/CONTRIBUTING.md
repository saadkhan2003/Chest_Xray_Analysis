# Contributing to AI X-Ray Assistant

Thank you for your interest in contributing to the AI X-Ray Assistant project! This document provides guidelines and instructions for contributing.

---

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Gender, gender identity, or expression
- Sexual orientation
- Disability
- Personal appearance
- Body size
- Race or ethnicity
- Age
- Religion or lack thereof

### Expected Behavior

- ✅ Be respectful and inclusive
- ✅ Welcome newcomers and help them get started
- ✅ Provide constructive feedback
- ✅ Focus on what is best for the community
- ✅ Show empathy towards other contributors

### Unacceptable Behavior

- ❌ Harassment or discriminatory language
- ❌ Personal attacks or trolling
- ❌ Publishing others' private information
- ❌ Spam or off-topic discussions

### Enforcement

Violations of the Code of Conduct can be reported by opening an issue or contacting the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? Help us improve by reporting it!

**Before submitting:**
1. Check [existing issues](https://github.com/yourusername/AI-XRay-Assistant/issues) to avoid duplicates
2. Ensure you're using the latest version
3. Verify the bug is reproducible

**Bug Report Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. Upload '...'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Windows 10, Ubuntu 22.04]
- Python Version: [e.g. 3.10.5]
- Browser: [e.g. Chrome 120]
- Installation Method: [local/executable/docker]

**Additional context**
Any other relevant information.
```

### 💡 Suggesting Enhancements

Have an idea to improve the project?

**Enhancement Suggestion Template:**
```markdown
**Is your feature request related to a problem?**
A clear description of the problem. Ex. "I'm always frustrated when..."

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Additional context**
Any other context, mockups, or examples.
```

### 📝 Improving Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples or tutorials
- Translate documentation
- Improve code comments
- Create video tutorials

### 🧪 Adding Test Cases

Help improve code quality:
- Write unit tests for existing features
- Add integration tests
- Create test datasets
- Improve test coverage

### 🎨 UI/UX Improvements

Enhance the user interface:
- Improve Streamlit UI design
- Add visualizations
- Enhance accessibility
- Create new themes

### 🔬 Model Improvements

Advance the ML capabilities:
- Train on new datasets
- Experiment with different architectures
- Improve model accuracy
- Optimize inference speed
- Add new pathology detection

---

## Getting Started

### Prerequisites

- **Git**: [Install Git](https://git-scm.com/downloads)
- **Python 3.10+**: [Install Python](https://www.python.org/downloads/)
- **GitHub Account**: [Sign up](https://github.com/join)

### Fork and Clone

1. **Fork the repository**:
   - Click the "Fork" button on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-XRay-Assistant.git
   cd AI-XRay-Assistant
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/yourusername/AI-XRay-Assistant.git
   ```

### Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (choose your OS)
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # If available
# Or manually install:
pip install pytest black flake8 mypy
```

### Download Test Models

You need model files for testing. See [`models/README.md`](../models/README.md) for instructions.

### Verify Setup

```bash
# Run the app
streamlit run app.py

# Run tests (if available)
pytest tests/
```

---

## Development Workflow

### 1. Create a Branch

Create a descriptive branch for your work:

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/amazing-feature
# Or for bug fixes:
git checkout -b fix/bug-description
```

**Branch Naming Conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/improvements
- `chore/` - Maintenance tasks

### 2. Make Your Changes

- Write clean, readable code
- Follow the [coding standards](#coding-standards)
- Add comments for complex logic
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run the app locally
streamlit run app.py

# Test with sample images
# Upload images from test_images/ folder

# Run automated tests (if available)
pytest tests/

# Check code style
flake8 app.py
black --check app.py
```

### 4. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of what you did

- Detailed point 1
- Detailed point 2
- Fixes #123"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line: 50 chars or less
- Reference issues/PRs when applicable

### 5. Push to Your Fork

```bash
git push origin feature/amazing-feature
```

### 6. Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request" button
3. Fill out the PR template (see below)
4. Submit for review

---

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines:

```python
# Good
def predict_pneumonia(image: Image.Image) -> dict:
    """
    Predict pneumonia from chest X-ray image.
    
    Args:
        image: PIL Image object of chest X-ray
        
    Returns:
        Dictionary with prediction results
    """
    preprocessed = preprocess_image(image)
    prediction = model(preprocessed)
    return format_prediction(prediction)

# Avoid
def pred(img):
    p = preprocess_image(img)
    return model(p)
```

### Code Formatting

Use **Black** for automatic formatting:

```bash
# Format all Python files
black .

# Check without modifying
black --check .
```

### Linting

Use **flake8** for style checking:

```bash
# Check all files
flake8 app.py scripts/ docs/

# Configuration in setup.cfg or .flake8:
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv
ignore = E203, W503
```

### Type Hints

Use type hints for better code clarity:

```python
from typing import Tuple, Optional
import torch
from PIL import Image

def preprocess_image(
    image: Image.Image,
    size: Tuple[int, int] = (224, 224)
) -> torch.Tensor:
    """Preprocess image for model inference."""
    # ...
    return tensor
```

### Documentation Strings

Use Google-style docstrings:

```python
def train_model(
    train_loader: DataLoader,
    val_loader: DataLoader,
    epochs: int = 25
) -> nn.Module:
    """
    Train the pneumonia detection model.
    
    Args:
        train_loader: DataLoader for training data
        val_loader: DataLoader for validation data
        epochs: Number of training epochs (default: 25)
        
    Returns:
        Trained PyTorch model
        
    Raises:
        ValueError: If epochs < 1
        RuntimeError: If CUDA out of memory
        
    Example:
        >>> train_loader = create_dataloader("data/train")
        >>> val_loader = create_dataloader("data/val")
        >>> model = train_model(train_loader, val_loader, epochs=10)
    """
    if epochs < 1:
        raise ValueError(f"epochs must be >= 1, got {epochs}")
    
    # Training logic here
    return model
```

### File Organization

```python
# Order of imports:
# 1. Standard library
import os
import sys
from typing import List

# 2. Third-party packages
import torch
import streamlit as st
import numpy as np

# 3. Local imports
from utils import preprocess_image
from models import load_model

# Constants at top
MODEL_PATH = "models/densenet121_pneumonia.pth"
CLASSES = ["BACTERIA", "NORMAL", "VIRUS"]

# Functions
def helper_function():
    pass

# Main code
if __name__ == "__main__":
    main()
```

---

## Testing Guidelines

### Writing Tests

Create test files in `tests/` directory:

```python
# tests/test_preprocessing.py
import pytest
from PIL import Image
import numpy as np
from app import preprocess_pediatric

def test_preprocess_output_shape():
    """Test that preprocessing outputs correct tensor shape"""
    image = Image.new('RGB', (512, 512))
    tensor = preprocess_pediatric(image)
    
    assert tensor.shape == (1, 3, 224, 224)

def test_preprocess_normalization():
    """Test that image is properly normalized"""
    image = Image.new('RGB', (224, 224), color=(128, 128, 128))
    tensor = preprocess_pediatric(image)
    
    # Check tensor is normalized (roughly in [-3, 3] range)
    assert tensor.min() >= -3
    assert tensor.max() <= 3

@pytest.mark.parametrize("size", [(100, 100), (512, 512), (1024, 1024)])
def test_preprocess_various_sizes(size):
    """Test preprocessing with different image sizes"""
    image = Image.new('RGB', size)
    tensor = preprocess_pediatric(image)
    
    # Should always output 224x224
    assert tensor.shape[-2:] == (224, 224)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_preprocessing.py

# Run specific test function
pytest tests/test_preprocessing.py::test_preprocess_output_shape

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Test Coverage

Aim for >80% code coverage on core functionality:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Documentation

### Code Comments

```python
# Good: Explain WHY, not WHAT
# Use patient-level splitting to prevent data leakage
# (same patient's images should not appear in both train and test)
train_patients, test_patients = train_test_split(unique_patients, test_size=0.2)

# Avoid: Obvious comments
# Split patients into train and test
train_patients, test_patients = train_test_split(unique_patients, test_size=0.2)
```

### README Updates

When adding features, update relevant documentation:
- Main README.md
- Appropriate docs/*.md files
- Code comments
- Docstrings

### Writing Tutorials

If creating tutorials:
- Use clear, step-by-step instructions
- Include screenshots where helpful
- Provide example code
- Test all instructions before submitting

---

## Pull Request Process

### PR Template

```markdown
## Description
Brief description of changes

Fixes #(issue number)

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to not work as expected)
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tested locally with sample images
- [ ] All existing tests pass
- [ ] Added new tests for new features
- [ ] Updated documentation

## Screenshots (if applicable)
Add screenshots showing the changes

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### Review Process

1. **Automated Checks**: CI/CD will run tests and linters
2. **Code Review**: Maintainer(s) will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, PR will be merged

### Responding to Feedback

- Be open to suggestions
- Ask questions if unclear
- Make requested changes promptly
- Thank reviewers for their time

---

## Issue Guidelines

### Creating Issues

Use appropriate labels:
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested

### Issue Etiquette

- **Be specific**: Provide details and examples
- **Be patient**: Maintainers are volunteers
- **Be respectful**: Follow Code of Conduct
- **Follow up**: Provide additional info if requested

---

## Project Structure for Contributors

```
AI-XRay-Assistant/
├── app.py                 # Main Streamlit app - UI and inference logic
├── run_main.py           # PyInstaller entry point
├── build_exe.py          # Executable build script
├── requirements.txt      # Python dependencies
│
├── models/               # Model files (.pth)
│   └── README.md        # Model download instructions
│
├── notebooks/           # Training notebooks
│   ├── Colab_Model_training.ipynb   # Pediatric model training
│   └── NIH_Adult_Training.ipynb     # Adult model setup
│
├── scripts/             # Utility scripts
│   ├── colab_data_setup.py    # Dataset downloader
│   └── nih_data_setup.py      # NIH dataset helper
│
├── docs/                # Documentation
│   ├── README.md              # Auto-generated index
│   ├── INSTALLATION.md        # Setup guide
│   ├── USAGE.md               # User guide
│   ├── TRAINING.md            # Training guide
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── CONTRIBUTING.md        # This file
│   ├── MODEL_CARD.md          # ML model specs
│   └── PROJECT_STRUCTURE.md   # Architecture overview
│
├── test_images/         # Sample images for testing
│   ├── Normal/
│   └── Bacteria_and_Virus/
│
├── tests/               # Automated tests (if available)
│   └── test_*.py
│
└── .github/             # GitHub-specific files
    ├── workflows/       # CI/CD pipelines
    └── ISSUE_TEMPLATE/  # Issue templates
```

### Key Files to Know

- **`app.py`**: Main application logic - models, preprocessing, UI
- **`requirements.txt`**: All Python dependencies
- **`docs/*.md`**: User-facing documentation
- **`notebooks/*.ipynb`**: Training and experimentation

---

## Recognition

Contributors will be recognized in:
- GitHub Contributors page
- CHANGELOG.md for significant contributions
- README.md acknowledgments section

---

## Questions?

- **General Questions**: [GitHub Discussions](https://github.com/yourusername/AI-XRay-Assistant/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/AI-XRay-Assistant/issues)
- **Security Issues**: Email maintainers privately

---

## License

By contributing, you agree that your contributions will be licensed under the same [MIT License](../LICENSE) that covers the project.

---

**Thank you for contributing to AI X-Ray Assistant! 🙏**

Your contributions help advance AI in healthcare and make this tool better for everyone.

---

**Last Updated**: March 3, 2026  
**Contributing Guide Version**: 1.0
