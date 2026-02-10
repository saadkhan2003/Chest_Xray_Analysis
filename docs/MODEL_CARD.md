# Model Card — DenseNet121 Pneumonia Classifier

## Model Details

| Field | Value |
|---|---|
| **Model Name** | DenseNet121 Chest X-Ray Classifier |
| **Architecture** | DenseNet-121 (Huang et al., 2017) |
| **Framework** | PyTorch / TorchVision |
| **Pre-training** | ImageNet-1K |
| **Fine-tuning** | Kaggle Pediatric Pneumonia Dataset |
| **Output Classes** | 3 (Bacteria, Normal, Virus) |
| **Input Size** | 224 × 224 × 3 (RGB) |
| **Parameters** | ~7M |
| **File Size** | ~27 MB (.pth) |

---

## Intended Use

- **Primary Use:** Educational tool for understanding AI-assisted medical imaging
- **Target Users:** Students, researchers, and ML practitioners
- **Out-of-Scope:** Clinical diagnosis, patient treatment decisions, regulatory submissions

---

## Training Data

| Property | Detail |
|---|---|
| **Dataset** | [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) |
| **Source** | Guangzhou Women and Children's Medical Center |
| **Population** | Pediatric patients (ages 1–5) |
| **Split Method** | Patient-level (80% train / 10% val / 10% test) |
| **Augmentation** | Random horizontal flip, rotation (±10°), brightness/contrast jitter |

### Class Distribution (approximate)

| Class | Count | Percentage |
|---|---|---|
| Bacteria | ~2,500 | ~50% |
| Normal | ~1,300 | ~26% |
| Virus | ~1,200 | ~24% |

> **Note:** Class imbalance is addressed using Weighted Cross-Entropy Loss.

---

## Performance Metrics

Evaluated on the held-out test set (patient-level split):

| Metric | Value |
|---|---|
| **Infection Sensitivity** | 98.6% (only 6/433 sick patients missed) |
| **Normal Accuracy** | 95.3% (162/170) |

### Confusion Matrix Summary

| | Pred: Bacteria | Pred: Normal | Pred: Virus |
|---|---|---|---|
| **Actual Bacteria** | 245 | 3 | 52 |
| **Actual Normal** | 0 | 162 | 8 |
| **Actual Virus** | 20 | 3 | 110 |

### Key Observations
- **Strength:** Near-zero false negatives for pneumonia detection (high recall)
- **Weakness:** Bacteria vs. Virus confusion (52 Bacteria predicted as Virus), which is expected since radiological features overlap significantly
- **Clinical Safety:** The model is biased toward detecting disease, minimizing the risk of sending sick patients home

---

## Explainability

**Grad-CAM** heatmaps confirm the model focuses on:
- Lung parenchyma (the tissue where pneumonia manifests)
- Areas of consolidation and opacification

The model does **not** attend to:
- Image borders, text labels, or bone structures
- This indicates the model has learned medically relevant features

---

## Limitations

1. **Pediatric Only:** Trained exclusively on pediatric X-rays (ages 1–5). While the underlying radiological features of pneumonia (consolidation, opacities) are similar across age groups, the model has **not been validated on adult data**. A separate adult model using the NIH ChestX-ray14 dataset is available (see Future Work below).
2. **Single Dataset:** No external validation on other hospital datasets
3. **Binary Subtypes:** Only distinguishes Bacterial vs. Viral — does not identify specific organisms
4. **Image Quality:** Performance may degrade on low-resolution, rotated, or cropped images
5. **Not FDA Approved:** This is a research tool, not a medical device

---

## Future Work — Adult Model (NIH ChestX-ray14)

To address Limitation #1, a second model has been developed using the [NIH ChestX-ray14](https://www.kaggle.com/datasets/nih-chest-xrays/data) adult dataset:

| Property | Pediatric Model | Adult Model |
|---|---|---|
| **Dataset** | Kaggle Pediatric Pneumonia | NIH ChestX-ray14 |
| **Population** | Ages 1–5 | Adult patients |
| **Classes** | 3 (Bacteria, Normal, Virus) | 2 (Pneumonia, Normal) |
| **Model File** | `densenet121_pneumonia.pth` | `densenet121_nih_pneumonia.pth` |
| **Notebook** | `Colab_Model_training.ipynb` | `NIH_Adult_Training.ipynb` |

> **Note:** The NIH dataset does not distinguish between Bacterial and Viral pneumonia, so the adult model is a binary classifier (Pneumonia vs Normal).

---

## Ethical Considerations

- The model should **never** be the sole basis for clinical decisions
- False negatives (missed pneumonia) could have serious consequences in real settings
- The dataset represents a single geographic population; bias against other demographics is possible
- Any deployment in clinical settings would require extensive validation and regulatory approval
