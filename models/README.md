# Model Weights

This directory stores the trained model weights (`.pth` files).

**These files are NOT included in the repository** (too large for Git).

## How to Get the Models

### 🧒 Pediatric Model (`densenet121_pneumonia.pth`)
1. Open `notebooks/Colab_Model_training.ipynb` in Google Colab
2. Run all cells (requires GPU runtime)
3. Download the `.pth` file from the Colab Files sidebar
4. Place it in this `models/` directory

### 🧑 Adult Model (`densenet121_adult_rsna.pth`)
1. Open `notebooks/NIH_Adult_Training.ipynb` in Google Colab
2. Run all cells (no GPU needed — uses pre-trained weights)
3. Download the `.pth` file from the Colab Files sidebar
4. Place it in this `models/` directory
