# Installation Guide

Complete installation instructions for the AI X-Ray Assistant application.

---

## Table of Contents
- [System Requirements](#system-requirements)
- [Method 1: One-Click Installation](#method-1-one-click-installation-recommended)
- [Method 2: Manual Installation](#method-2-manual-installation)
- [Method 3: Using Pre-built Executable](#method-3-using-pre-built-executable)
- [Downloading Model Weights](#downloading-model-weights)
- [Troubleshooting](#troubleshooting)
- [Verification](#verification)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Ubuntu 20.04+, macOS 10.15+
- **Python**: 3.10 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space (for dependencies + models)
- **Internet**: Required for initial setup

### Recommended Requirements
- **RAM**: 8GB or more
- **GPU**: NVIDIA GPU with CUDA support (optional, speeds up inference)
- **Storage**: 5GB free space

### Supported Python Versions
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12
- ❌ Python 3.9 or older (not tested)

---

## Method 1: One-Click Installation (Recommended)

### Windows

1. **Download the repository** (or clone it):
   ```bash
   git clone https://github.com/yourusername/AI-XRay-Assistant.git
   cd AI-XRay-Assistant
   ```

2. **Double-click** `run_app.bat` in File Explorer
   - The script will automatically:
     - Check for Python installation
     - Create a virtual environment
     - Install all dependencies
     - Download models (if available)
     - Launch the web application

3. **Access the app** at `http://localhost:8501`

### Linux/macOS

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/AI-XRay-Assistant.git
   cd AI-XRay-Assistant
   ```

2. **Make the script executable**:
   ```bash
   chmod +x run_app.sh
   ```

3. **Run the launcher**:
   ```bash
   ./run_app.sh
   ```

4. **Access the app** at `http://localhost:8501`

---

## Method 2: Manual Installation

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **Important**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
python3 --version
```

#### macOS
```bash
# Using Homebrew
brew install python@3.10
python3 --version
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/AI-XRay-Assistant.git
cd AI-XRay-Assistant
```

Or download as ZIP and extract it.

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- PyTorch & TorchVision
- Streamlit
- TorchXRayVision
- Pillow, NumPy, scikit-learn
- And more...

**Note**: Installation may take 5-10 minutes depending on your internet speed.

### Step 6: Verify Installation

```bash
python -c "import torch; import streamlit; print('✅ All dependencies installed successfully!')"
```

---

## Method 3: Using Pre-built Executable

### Windows Executable

1. **Download** the latest release from [Releases](https://github.com/yourusername/AI-XRay-Assistant/releases)

2. **Extract** the ZIP file to a folder

3. **Copy models** to the `models/` subfolder:
   - `densenet121_pneumonia.pth` (Pediatric model)
   - `densenet121_adult_rsna.pth` (Adult model)

4. **Double-click** `AI_XRay_Assistant.exe`

5. **Wait** for the app to launch (may take 30-60 seconds on first run)

### Building Your Own Executable

If you want to build the executable yourself:

```bash
# Activate virtual environment
pip install pyinstaller

# Run the build script
python build_exe.py

# Find executable in dist/AI_XRay_Assistant/
```

---

## Downloading Model Weights

The application requires trained model files (`.pth` format) to function. These files are **not included in the repository** due to their size.

### Option 1: Train Your Own Models

#### Pediatric Model
1. Open [notebooks/Colab_Model_training.ipynb](../notebooks/Colab_Model_training.ipynb) in Google Colab
2. Upload your Kaggle API key (`kaggle.json`)
3. Run all cells in the notebook
4. Download `densenet121_pneumonia.pth` from Colab Files sidebar
5. Place it in the `models/` folder

#### Adult Model
1. Open [notebooks/NIH_Adult_Training.ipynb](../notebooks/NIH_Adult_Training.ipynb) in Google Colab
2. Run all cells (uses pre-trained weights)
3. Download `densenet121_adult_rsna.pth` from Colab Files sidebar
4. Place it in the `models/` folder

### Option 2: Download Pre-trained Models

If available, download from:
- [Google Drive Link](#) (coming soon)
- [Hugging Face](#) (coming soon)
- [GitHub Releases](https://github.com/yourusername/AI-XRay-Assistant/releases)

### Model File Structure

Your `models/` folder should look like this:

```
models/
├── README.md
├── densenet121_pneumonia.pth        # ~27MB (Pediatric)
└── densenet121_adult_rsna.pth       # ~30MB (Adult)
```

**Note**: You need at least ONE model to run the app. Both are optional but provide different capabilities.

---

## Troubleshooting

### Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
- Windows: Reinstall Python with "Add to PATH" checked
- Linux/macOS: Use `python3` instead of `python`

### Permission Denied (Linux/macOS)

**Error**: `Permission denied` when running `run_app.sh`

**Solution**:
```bash
chmod +x run_app.sh
```

### pip Install Fails

**Error**: `Failed building wheel for package`

**Solution 1** - Update pip and setuptools:
```bash
pip install --upgrade pip setuptools wheel
```

**Solution 2** - Install build dependencies (Linux):
```bash
sudo apt-get install python3-dev build-essential
```

### PyTorch Installation Issues

**Error**: PyTorch download is very slow or times out

**Solution** - Use a specific PyTorch index:

**CPU-only** (smaller download):
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**CUDA 11.8** (for NVIDIA GPU):
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Streamlit Port Already in Use

**Error**: `Port 8501 is already in use`

**Solution**:
```bash
streamlit run app.py --server.port 8502
```

### Model Not Found

**Error**: `Model file not found at models/densenet121_pneumonia.pth`

**Solution**:
- Make sure you've downloaded the model files (see [Downloading Model Weights](#downloading-model-weights))
- Check that files are in the correct location: `models/` folder
- Verify file names match exactly (case-sensitive on Linux/macOS)

### Import Error: No module named 'torchxrayvision'

**Error**: `ModuleNotFoundError: No module named 'torchxrayvision'`

**Solution**:
```bash
pip install torchxrayvision
```

### Out of Memory Error

**Error**: `RuntimeError: CUDA out of memory` or system freezes

**Solution**:
- Close other applications
- Use CPU inference (add `--server.maxUploadSize=10` to limit image size)
- Reduce image resolution before uploading

---

## Verification

### Test the Installation

1. **Activate virtual environment** (if using Method 2)
2. **Run the app**:
   ```bash
   streamlit run app.py
   ```
3. **Open browser** to `http://localhost:8501`
4. **Upload a test image** from `test_images/` folder
5. **Verify** you get prediction results

### Expected Output

You should see:
- ✅ Model loaded successfully
- ✅ Image uploaded and displayed
- ✅ Prediction results with confidence scores
- ✅ No error messages in terminal

### Check Installed Packages

```bash
pip list
```

Key packages to verify:
- `torch` (2.0.0+)
- `torchvision` (0.15.0+)
- `streamlit` (1.30.0+)
- `torchxrayvision` (latest)
- `Pillow` (10.0.0+)

---

## Additional Configuration

### GPU Acceleration (Optional)

If you have an NVIDIA GPU:

1. **Install CUDA Toolkit**: [nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
2. **Install cuDNN**: Follow NVIDIA's instructions
3. **Install PyTorch with CUDA**:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```
4. **Verify GPU is detected**:
   ```bash
   python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
   ```

### Streamlit Configuration

Create `.streamlit/config.toml` (if it doesn't exist):

```toml
[server]
port = 8501
headless = true
maxUploadSize = 10

[theme]
primaryColor = "#e94560"
backgroundColor = "#0f0f0f"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#ffffff"
font = "sans serif"
```

---

## Uninstallation

### Remove Virtual Environment

**Windows:**
```bash
deactivate
rmdir /s venv
```

**Linux/macOS:**
```bash
deactivate
rm -rf venv
```

### Remove All Files

```bash
cd ..
rm -rf AI-XRay-Assistant
```

---

## Next Steps

After successful installation:

1. **Read the Usage Guide**: [docs/USAGE.md](USAGE.md)
2. **Explore Training**: [docs/TRAINING.md](TRAINING.md)
3. **Try Deployment**: [docs/DEPLOYMENT.md](DEPLOYMENT.md)

---

## Getting Help

If you encounter issues not covered here:

1. **Check GitHub Issues**: [github.com/yourusername/AI-XRay-Assistant/issues](https://github.com/yourusername/AI-XRay-Assistant/issues)
2. **Create New Issue**: Include:
   - OS and Python version
   - Error message (full traceback)
   - Steps to reproduce
3. **Discussion Forum**: [GitHub Discussions](https://github.com/yourusername/AI-XRay-Assistant/discussions)

---

**Last Updated**: March 3, 2026  
**Installation Guide Version**: 1.0
