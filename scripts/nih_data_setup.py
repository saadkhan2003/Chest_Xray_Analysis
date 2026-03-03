"""
Adult X-Ray Model Setup — Using Pre-trained TorchXRayVision
============================================================
Uses the TorchXRayVision library which provides a DenseNet121 model
ALREADY pre-trained on the RSNA Pneumonia Detection Challenge dataset.

NO TRAINING NEEDED — just install and use!

The model outputs probabilities for 18 pathologies including Pneumonia.
We extract the Pneumonia probability for our binary classification.

Author: Muhammad Saad Khan
License: MIT
"""

import os
import sys


def setup_on_colab():
    """
    Installs TorchXRayVision and downloads the pre-trained model.
    Run this on Colab.
    """
    print("=" * 60)
    print("  Adult X-Ray Model — Pre-trained Setup")
    print("  (No training needed!)")
    print("=" * 60)

    # Install torchxrayvision
    print("\n⬇️  Installing TorchXRayVision...")
    os.system("pip install -q torchxrayvision")

    import torchxrayvision as xrv
    import torch

    # Load the pre-trained model (auto-downloads weights ~27MB)
    print("\n⬇️  Downloading pre-trained RSNA model weights...")
    model = xrv.models.DenseNet(weights="densenet121-res224-rsna")
    model.eval()

    print("\n✅ Model loaded successfully!")
    print(f"   Architecture: DenseNet121")
    print(f"   Trained on: RSNA Pneumonia Detection Challenge (adult X-rays)")
    print(f"   Output pathologies: {model.pathologies}")

    # Find the Pneumonia index
    pneumonia_idx = model.pathologies.index("Pneumonia") if "Pneumonia" in model.pathologies else None
    if pneumonia_idx is not None:
        print(f"   Pneumonia index: {pneumonia_idx}")
    else:
        print(f"   ⚠️ 'Pneumonia' not found in pathologies list")
        print(f"   Available: {model.pathologies}")

    # Save the state dict for use in app.py
    save_path = "/content/densenet121_adult_rsna.pth"
    torch.save({
        'model_state_dict': model.state_dict(),
        'pathologies': model.pathologies,
        'weights_name': 'densenet121-res224-rsna',
    }, save_path)
    print(f"\n💾 Model saved to: {save_path}")
    print("� Download this file from the Files sidebar")

    return model


def demo_inference(model=None):
    """
    Demo: Run inference on a sample image.
    """
    import torchxrayvision as xrv
    import torch
    import numpy as np
    from PIL import Image
    import skimage

    if model is None:
        model = xrv.models.DenseNet(weights="densenet121-res224-rsna")
        model.eval()

    # Create a synthetic test image (or load a real one)
    print("\n🔬 Running demo inference...")

    # The model expects 224x224 grayscale normalized to [-1024, 1024]
    # Use xrv.datasets.normalize to handle this
    dummy_img = torch.randn(1, 1, 224, 224)  # batch, channels, H, W
    with torch.no_grad():
        output = model(dummy_img)

    print(f"\n   Output shape: {output.shape}")
    print(f"   Pathologies and scores:")
    for i, path in enumerate(model.pathologies):
        score = output[0, i].item()
        marker = " ← THIS ONE" if path == "Pneumonia" else ""
        print(f"   [{i:2d}] {path:25s}: {score:.4f}{marker}")


if __name__ == "__main__":
    model = setup_on_colab()
    demo_inference(model)
