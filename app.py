"""
AI X-Ray Assistant — Streamlit Web Application
================================================
Automated Chest X-Ray Pneumonia Detection using DenseNet121.

Supports TWO models:
  - Pediatric Model: 3-class (Normal, Bacteria, Virus) — trained on pediatric X-rays
  - Adult Model: Binary (Normal vs Pneumonia) — pre-trained on RSNA adult X-rays

Author: Muhammad Saad Khan
License: MIT
"""

import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import os

import sys

# Constants
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    BASE_PATH = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

PEDIATRIC_MODEL_PATH = os.path.join(BASE_PATH, "models", "densenet121_pneumonia.pth")
ADULT_MODEL_PATH = os.path.join(BASE_PATH, "models", "densenet121_adult_rsna.pth")
PEDIATRIC_CLASSES = ["BACTERIA", "NORMAL", "VIRUS"]


@st.cache_resource
def load_pediatric_model():
    """Loads the pediatric 3-class PyTorch model."""
    try:
        if not os.path.exists(PEDIATRIC_MODEL_PATH):
            return None, f"Model file not found at {PEDIATRIC_MODEL_PATH}"

        model = models.densenet121(weights=None)
        num_ftrs = model.classifier.in_features
        model.classifier = nn.Linear(num_ftrs, 3)

        state_dict = torch.load(PEDIATRIC_MODEL_PATH, map_location=torch.device('cpu'))
        model.load_state_dict(state_dict)
        model.eval()
        return model, None
    except Exception as e:
        return None, str(e)


@st.cache_resource
def load_adult_model():
    """Loads the adult RSNA pre-trained model (TorchXRayVision format)."""
    try:
        if not os.path.exists(ADULT_MODEL_PATH):
            return None, None, f"Model file not found at {ADULT_MODEL_PATH}"

        checkpoint = torch.load(ADULT_MODEL_PATH, map_location=torch.device('cpu'))
        pathologies = checkpoint.get('pathologies', [])
        state_dict = checkpoint.get('model_state_dict', checkpoint)

        # Remove non-model keys if present
        state_dict = {k: v for k, v in state_dict.items() if k != 'op_threshs'}

        # Try TorchXRayVision first (best compatibility)
        try:
            import torchxrayvision as xrv
            model = xrv.models.DenseNet(weights=None)
            model.load_state_dict(state_dict)
        except ImportError:
            # Fallback: standard DenseNet121 modified for 1-channel grayscale input
            model = models.densenet121(weights=None)
            # Change first conv from 3-channel to 1-channel input
            old_conv = model.features.conv0
            model.features.conv0 = nn.Conv2d(
                1, old_conv.out_channels, kernel_size=old_conv.kernel_size,
                stride=old_conv.stride, padding=old_conv.padding, bias=False
            )
            # Change classifier to match pathology count
            num_ftrs = model.classifier.in_features
            model.classifier = nn.Linear(num_ftrs, len(pathologies))
            model.load_state_dict(state_dict)

        model.eval()
        return model, pathologies, None
    except Exception as e:
        return None, None, str(e)


def preprocess_pediatric(image):
    """Prepares image for pediatric model (RGB, ImageNet normalization)."""
    image = image.convert('RGB')
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)


def preprocess_adult(image):
    """Prepares image for adult model (Grayscale, XRV normalization)."""
    image = image.convert('L')  # Grayscale
    image = image.resize((224, 224))
    img_array = np.array(image, dtype=np.float32)

    # Normalize to [-1024, 1024] range (XRV convention)
    if img_array.max() > 0:
        img_array = (img_array - img_array.min()) / (img_array.max() - img_array.min())
        img_array = img_array * 2048.0 - 1024.0

    img_tensor = torch.from_numpy(img_array).unsqueeze(0).unsqueeze(0)
    return img_tensor


def run_pediatric_inference(model, input_tensor):
    """Runs inference on the pediatric 3-class model."""
    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        return probs.numpy()[0]


def run_adult_inference(model, input_tensor, pathologies):
    """Runs inference on the adult RSNA model."""
    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.sigmoid(outputs).numpy()[0]

        pneumonia_idx = pathologies.index("Pneumonia") if "Pneumonia" in pathologies else 0
        pneumonia_prob = probs[pneumonia_idx]
        normal_prob = 1.0 - pneumonia_prob

        return pneumonia_prob, normal_prob


