# Project Structure

```
chest-xray-ai/
│
├── app.py                    # Streamlit web app (main entry point)
├── requirements.txt          # Python dependencies
├── run_app.bat               # Windows launcher script
├── run_app.sh                # Linux/macOS launcher script
├── README.md                 # Project overview & setup guide
├── LICENSE                   # MIT License
├── .gitignore                # Git exclusion rules
│
├── .streamlit/
│   └── config.toml           # Streamlit configuration
│
├── models/
│   ├── README.md             # Instructions to download model weights
│   ├── densenet121_pneumonia.pth      # Pediatric model (gitignored)
│   └── densenet121_adult_rsna.pth     # Adult model (gitignored)
│
├── notebooks/
│   ├── Colab_Model_training.ipynb     # Pediatric model training (Colab)
│   └── NIH_Adult_Training.ipynb       # Adult model setup (Colab)
│
├── scripts/
│   ├── colab_data_setup.py   # Pediatric dataset download & splitting
│   └── nih_data_setup.py     # Adult model setup helper
│
├── docs/
│   ├── MODEL_CARD.md         # ML Model Card (architecture, metrics, limitations)
│   └── PROJECT_STRUCTURE.md  # This file
│
└── test_images/              # Sample X-ray images for testing
    ├── Bacteria_and_Virus/
    └── Normal/
```

## File Descriptions

### Root Files
| File | Purpose |
|---|---|
| `app.py` | Streamlit app with dual-model support (Pediatric + Adult) |
| `requirements.txt` | Pinned Python dependencies |
| `run_app.bat` / `run_app.sh` | One-click launcher scripts |

### `models/`
Pre-trained model weights. **Not in Git** — download via the Colab notebooks.

| Model | Classes | Data |
|---|---|---|
| `densenet121_pneumonia.pth` | Bacteria, Normal, Virus | Pediatric X-rays (ages 1–5) |
| `densenet121_adult_rsna.pth` | Pneumonia, Normal | RSNA adult X-rays |

### `notebooks/`
Google Colab notebooks for model training and setup.

### `scripts/`
Helper scripts used by the Colab notebooks to download and organize datasets.

### `docs/`
Project documentation including the ML Model Card.
