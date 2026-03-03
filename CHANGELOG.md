# Changelog

All notable changes to the AI X-Ray Assistant project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned

- Docker containerization
- REST API with FastAPI
- Batch processing mode
- DICOM file support
- Additional pathology detection (TB, COVID-19)
- Mobile app version
- Grad-CAM visualization in UI
- Multi-language support

---

## [1.0.0] - 2026-03-03

### 🎉 Initial Release

The first stable release of AI X-Ray Assistant with dual-model support for pneumonia detection.

### Added

#### Core Features

- **Dual-Model System**: Support for both pediatric and adult X-ray analysis
  - Pediatric model: 3-class classification (Normal/Bacteria/Virus)
  - Adult model: Binary classification (Normal/Pneumonia)
- **Streamlit Web Interface**: User-friendly web application
- **Model Selection**: Dynamic switching between pediatric and adult models
- **Image Upload**: Drag-and-drop or file browser upload
- **Real-time Inference**: Fast prediction with confidence scores
- **Detailed Probabilities**: Show prediction breakdown for all classes

#### Models

- **Pediatric Model** (`densenet121_pneumonia.pth`):

  - DenseNet121 architecture
  - Trained on Kaggle Pediatric Pneumonia Dataset
  - 98.6% infection sensitivity
  - ~87% overall accuracy
  - Patient-level data splitting
  - Weighted loss for class imbalance
- **Adult Model** (`densenet121_adult_rsna.pth`):

  - DenseNet121 architecture (1-channel grayscale input)
  - Pre-trained on RSNA Pneumonia Challenge
  - TorchXRayVision integration
  - Binary pneumonia detection

#### Training Notebooks

- `Colab_Model_training.ipynb`: Complete pediatric model training pipeline

  - Kaggle API integration
  - Patient-level data splitting
  - Data augmentation with Albumentations
  - Training with GPU acceleration
  - Evaluation metrics and confusion matrix
  - Grad-CAM visualization
- `NIH_Adult_Training.ipynb`: Adult model setup

  - TorchXRayVision pre-trained weights
  - Quick setup (no training required)
  - Model extraction for deployment

#### Scripts

- `colab_data_setup.py`: Automated dataset download and organization

  - Kaggle dataset download
  - Patient-level splitting logic
  - Directory structure organization
  - Hidden file filtering
- `nih_data_setup.py`: NIH dataset helper functions

#### Deployment

- **One-Click Launchers**:
  - `run_app.bat` for Windows
  - `run_app.sh` for Linux/macOS
- **PyInstaller Support**:
  - `build_exe.py` for creating standalone executable
  - `run_main.py` as entry point
  - `AI_XRay_Assistant.spec` configuration
- **Portable Execution**: No installation required for end users

#### Documentation

- Comprehensive **README.md** with:

  - Project overview and features
  - Architecture diagrams
  - Performance metrics
  - Quick start guide
  - Project structure
  - Tech stack details
- **docs/INSTALLATION.md**: Detailed installation guide

  - System requirements
  - Multiple installation methods
  - Model download instructions
  - Troubleshooting section
- **docs/USAGE.md**: Complete usage guide

  - Interface overview
  - Model selection guide
  - Image upload instructions
  - Result interpretation
  - Best practices
- **docs/TRAINING.md**: Model training guide

  - Google Colab setup
  - Hyperparameter tuning
  - Custom dataset training
  - Evaluation metrics
- **docs/DEPLOYMENT.md**: Deployment options

  - Local deployment
  - Docker containerization
  - Cloud deployment (AWS, GCP, Azure)
  - REST API development
  - Security best practices
- **docs/CONTRIBUTING.md**: Contribution guidelines

  - Code of conduct
  - Development workflow
  - Coding standards
  - Testing guidelines
- **docs/MODEL_CARD.md**: ML model specifications

  - Model details and architecture
  - Training data description
  - Performance metrics
  - Limitations and ethical considerations
- **docs/PROJECT_STRUCTURE.md**: Architecture overview

  - File descriptions
  - Directory structure
  - Component explanations