# --- UI ---
st.set_page_config(page_title="AI X-Ray Assistant", layout="wide")
st.title("🩻 AI X-Ray Assistant")
st.markdown("### Automated Pneumonia Detection System")

# Check which models are available
has_pediatric = os.path.exists(PEDIATRIC_MODEL_PATH)
has_adult = os.path.exists(ADULT_MODEL_PATH)

if not has_pediatric and not has_adult:
    st.error("No model files found!")
    st.info(
        f"Please place one of these in the current directory:\n"
        f"- `{PEDIATRIC_MODEL_PATH}` (Pediatric model)\n"
        f"- `{ADULT_MODEL_PATH}` (Adult model)"
    )
else:
    # Model selection
    available_models = []
    if has_pediatric:
        available_models.append("🧒 Pediatric (Bacteria/Normal/Virus)")
    if has_adult:
        available_models.append("🧑 Adult (Pneumonia/Normal)")

    if len(available_models) > 1:
        selected = st.radio("Select Model:", available_models, horizontal=True)
    else:
        selected = available_models[0]

    use_adult = "Adult" in selected

    # Show model info
    if use_adult:
        st.markdown("Using **Adult Model** — Pre-trained on RSNA Pneumonia Challenge (adult X-rays)")
    else:
        st.markdown("Using **Pediatric Model** — Trained on pediatric X-rays (ages 1–5)")

    # File uploader
    uploaded_file = st.file_uploader("Choose an X-Ray Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)

        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded X-Ray", width="stretch")

        with col2:
            st.write("Analyzing...")

            if use_adult:
                # Adult model inference
                model, pathologies, error = load_adult_model()
                if error:
                    st.error(f"Error: {error}")
                else:
                    input_tensor = preprocess_adult(image)
                    pneumonia_prob, normal_prob = run_adult_inference(model, input_tensor, pathologies)

                    if pneumonia_prob > 0.5:
                        st.error(f"## Result: PNEUMONIA")
                    else:
                        st.success(f"## Result: NORMAL")

                    st.metric("Confidence", f"{max(pneumonia_prob, normal_prob):.2%}")

                    st.write("---")
                    st.write("### Detailed Probabilities:")
                    st.write(f"**NORMAL**: {normal_prob:.4f}")
                    st.write(f"**PNEUMONIA**: {pneumonia_prob:.4f}")

            else:
                # Pediatric model inference
                model, error = load_pediatric_model()
                if error:
                    st.error(f"Error: {error}")
                else:
                    input_tensor = preprocess_pediatric(image)
                    probs = run_pediatric_inference(model, input_tensor)

                    top_class_idx = np.argmax(probs)
                    top_class = PEDIATRIC_CLASSES[top_class_idx]
                    confidence = probs[top_class_idx]

                    if top_class == "NORMAL":
                        st.success(f"## Result: {top_class}")
                    else:
                        st.error(f"## Result: {top_class}")

                    st.metric("Confidence", f"{confidence:.2%}")

                    st.write("---")
                    st.write("### Detailed Probabilities:")
                    for i, cls in enumerate(PEDIATRIC_CLASSES):
                        st.write(f"**{cls}**: {probs[i]:.4f}")

# --- Sidebar ---
st.sidebar.title("About")
st.sidebar.info(
    "**AI X-Ray Assistant**\n\n"
    "Uses DenseNet121 models for pneumonia detection:\n\n"
    "🧒 **Pediatric:** Fine-tuned on pediatric X-rays "
    "(Bacteria/Normal/Virus)\n\n"
    "🧑 **Adult:** Pre-trained on RSNA Pneumonia Challenge "
    "(Pneumonia/Normal)\n\n"
    "**Tech Stack:** PyTorch · Streamlit · DenseNet121 · TorchXRayVision"
)
st.sidebar.warning(
    "⚠️ **Disclaimer**\n\n"
    "This tool is for **educational purposes only**. "
    "It is NOT a certified medical device. "
    "Always consult a qualified healthcare professional."
)
