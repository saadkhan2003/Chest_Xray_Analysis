"""
Model Optimization — PyTorch to ONNX + INT8 Quantization
=========================================================
Exports the trained DenseNet121 model to ONNX format and applies
dynamic INT8 quantization for fast CPU inference (~4x size reduction).

Usage:
    python src/optimize_model.py

Author: Muhammad Saad Khan
License: MIT
"""

import torch
import torch.onnx
import onnx

from onnxruntime.quantization import quantize_dynamic, QuantType
from torchvision import models
import torch.nn as nn
import os

def export_and_quantize(model_path, output_path="models/quantized_model.onnx"):
    """
    Exports a PyTorch DenseNet121 model to ONNX and quantizes it to INT8.
    """
    print(f"Loading model from {model_path}...")
    
    # 1. Recreate the model architecture
    # IMPORTANT: Must match the training architecture exactly
    model = models.densenet121(pretrained=False)
    num_ftrs = model.classifier.in_features
    model.classifier = nn.Linear(num_ftrs, 3) # Normal, Bacteria, Virus
    
    # Load weights
    try:
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    model.eval()
    
    # 2. Create dummy input for tracing (Batch Size 1, 3 Channels, 224x224)
    dummy_input = torch.randn(1, 3, 224, 224)
    
    # 3. Export to ONNX (FP32)
    onnx_path = "models/model_fp32.onnx"
    os.makedirs("models", exist_ok=True)
    
    print("Exporting to ONNX...")
    torch.onnx.export(model, 
                      dummy_input, 
                      onnx_path, 
                      opset_version=12, # Trying a slightly newer opset
                      input_names=['input'], 
                      output_names=['output'],
                      dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})
    
    print(f"FP32 Model saved to {onnx_path}")
    
    # 4. Quantize to INT8
    print("Quantizing to INT8...")
    quantize_dynamic(onnx_path,
                     output_path,
                     weight_type=QuantType.QUInt8)
    
    print(f"Quantized Model saved to {output_path}")
    
    # Compare sizes
    size_fp32 = os.path.getsize(onnx_path) / (1024 * 1024)
    size_int8 = os.path.getsize(output_path) / (1024 * 1024)
    print(f"FP32 Size: {size_fp32:.2f} MB")
    print(f"INT8 Size: {size_int8:.2f} MB")
    print(f"Reduction: {size_fp32 / size_int8:.2f}x")

if __name__ == "__main__":
    export_and_quantize("densenet121_pneumonia.pth")