#### Testing

- **Sample Images**: `test_images/` directory with:
  - Normal chest X-rays
  - Bacterial and viral pneumonia cases
  - Ready-to-use test data

#### Configuration

- `.streamlit/config.toml`: Streamlit app configuration
- `requirements.txt`: Python dependencies with version pinning
- `.gitignore`: Proper exclusions for Python, models, and IDE files

### Dependencies

- PyTorch 2.0+
- TorchVision
- Streamlit 1.30+
- TorchXRayVision
- Pillow (PIL)
- NumPy
- scikit-learn
- Albumentations
- Matplotlib & Seaborn
- ONNX Runtime (optional)

### Technical Details

#### Architecture

- **Base Model**: DenseNet121 (Huang et al., 2017)
- **Pre-training**: ImageNet-1K for pediatric model
- **Fine-tuning**: Transfer learning on medical datasets
- **Input Size**: 224×224 pixels
- **Model Size**: ~27MB per model

#### Data Processing

- **Patient-Level Splitting**: Prevents data leakage
- **Data Augmentation**:
  - Horizontal flip
  - Random rotation (±10°)
  - Brightness/contrast adjustment
- **Normalization**: ImageNet statistics for pediatric, XRV for adult
- **Class Weighting**: Handles imbalanced datasets

#### Performance

- **Inference Time**: <3 seconds on CPU
- **GPU Support**: CUDA acceleration available
- **Batch Processing**: Optimized for single-image workflow
- **Memory Usage**: ~2GB RAM minimum

---

## Version History

### Version Numbering

- **Major version** (X.0.0): Breaking changes or major new features
- **Minor version** (1.X.0): New features, backwards compatible
- **Patch version** (1.0.X): Bug fixes, minor improvements

---

## How to Update

### For Users

To update to the latest version:

```bash
# Navigate to project directory
cd AI-XRay-Assistant

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart the application
streamlit run app.py
```

### For Executable Users

1. Download the latest release from [GitHub Releases](https://github.com/yourusername/AI-XRay-Assistant/releases)
2. Extract to a new folder
3. Copy your `models/` folder to the new installation
4. Run the new executable

---

## Migration Guide

### From Pre-release to 1.0.0

If you were using an earlier development version:

1. **Backup your models**: Copy `*.pth` files to a safe location
2. **Pull latest code**: `git pull origin main`
3. **Reinstall dependencies**: `pip install -r requirements.txt --force-reinstall`
4. **Restore models**: Move `*.pth` files back to `models/` folder
5. **Test**: Run the app and verify both models work

### Breaking Changes

None in this release (initial stable version).

---

## Known Issues

### Version 1.0.0

- **Large File Uploads**: Files > 10MB may timeout on slow connections

  - **Workaround**: Resize images before uploading
- **DICOM Support**: Not yet implemented

  - **Workaround**: Convert DICOM to JPEG/PNG using external tools
- **Grad-CAM in UI**: Visualization not shown in web interface

  - **Workaround**: Use training notebook for Grad-CAM analysis
- **Multi-Image Batch**: No batch processing mode

  - **Workaround**: Upload images one at a time
- **Mobile Responsiveness**: UI not optimized for mobile devices

  - **Workaround**: Use desktop browser

---

## Deprecated Features

None in this release.

---

## Security Updates

### Version 1.0.0

- Implemented file type validation for uploads
- Added file size limits (10MB)
- Secure model file loading
- No patient data logging

---

## Contributors

### Version 1.0.0

- **Muhammad Saad Khan** - Initial development and release

Special thanks to:

- Kaggle community for datasets
- PyTorch and Streamlit teams
- Open-source medical AI community

---

## Future Roadmap

See [README.md](README.md#-future-roadmap) for planned features and enhancements.

---

**Keep up to date**: Watch the repository on GitHub to receive notifications of new releases.

**Report Issues**: Found a bug? [Open an issue](https://github.com/yourusername/AI-XRay-Assistant/issues/new).

---

*Last Updated: March 3, 2026*
