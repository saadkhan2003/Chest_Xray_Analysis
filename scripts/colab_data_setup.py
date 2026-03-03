"""
Colab Data Setup — Kaggle Dataset Download & Patient-Level Splitting
====================================================================
Downloads the Pediatric Pneumonia dataset from Kaggle, filters hidden/system
files, and splits data by patient ID to prevent data leakage.

Designed to run on Google Colab. Upload this file alongside kaggle.json.

Author: Muhammad Saad Khan
License: MIT
"""

import os
import shutil
import glob
from pathlib import Path

from sklearn.model_selection import train_test_split

# --- Configuration ---
DATASET_NAME = "paultimothymooney/chest-xray-pneumonia"  # Kaggle Dataset
BASE_DIR = Path("/content/chest_xray")
PROCESSED_DIR = Path("/content/processed_data")

def setup_kaggle_auth():
    """
    Finds kaggle.json in the current directory (even if named 'kaggle (2).json'),
    moves it to /root/.kaggle/, and sets permissions.
    """
    kaggle_dir = Path("/root/.kaggle")
    kaggle_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Look for any kaggle JSON file in /content
    candidates = list(Path("/content").glob("kaggle*.json"))
    
    if not candidates:
        print("❌ Error: No 'kaggle.json' found in /content.")
        print("   -> Please check the 'Files' sidebar to ensure you uploaded it.")
        return False
        
    # Pick the most likely file (if multiple, pick the first one)
    target_file = candidates[0]
    print(f"✅ Found credentials file: {target_file.name}")
    
    # 2. Move and Rename to /root/.kaggle/kaggle.json
    destination = kaggle_dir / "kaggle.json"
    shutil.copy(str(target_file), str(destination))
    
    # 3. Set Permissions (Required by Kaggle)
    os.chmod(destination, 0o600)
    print("✅ Moved to ~/.kaggle/kaggle.json and set permissions.")
    return True

def download_dataset():
    """Downloads dataset from Kaggle."""
    print("⬇️ Downloading dataset...")
    os.system(f"kaggle datasets download -d {DATASET_NAME} --unzip -p /content")
    
    # Check if download worked
    if not BASE_DIR.exists():
        print(f"❌ Error: Dataset not found at {BASE_DIR}. Download might have failed.")
        return False
    print("✅ Dataset downloaded!")
    return True

def organize_by_patient():
    """
    Re-organize dataset to prevent data leakage (Patient overlap).
    """
    print("🔄 Re-organizing dataset logic...")
    
    # Collect all image paths
    all_images = list(BASE_DIR.rglob("*.jpeg")) + list(BASE_DIR.rglob("*.jpg"))
    data = []
    
    for img_path in all_images:
        filename = img_path.name
        # Skip hidden/system files (Mac metadata)
        if filename.startswith(".") or "checkpoint" in filename:
            continue

        # Extract Label
        if "NORMAL" in str(img_path):
            label = "NORMAL"
        elif "PNEUMONIA" in str(img_path):
            if "bacteria" in filename:
                label = "BACTERIA"
            elif "virus" in filename:
                label = "VIRUS"
            else:
                label = "PNEUMONIA"
        
        # Extract Patient ID
        if "person" in filename:
            patient_id = filename.split("_")[0] 
        else:
            patient_id = filename.split(".")[0]
            
        data.append({"path": img_path, "label": label, "patient_id": patient_id})
        
    print(f"   -> Found {len(data)} images.")
    return data

def split_and_move(data):
    """Splits data by Patient ID and moves to new folders."""
    print("✂️ Splitting data (Train: 80%, Val: 10%, Test: 10%)...")
    
    # Group by Patient ID
    patient_map = {}
    for item in data:
        pid = item['patient_id']
        if pid not in patient_map:
            patient_map[pid] = []
        patient_map[pid].append(item)
        
    patient_ids = list(patient_map.keys())
    
    # Split
    train_ids, test_val_ids = train_test_split(patient_ids, test_size=0.2, random_state=42)
    val_ids, test_ids = train_test_split(test_val_ids, test_size=0.5, random_state=42)
    
    splits = {"train": train_ids, "val": val_ids, "test": test_ids}
    
    # Move files
    for split_name, pids in splits.items():
        for pid in pids:
            for item in patient_map[pid]:
                src = item['path']
                label = item['label']
                dest_dir = PROCESSED_DIR / split_name / label
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dest_dir / src.name)
                
    print("✅ Dataset organization complete!")
    print(f"   -> Data ready at {PROCESSED_DIR}")

if __name__ == "__main__":
    # 0. Install Kaggle
    os.system("pip install -q kaggle")
    
    # 1. Setup Auth
    if setup_kaggle_auth():
        # 2. Download
        if download_dataset():
            # 3. Process
            data = organize_by_patient()
            split_and_move(data)
