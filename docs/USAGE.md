# Usage Guide

Complete guide for using the AI X-Ray Assistant web application.

---

## Table of Contents
- [Starting the Application](#starting-the-application)
- [User Interface Overview](#user-interface-overview)
- [Selecting a Model](#selecting-a-model)
- [Uploading X-Ray Images](#uploading-x-ray-images)
- [Understanding Results](#understanding-results)
- [Using Test Images](#using-test-images)
- [Model Comparison](#model-comparison)
- [Best Practices](#best-practices)
- [Common Issues](#common-issues)

---

## Starting the Application

### Option 1: One-Click Launch

**Windows:**
- Double-click `run_app.bat` in File Explorer
- Wait for the browser window to open automatically

**Linux/macOS:**
```bash
chmod +x run_app.sh
./run_app.sh
```

### Option 2: Command Line

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Run the app
streamlit run app.py
```

### Option 3: Pre-built Executable

- Navigate to `dist/AI_XRay_Assistant/`
- Double-click `AI_XRay_Assistant.exe`
- Wait 30-60 seconds for the app to initialize

### Accessing the Interface

Once started, the app will be available at:
- **Local URL**: `http://localhost:8501`
- **Network URL**: `http://your-ip:8501` (for LAN access)

The browser should open automatically. If not, manually navigate to the local URL.

---

## User Interface Overview

The application interface consists of three main sections:

### 1. Header Section
- **Title**: "🩻 AI X-Ray Assistant"
- **Subtitle**: "Automated Pneumonia Detection System"
- **Model Selection**: Choose between Pediatric or Adult model

### 2. Main Content Area
- **Left Column**: Image upload and display
- **Right Column**: Analysis results and confidence scores

### 3. Sidebar
- **About Section**: Information about the models
- **Tech Stack**: Technologies used
- **Disclaimer**: Important usage warnings

---

## Selecting a Model

The application supports two different models optimized for different populations:

### 🧒 Pediatric Model (Ages 1-5)

**Use for:**
- Children aged 1-5 years
- Pediatric chest X-rays
- When you need 3-class classification

**Output Classes:**
1. **NORMAL** - No pneumonia detected
2. **BACTERIA** - Bacterial pneumonia
3. **VIRUS** - Viral pneumonia

**Dataset**: Kaggle Pediatric Pneumonia Dataset (Guangzhou Women and Children's Medical Center)

### 🧑 Adult Model

**Use for:**
- Adult patients (18+ years)
- General chest X-rays
- When you need binary classification

**Output Classes:**
1. **NORMAL** - No pneumonia detected
2. **PNEUMONIA** - Pneumonia present (type not specified)

**Dataset**: RSNA Pneumonia Detection Challenge (adult X-rays)

### How to Select

1. Look for the **radio button selector** at the top of the page
2. Click on your preferred model:
   - "🧒 Pediatric (Bacteria/Normal/Virus)"
   - "🧑 Adult (Pneumonia/Normal)"
3. The interface will update to show model-specific information

**Note**: If only one model is available, selection will be automatic.

---

## Uploading X-Ray Images

### Supported Formats
- ✅ **JPEG** (.jpg, .jpeg)
- ✅ **PNG** (.png)
- ❌ **DICOM** (.dcm) - Not yet supported

### Upload Methods

#### Method 1: Drag and Drop
1. Locate the **"Choose an X-Ray Image"** upload box
2. Drag an image file from your file manager
3. Drop it into the upload box
4. The image will automatically upload and display

#### Method 2: File Browser
1. Click the **"Browse files"** button in the upload box
2. Navigate to your image file in the file dialog
3. Select the image and click "Open"
4. The image will upload and display

### Image Requirements

**Recommended:**
- **Resolution**: 224x224 to 1024x1024 pixels
- **Format**: Grayscale or RGB (auto-converted)
- **Quality**: Clear, well-exposed X-ray
- **Orientation**: Frontal view (PA or AP)
- **File Size**: Under 10MB

**Things to Avoid:**
- ❌ Lateral (side) views
- ❌ Heavily cropped images
- ❌ Low resolution (<224px)
- ❌ Images with text overlays
- ❌ Rotated or skewed images
- ❌ Multiple X-rays in one image

---

## Understanding Results

### Result Display

After uploading an image, you'll see:

#### 1. Image Preview (Left Column)
- The uploaded X-ray image
- Caption: "Uploaded X-Ray"

#### 2. Analysis Status
- "Analyzing..." message while processing (usually <3 seconds)

#### 3. Primary Result (Right Column)

**Pediatric Model Result:**
```
## Result: BACTERIA
Confidence: 87.45%
```

**Adult Model Result:**
```
## Result: PNEUMONIA
Confidence: 92.18%
```

#### 4. Detailed Probabilities

**Pediatric Model Example:**
```
### Detailed Probabilities:
BACTERIA: 0.8745
NORMAL: 0.0523
VIRUS: 0.0732
```

**Adult Model Example:**
```
### Detailed Probabilities:
NORMAL: 0.0782
PNEUMONIA: 0.9218
```

### Interpreting Confidence Scores

| Confidence Range | Interpretation | Action |
|------------------|----------------|--------|
| **90-100%** | Very confident | Result is highly reliable |
| **70-90%** | Confident | Result is likely accurate |
| **50-70%** | Moderate confidence | Consider additional evaluation |
| **<50%** | Low confidence | Unreliable, requires review |

### Color Coding

- 🟢 **Green (Success)**: NORMAL result
- 🔴 **Red (Error/Warning)**: BACTERIA, VIRUS, or PNEUMONIA detected

---

## Using Test Images

The repository includes sample images for testing the application:

### Test Image Location

```
test_images/
├── Normal/               # Normal chest X-rays
│   ├── NORMAL-123.jpeg
│   ├── NORMAL-456.jpeg
│   └── ...
└── Bacteria_and_Virus/  # Pneumonia cases
    ├── bacteria-789.jpeg
    ├── virus-012.jpeg
    └── ...
```

### Testing Workflow

1. **Start the application**
2. **Select a model** (Pediatric or Adult)
3. **Upload a test image**:
   - Try a Normal image → expect "NORMAL" result
   - Try a Pneumonia image → expect "BACTERIA" or "VIRUS" result
4. **Compare results** with expected outcome
5. **Test multiple images** to see consistency

### Expected Results

**Normal Images:**
- Should predict "NORMAL" with high confidence (>80%)

**Pneumonia Images:**
- Pediatric Model: Should predict "BACTERIA" or "VIRUS"
- Adult Model: Should predict "PNEUMONIA"
- Confidence typically 70-95%

---

## Model Comparison

### When to Use Which Model

| Scenario | Recommended Model | Reason |
|----------|-------------------|--------|
| Pediatric patient (1-5 years) | 🧒 Pediatric | Trained on this population |
| Adult patient (18+ years) | 🧑 Adult | Better for adult anatomy |
| Need bacteria vs. virus distinction | 🧒 Pediatric | Only model with 3-class output |
| General screening | Either | Both perform well for detection |
| Unknown patient age | 🧑 Adult | More general-purpose |

### Performance Comparison

| Metric | Pediatric Model | Adult Model |
|--------|-----------------|-------------|
| **Sensitivity** | 98.6% | ~95% (estimated) |
| **Specificity** | ~95% | ~90% (estimated) |
| **Classes** | 3 (Normal/Bacteria/Virus) | 2 (Normal/Pneumonia) |
| **Training Data** | 5,000+ pediatric X-rays | 26,000+ adult X-rays |

### Complementary Use

For comprehensive analysis:
1. **Run both models** on the same image
2. **Compare results**:
   - Do they agree on Normal vs. Pneumonia?
   - Does pediatric model distinguish bacteria vs. virus?
3. **Use agreement** as a confidence indicator

---

## Best Practices

### Image Preparation

1. **Use High-Quality Images**
   - Original DICOM exports are best
   - Avoid screenshots of X-rays
   - Ensure good contrast

2. **Check Orientation**
   - Frontal view (PA or AP)
   - Patient facing forward
   - Lungs clearly visible

3. **Remove Annotations**
   - Strip identifying information (HIPAA compliance)
   - Remove text overlays if possible
   - Crop to just the chest area

### Workflow Recommendations

1. **Select Appropriate Model**
   - Match to patient age group
   - Consider clinical question

2. **Upload Image**
   - Use original quality when possible
   - Avoid multiple uploads simultaneously

3. **Review Results Carefully**
   - Check confidence scores
   - Look at all class probabilities
   - Consider clinical context

4. **Document Findings**
   - Screenshot results for records
   - Note confidence levels
   - Record any anomalies

### Safety Guidelines

⚠️ **Critical Reminders**:
- **Never** use as sole diagnostic tool
- **Always** have physician review
- **Not** intended for emergency decisions
- **Report** unusual predictions
- **Validate** with other diagnostic methods

---

## Common Issues

### Issue 1: Model Not Found

**Symptom**: Error message "Model file not found"

**Solution**:
1. Check that `.pth` files exist in `models/` folder
2. Verify file names match exactly:
   - `densenet121_pneumonia.pth` (Pediatric)
   - `densenet121_adult_rsna.pth` (Adult)
3. Download models if missing (see [Installation Guide](INSTALLATION.md))

### Issue 2: Upload Fails

**Symptom**: Image doesn't upload or shows error

**Solution**:
- Check file format (must be .jpg, .jpeg, or .png)
- Verify file size (<10MB)
- Try different image
- Check internet connection (if using remote server)

### Issue 3: Slow Inference

**Symptom**: Results take >10 seconds

**Solution**:
- Check CPU usage (close other programs)
- Reduce image resolution before upload
- Consider GPU acceleration (see Installation Guide)
- Restart the application

### Issue 4: Inconsistent Results

**Symptom**: Same image gives different results on re-upload

**Solution**:
- This is normal (minor variations in preprocessing)
- Differences should be small (<5% confidence)
- If large differences, check image quality
- Report persistent issues on GitHub

### Issue 5: App Won't Start

**Symptom**: Browser doesn't open or shows error

**Solution**:
1. Check terminal for error messages
2. Ensure port 8501 is available:
   ```bash
   streamlit run app.py --server.port 8502
   ```
3. Verify virtual environment is activated
4. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

### Issue 6: Low Confidence on All Images

**Symptom**: All predictions show <50% confidence

**Solution**:
- Verify model file integrity (re-download)
- Check that image quality is adequate
- Ensure using correct model for age group
- Try test images to establish baseline

---

## Advanced Usage

### Batch Processing (Coming Soon)

For processing multiple images:
1. Place all images in a folder
2. Use the Python API (see Development Guide)
3. Export results to CSV

### API Integration (Coming Soon)

REST API for programmatic access:
```python
import requests

response = requests.post(
    "http://localhost:8501/api/predict",
    files={"file": open("xray.jpg", "rb")},
    data={"model": "pediatric"}
)
print(response.json())
```

### Custom Preprocessing

For specialized images, you can modify preprocessing in `app.py`:
- Adjust normalization parameters
- Change resize dimensions
- Apply custom filters

See [Contributing Guide](CONTRIBUTING.md) for code modifications.

---

## Data Privacy

### Important Considerations

- ⚠️ **Do NOT upload** patient-identifiable information
- ✅ **Remove all metadata** from images
- ✅ **Strip DICOM headers** before upload
- ✅ **Use anonymized test data** only
- ⚠️ **Local deployment** is required for HIPAA compliance

### Compliant Workflow

1. **Anonymize images** using DICOM tools
2. **Run app locally** (not on shared servers)
3. **Delete uploaded images** after analysis
4. **Do not store** predictions with patient data

---

## Performance Tips

### For Fast Inference
- Use smaller images (resize to 512x512 before upload)
- Close unused browser tabs
- Run on dedicated machine
- Use GPU acceleration if available

### For Best Accuracy
- Use high-resolution original X-rays
- Ensure proper exposure (not over/underexposed)
- Upload frontal views only
- Use age-appropriate model

---

## Getting Help

If you need assistance:

1. **Check Documentation**:
   - [Installation Guide](INSTALLATION.md)
   - [Troubleshooting Section](#common-issues)
   - [FAQ](#) (coming soon)

2. **GitHub Resources**:
   - [Issues](https://github.com/yourusername/AI-XRay-Assistant/issues)
   - [Discussions](https://github.com/yourusername/AI-XRay-Assistant/discussions)

3. **Contact**:
   - Open a GitHub Issue with:
     - Screenshot of problem
     - Error messages
     - Steps to reproduce

---

## Next Steps

- **Train Your Own Model**: [Training Guide](TRAINING.md)
- **Deploy the App**: [Deployment Guide](DEPLOYMENT.md)
- **Contribute**: [Contributing Guide](CONTRIBUTING.md)

---

**Last Updated**: March 3, 2026  
**Usage Guide Version**: 1.0
