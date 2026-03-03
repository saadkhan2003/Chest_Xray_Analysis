# Training Guide

Complete guide for training your own pneumonia detection models using Google Colab.

---

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Pediatric Model Training](#pediatric-model-training)
- [Adult Model Setup](#adult-model-setup)
- [Training from Scratch](#training-from-scratch)
- [Hyperparameter Tuning](#hyperparameter-tuning)
- [Evaluation and Metrics](#evaluation-and-metrics)
- [Model Export](#model-export)
- [Troubleshooting](#troubleshooting)

---

## Overview

This guide covers:
- ✅ Training the **Pediatric 3-class model** (Normal/Bacteria/Virus)
- ✅ Setting up the **Adult binary model** (Normal/Pneumonia)
- ✅ Custom dataset training
- ✅ Hyperparameter optimization
- ✅ Model evaluation and testing

### Why Google Colab?

- **Free GPU Access**: T4 GPU for faster training
- **No Local Setup**: Everything runs in the cloud
- **Easy Sharing**: Share notebooks with team
- **Pre-installed Libraries**: Most dependencies already available

---

## Prerequisites

### Required Materials

1. **Google Account** - For Google Colab access
2. **Kaggle Account** - For dataset download
3. **Kaggle API Key** (`kaggle.json`) - [How to get it](https://www.kaggle.com/docs/api)
4. **Basic Python Knowledge** - Understanding of ML concepts helpful

### Kaggle API Key Setup

1. Go to [Kaggle.com](https://www.kaggle.com/) and log in
2. Click on your profile picture → **Account**
3. Scroll to **API** section
4. Click **"Create New API Token"**
5. Download `kaggle.json` file
6. Keep this file safe (you'll upload it to Colab)

### Expected Time

- **Pediatric Model Training**: 2-3 hours (with GPU)
- **Adult Model Setup**: 5-10 minutes (pre-trained)
- **Custom Training**: Varies by dataset size

---

## Pediatric Model Training

This section covers training the 3-class pneumonia classifier on pediatric X-rays.

### Step 1: Open the Notebook

1. Navigate to [`notebooks/Colab_Model_training.ipynb`](../notebooks/Colab_Model_training.ipynb)
2. Click **"Open in Colab"** button (or upload to Google Colab)
3. Sign in to your Google Account

### Step 2: Enable GPU Runtime

1. Click **Runtime** → **Change runtime type**
2. Select **"T4 GPU"** or **"GPU"** from Hardware accelerator
3. Click **Save**

**Verify GPU is enabled:**
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
```

### Step 3: Upload Required Files

Upload to Colab Files sidebar (left panel):
1. **`kaggle.json`** - Your Kaggle API key
2. **`scripts/colab_data_setup.py`** - Dataset processing script

### Step 4: Run Setup Cells

Execute cells in order:

#### Cell 1: Install Dependencies
```python
!pip install kaggle albumentations pytorch-grad-cam
```

#### Cell 2: Setup Authentication
The notebook will:
- Find and configure your `kaggle.json`
- Set correct permissions
- Verify Kaggle API access

#### Cell 3: Download Dataset
```python
# Downloads ~6GB Pediatric Pneumonia Dataset
# Extracts to /content/chest_xray
```

Expected output:
```
⬇️ Downloading dataset...
✅ Dataset downloaded!
```

### Step 5: Data Processing

#### Patient-Level Splitting
```python
# Prevents data leakage by ensuring 
# no patient's X-rays appear in both train and test sets
```

The script will:
- Parse all X-ray images
- Extract patient IDs from filenames
- Split by patient (80% train, 10% val, 10% test)
- Organize into class folders

Output structure:
```
/content/processed_data/
├── train/
│   ├── BACTERIA/
│   ├── NORMAL/
│   └── VIRUS/
├── val/
│   └── ...
└── test/
    └── ...
```

### Step 6: Configure Training Parameters

Default hyperparameters:
```python
# Model
MODEL_NAME = "densenet121"
NUM_CLASSES = 3
PRETRAINED = True

# Training
BATCH_SIZE = 32
LEARNING_RATE = 0.0001
NUM_EPOCHS = 25
WEIGHT_DECAY = 1e-4

# Optimizer
OPTIMIZER = "Adam"

# Loss Function
CRITERION = "WeightedCrossEntropy"  # For class imbalance
```

**Recommended Modifications for Different Hardware:**

| GPU Memory | Batch Size | Expected Time |
|------------|------------|---------------|
| 16GB (T4)  | 32         | 2-3 hours     |
| 8GB        | 16         | 4-5 hours     |
| CPU only   | 8          | 20+ hours ❌   |

### Step 7: Train the Model

Run the training cell:
```python
# Trains for NUM_EPOCHS with:
# - Data augmentation (rotation, flip, brightness)
# - Weighted loss for class imbalance
# - Learning rate scheduling
# - Early stopping (optional)
# - Checkpoint saving
```

**Monitor Progress:**
- **Loss curves**: Should decrease over epochs
- **Accuracy**: Should increase to 85-90%
- **Validation metrics**: Watch for overfitting

Expected output per epoch:
```
Epoch 1/25
Train Loss: 0.8234 | Train Acc: 68.2%
Val Loss: 0.6543 | Val Acc: 73.5%
---
Epoch 2/25
Train Loss: 0.5432 | Train Acc: 78.1%
Val Loss: 0.5123 | Val Acc: 79.8%
...
```

### Step 8: Evaluate the Model

```python
# Runs inference on test set
# Generates confusion matrix
# Calculates per-class metrics
```

**Key Metrics:**

**Infection Sensitivity** (most important):
```python
# (True Positive Pneumonia) / (All Actual Pneumonia)
# Target: >95% (minimize false negatives)
```

**Per-Class Performance:**
- **Normal Accuracy**: How well it identifies healthy X-rays
- **Bacteria Recall**: % of bacterial pneumonia caught
- **Virus Recall**: % of viral pneumonia caught

**Confusion Matrix Example:**
```
              Pred       Pred       Pred
              Bacteria   Normal     Virus
Actual Bacteria   245        3        52
Actual Normal       0      162         8
Actual Virus       20        3       110
```

### Step 9: Visualize Results

The notebook includes:
1. **Training curves** (loss and accuracy)
2. **Confusion matrix** heatmap
3. **Sample predictions** with Grad-CAM heatmaps
4. **Error analysis** (misclassified examples)

### Step 10: Download the Model

```python
# Save model
torch.save(model.state_dict(), "densenet121_pneumonia.pth")

# Download from Colab Files sidebar:
# 1. Click folder icon (left panel)
# 2. Right-click densenet121_pneumonia.pth
# 3. Select "Download"
```

**File size**: ~27MB

**Move to project**: Place in `AI-XRay-Assistant/models/` folder

---

## Adult Model Setup

The adult model uses **pre-trained weights** from TorchXRayVision, requiring minimal setup.

### Step 1: Open the Notebook

1. Navigate to [`notebooks/NIH_Adult_Training.ipynb`](../notebooks/NIH_Adult_Training.ipynb)
2. Open in Google Colab

### Step 2: Install TorchXRayVision

```python
!pip install torchxrayvision
```

### Step 3: Load Pre-trained Model

```python
import torchxrayvision as xrv

# Load model pre-trained on RSNA adult X-rays
model = xrv.models.DenseNet(weights="densenet121-res224-rsna")

# The model is already trained on adult pneumonia detection
```

### Step 4: Extract Pneumonia Classifier

```python
# TorchXRayVision models predict multiple pathologies
# Extract just the pneumonia prediction weights

checkpoint = {
    'model_state_dict': model.state_dict(),
    'pathologies': model.pathologies,
    'op_threshs': model.op_threshs
}

torch.save(checkpoint, "densenet121_adult_rsna.pth")
```

### Step 5: Download and Deploy

1. Download `densenet121_adult_rsna.pth` from Colab
2. Place in `AI-XRay-Assistant/models/` folder
3. Model is ready to use!

**No training required** - the model is already optimized for adult pneumonia detection.

---

## Training from Scratch

Want to train on your own dataset? Follow these steps:

### Dataset Preparation

1. **Organize images** in this structure:
   ```
   my_dataset/
   ├── train/
   │   ├── class1/
   │   ├── class2/
   │   └── class3/
   ├── val/
   │   └── ...
   └── test/
       └── ...
   ```

2. **Image requirements**:
   - Format: JPEG or PNG
   - Resolution: 224x224 or higher
   - Grayscale or RGB (auto-converted)
   - Frontal chest X-rays only

3. **Minimum dataset size**:
   - **Per class**: 100+ images (500+ recommended)
   - **Total**: 300+ images (1500+ recommended)
   - **Validation**: 10-20% of training set
   - **Test**: 10-20% of training set

### Modify the Training Notebook

#### 1. Update Data Paths
```python
TRAIN_DIR = "/path/to/your/train"
VAL_DIR = "/path/to/your/val"
TEST_DIR = "/path/to/your/test"
```

#### 2. Define Classes
```python
CLASSES = ["Class1", "Class2", "Class3"]
NUM_CLASSES = len(CLASSES)
```

#### 3. Adjust Class Weights (if imbalanced)
```python
from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight(
    'balanced',
    classes=np.unique(train_labels),
    y=train_labels
)
```

#### 4. Configure Augmentation
```python
import albumentations as A

train_transform = A.Compose([
    A.Resize(224, 224),
    A.HorizontalFlip(p=0.5),
    A.Rotate(limit=10, p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.Normalize(mean=[0.485], std=[0.229]),
])
```

### Training Tips

**Start with small epochs:**
```python
NUM_EPOCHS = 5  # Quick test
```
Then increase after verifying training works.

**Monitor for overfitting:**
- If val_loss increases while train_loss decreases → overfitting
- Solutions:
  - Add dropout layers
  - Increase data augmentation
  - Use early stopping
  - Reduce model capacity

**Use learning rate scheduling:**
```python
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=3
)
```

---

## Hyperparameter Tuning

### Key Hyperparameters

#### Learning Rate
```python
LR = 0.0001  # Default

# Too high: Training unstable
# Too low: Training too slow
# Recommended range: 0.00001 to 0.001
```

#### Batch Size
```python
BATCH_SIZE = 32  # Default

# Larger: Faster training, more GPU memory
# Smaller: Better generalization, less memory
# Recommended: 16, 32, or 64
```

#### Optimizer
```python
# Adam (default): Good all-around choice
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# SGD with momentum: Sometimes better generalization
optimizer = torch.optim.SGD(model.parameters(), lr=LR, momentum=0.9)

# AdamW: Better weight decay handling
optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
```

#### Weight Decay
```python
WEIGHT_DECAY = 1e-4  # L2 regularization

# Prevents overfitting
# Range: 1e-5 to 1e-3
```

### Experimentation Strategy

1. **Baseline**: Train with default parameters
2. **Learning Rate**: Try [1e-5, 1e-4, 1e-3]
3. **Batch Size**: Try [16, 32, 64]
4. **Augmentation**: Add/remove transforms
5. **Architecture**: Try DenseNet-169 or ResNet-50

### Tracking Experiments

Use a simple log:
```python
experiments = {
    "exp1": {"lr": 0.0001, "bs": 32, "val_acc": 87.5},
    "exp2": {"lr": 0.001, "bs": 32, "val_acc": 85.2},
    "exp3": {"lr": 0.0001, "bs": 64, "val_acc": 88.1},
}
```

Or use [Weights & Biases](https://wandb.ai/) for automatic tracking.

---

## Evaluation and Metrics

### Classification Metrics

#### Accuracy
```python
accuracy = correct_predictions / total_predictions
```
Good for balanced datasets.

#### Sensitivity (Recall)
```python
sensitivity = true_positives / (true_positives + false_negatives)
```
**Most important for medical applications** - measures how many sick patients are caught.

#### Specificity
```python
specificity = true_negatives / (true_negatives + false_positives)
```
Measures how many healthy patients are correctly identified.

#### F1-Score
```python
f1 = 2 * (precision * recall) / (precision + recall)
```
Balanced metric between precision and recall.

### Medical-Specific Metrics

**Infection Sensitivity**:
```python
# For 3-class problem: How many pneumonia cases (bacteria + virus) are caught?
infection_sensitivity = (TP_bacteria + TP_virus) / (All_Bacteria + All_Virus)
```

**Target**: >95% for clinical safety

### Confusion Matrix Analysis

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
```

**Look for**:
- **High diagonal**: Good per-class accuracy
- **Off-diagonal errors**: Common confusions
- **False negatives**: Most critical errors

---

## Model Export

### PyTorch Format (.pth)

```python
# Save model state dict
torch.save(model.state_dict(), "model.pth")

# Save complete checkpoint (with optimizer, epoch, etc.)
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, "checkpoint.pth")
```

### ONNX Format (Optional)

For faster inference:
```python
import torch.onnx

dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    export_params=True,
    opset_version=11,
    input_names=['input'],
    output_names=['output']
)
```

---

## Troubleshooting

### Out of Memory Error

**Error**: `RuntimeError: CUDA out of memory`

**Solutions**:
1. Reduce batch size:
   ```python
   BATCH_SIZE = 16  # or 8
   ```
2. Enable gradient accumulation:
   ```python
   ACCUMULATION_STEPS = 2  # Effective batch size = 16 * 2 = 32
   ```
3. Use mixed precision training:
   ```python
   from torch.cuda.amp import autocast, GradScaler
   ```

### Training Not Converging

**Symptoms**: Loss not decreasing, accuracy stuck at random

**Solutions**:
1. Check data loading:
   ```python
   # Verify labels are correct
   print(train_dataset[0])
   ```
2. Reduce learning rate:
   ```python
   LR = 0.00001
   ```
3. Check loss function:
   ```python
   # Verify class weights are computed correctly
   print(class_weights)
   ```

### Overfitting

**Symptoms**: Train accuracy high, val accuracy low

**Solutions**:
1. Add dropout:
   ```python
   model.classifier = nn.Sequential(
       nn.Dropout(0.5),
       nn.Linear(num_ftrs, NUM_CLASSES)
   )
   ```
2. Increase augmentation
3. Get more data
4. Use early stopping

### Poor Performance on One Class

**Symptoms**: One class has very low recall

**Solutions**:
1. Check class balance
2. Increase class weight:
   ```python
   class_weights[poor_class_idx] *= 2
   ```
3. Collect more samples for that class
4. Review data quality for that class

---

## Advanced Topics

### Transfer Learning from Custom Weights

Start from your own pretrained model:
```python
# Load your pretrained model
pretrained_model = torch.load("my_pretrained.pth")

# Transfer weights
model.load_state_dict(pretrained_model, strict=False)

# Freeze early layers
for param in model.features[:8].parameters():
    param.requires_grad = False
```

### Multi-GPU Training

```python
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)
```

### Mixed Precision Training

Faster training with lower memory:
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for data, target in train_loader:
    optimizer.zero_grad()
    with autocast():
        output = model(data)
        loss = criterion(output, target)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

---

## Next Steps

After training your model:

1. **Evaluate thoroughly**: Test on diverse images
2. **Deploy**: Follow [Deployment Guide](DEPLOYMENT.md)
3. **Monitor**: Track performance in production
4. **Iterate**: Collect feedback and retrain

---

## Resources

### Papers
- [DenseNet](https://arxiv.org/abs/1608.06993) - Huang et al., 2017
- [TorchXRayVision](https://arxiv.org/abs/2111.00595) - Cohen et al., 2022

### Datasets
- [Pediatric Pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
- [NIH ChestX-ray14](https://www.kaggle.com/datasets/nih-chest-xrays/data)
- [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/)

### Tools
- [Google Colab](https://colab.research.google.com/)
- [Kaggle Notebooks](https://www.kaggle.com/code)
- [Weights & Biases](https://wandb.ai/)

---

**Last Updated**: March 3, 2026  
**Training Guide Version**: 1.0
