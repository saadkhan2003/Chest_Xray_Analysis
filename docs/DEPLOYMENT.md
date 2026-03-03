# Deployment Guide

Complete guide for deploying the AI X-Ray Assistant in various environments.

---

## Table of Contents
- [Deployment Overview](#deployment-overview)
- [Local Deployment](#local-deployment)
- [Standalone Executable](#standalone-executable)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [REST API Deployment](#rest-api-deployment)
- [Production Considerations](#production-considerations)
- [Security Best Practices](#security-best-practices)

---

## Deployment Overview

### Available Deployment Methods

| Method | Best For | Complexity | Setup Time |
|--------|----------|------------|------------|
| **Local Streamlit** | Development, demos | ⭐ Easy | 5 minutes |
| **Standalone Exe** | Non-technical users | ⭐ Easy | 15 minutes |
| **Docker** | Reproducible environments | ⭐⭐ Medium | 30 minutes |
| **Cloud (AWS/GCP)** | Production, scaling | ⭐⭐⭐ Hard | 1-2 hours |
| **REST API** | Integration with systems | ⭐⭐ Medium | 45 minutes |

### Deployment Decision Tree

```
Start
  ├─ Need to share with non-technical users?
  │   └─ Yes → Standalone Executable
  │
  ├─ Need system integration?
  │   └─ Yes → REST API Deployment
  │
  ├─ Need scalability & high availability?
  │   └─ Yes → Cloud Deployment (Docker + Load Balancer)
  │
  └─ Just for personal use/testing?
      └─ Yes → Local Streamlit
```

---

## Local Deployment

The simplest deployment method - running on your local machine.

### Quick Start

**All Platforms:**
```bash
# Clone repository
git clone https://github.com/yourusername/AI-XRay-Assistant.git
cd AI-XRay-Assistant

# Install dependencies
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Download models to models/ folder

# Run the app
streamlit run app.py
```

Access at: `http://localhost:8501`

### Custom Port Configuration

```bash
streamlit run app.py --server.port 8080
```

### Running in Background

**Linux/macOS:**
```bash
nohup streamlit run app.py > streamlit.log 2>&1 &
```

**Windows (PowerShell):**
```powershell
Start-Process streamlit -ArgumentList "run app.py" -WindowStyle Hidden
```

### Auto-Start on Boot

**Linux (systemd):**
Create `/etc/systemd/system/xray-assistant.service`:
```ini
[Unit]
Description=AI X-Ray Assistant
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/AI-XRay-Assistant
Environment="PATH=/path/to/AI-XRay-Assistant/venv/bin"
ExecStart=/path/to/AI-XRay-Assistant/venv/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable xray-assistant
sudo systemctl start xray-assistant
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At startup
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\streamlit.exe`
6. Arguments: `run app.py`
7. Start in: `C:\path\to\AI-XRay-Assistant`

### Local Network Access

To allow access from other devices on your network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Access from other devices: `http://your-ip:8501`

Find your IP:
- **Linux/macOS**: `ifconfig | grep "inet "`
- **Windows**: `ipconfig`

---

## Standalone Executable

Create a portable Windows executable that requires no installation.

### Building the Executable

```bash
# Ensure you're in the project root
cd AI-XRay-Assistant

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Install PyInstaller
pip install pyinstaller

# Run the build script
python build_exe.py
```

This will:
- Clean previous builds
- Create a new PyInstaller build
- Output to `dist/AI_XRay_Assistant/`

### Output Structure

```
dist/
└── AI_XRay_Assistant/
    ├── AI_XRay_Assistant.exe    # Main executable
    ├── app.py                     # Streamlit app
    ├── _internal/                 # Dependencies (auto-generated)
    └── .streamlit/                # Config files
```

### Adding Models

**Critical Step**: Copy model files to the executable folder:

```bash
# Windows
xcopy /E /I models dist\AI_XRay_Assistant\models

# Linux/macOS
cp -r models dist/AI_XRay_Assistant/models
```

### Distribution

1. **Compress the folder**:
   ```bash
   # Create AI_XRay_Assistant.zip containing the entire dist/AI_XRay_Assistant folder
   ```

2. **Share with users**:
   - Upload to Google Drive, Dropbox, etc.
   - Or create a GitHub Release

3. **User instructions**:
   - Extract ZIP file
   - Double-click `AI_XRay_Assistant.exe`
   - Wait 30-60 seconds for app to launch
   - Browser opens automatically

### Troubleshooting Executable

**Issue: Slow startup**
- Solution: Normal on first run (loads dependencies)
- Subsequent launches are faster

**Issue: Antivirus flags the .exe**
- Solution: Code signing certificate (requires purchase)
- Or: Add exception in antivirus software

**Issue: Missing dependencies**
- Solution: Rebuild with all hidden imports:
  ```python
  # In build_exe.py, add to hidden imports:
  '--hidden-import=missing_module_name'
  ```

---

## Docker Deployment

Containerize the application for reproducible deployment across environments.

### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY models/ ./models/
COPY .streamlit/ ./.streamlit/

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create .dockerignore

Create `.dockerignore` to exclude unnecessary files:

```
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.git/
.gitignore
.vscode/
notebooks/
test_images/
build/
dist/
*.spec
*.log
```

### Build Docker Image

```bash
# Build the image
docker build -t ai-xray-assistant:latest .

# Check image size
docker images ai-xray-assistant
```

Expected size: ~2-3GB (includes PyTorch)

### Run Docker Container

```bash
# Run in foreground (for testing)
docker run -p 8501:8501 ai-xray-assistant:latest

# Run in background (daemon mode)
docker run -d \
  --name xray-assistant \
  -p 8501:8501 \
  --restart unless-stopped \
  ai-xray-assistant:latest

# View logs
docker logs -f xray-assistant

# Stop container
docker stop xray-assistant

# Remove container
docker rm xray-assistant
```

### Docker Compose

Create `docker-compose.yml` for easier management:

```yaml
version: '3.8'

services:
  xray-assistant:
    build: .
    container_name: ai-xray-assistant
    ports:
      - "8501:8501"
    volumes:
      - ./models:/app/models:ro
      - ./uploads:/app/uploads
    environment:
      - STREAMLIT_SERVER_MAX_UPLOAD_SIZE=10
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Run with:
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Push to Docker Hub

```bash
# Tag image
docker tag ai-xray-assistant:latest yourusername/ai-xray-assistant:latest

# Login to Docker Hub
docker login

# Push image
docker push yourusername/ai-xray-assistant:latest
```

---

## Cloud Deployment

Deploy to cloud platforms for production use.

### AWS Deployment (EC2)

#### 1. Launch EC2 Instance

- **Instance Type**: t3.medium (minimum), g4dn.xlarge (with GPU)
- **OS**: Ubuntu 22.04 LTS
- **Storage**: 20GB minimum
- **Security Group**: Allow inbound on port 8501

#### 2. Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.10 python3.10-venv python3-pip -y

# Clone repository
git clone https://github.com/yourusername/AI-XRay-Assistant.git
cd AI-XRay-Assistant

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download models
# ... (from S3 or direct download)
```

#### 3. Run with Screen

```bash
# Install screen
sudo apt install screen -y

# Start screen session
screen -S xray-app

# Run app
streamlit run app.py --server.address 0.0.0.0

# Detach: Ctrl+A, then D
# Reattach: screen -r xray-app
```

#### 4. Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install nginx -y

# Create config
sudo nano /etc/nginx/sites-available/xray-assistant
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
        proxy_buffering off;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/xray-assistant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Google Cloud Platform (GCP)

#### Using Cloud Run (Serverless)

1. **Build and push Docker image**:
   ```bash
   # Authenticate
   gcloud auth login
   gcloud config set project your-project-id

   # Build image
   gcloud builds submit --tag gcr.io/your-project-id/ai-xray-assistant

   # Deploy to Cloud Run
   gcloud run deploy ai-xray-assistant \
     --image gcr.io/your-project-id/ai-xray-assistant \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --memory 2Gi \
     --cpu 2 \
     --timeout 300
   ```

2. **Access the service**:
   - GCP provides a URL: `https://ai-xray-assistant-xxx.run.app`

### Azure Deployment

#### Using Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name xray-assistant-rg --location eastus

# Create container instance
az container create \
  --resource-group xray-assistant-rg \
  --name ai-xray-assistant \
  --image yourusername/ai-xray-assistant:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8501 \
  --dns-name-label xray-assistant \
  --restart-policy Always

# Get URL
az container show \
  --resource-group xray-assistant-rg \
  --name ai-xray-assistant \
  --query ipAddress.fqdn
```

Access at: `http://xray-assistant.eastus.azurecontainer.io:8501`

---

## REST API Deployment

Convert the Streamlit app to a REST API for system integration.

### Create FastAPI Wrapper

Create `api.py`:

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import numpy as np

app = FastAPI(title="AI X-Ray Assistant API")

# Load models (same logic as app.py)
pediatric_model = None  # Load your model here
adult_model = None

@app.get("/")
def read_root():
    return {
        "service": "AI X-Ray Assistant API",
        "version": "1.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict/pediatric")
async def predict_pediatric(file: UploadFile = File(...)):
    """Predict using pediatric model"""
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess
        # ... (use preprocessing from app.py)
        
        # Inference
        with torch.no_grad():
            outputs = pediatric_model(input_tensor)
            probs = torch.nn.functional.softmax(outputs, dim=1)
        
        # Format response
        return {
            "prediction": {
                "BACTERIA": float(probs[0][0]),
                "NORMAL": float(probs[0][1]),
                "VIRUS": float(probs[0][2])
            },
            "top_class": ["BACTERIA", "NORMAL", "VIRUS"][torch.argmax(probs).item()],
            "confidence": float(torch.max(probs))
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/adult")
async def predict_adult(file: UploadFile = File(...)):
    """Predict using adult model"""
    # Similar implementation
    pass
```

### Run API Locally

```bash
# Install FastAPI and Uvicorn
pip install fastapi uvicorn python-multipart

# Run the API
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Access:
- **Docs**: `http://localhost:8000/docs`
- **Redoc**: `http://localhost:8000/redoc`

### Example API Usage

```python
import requests

# Upload image
with open("xray.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/predict/pediatric",
        files={"file": f}
    )

print(response.json())
# {
#   "prediction": {
#     "BACTERIA": 0.8745,
#     "NORMAL": 0.0523,
#     "VIRUS": 0.0732
#   },
#   "top_class": "BACTERIA",
#   "confidence": 0.8745
# }
```

### Deploy API with Docker

Create `Dockerfile.api`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install fastapi uvicorn python-multipart

COPY api.py .
COPY models/ ./models/

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -f Dockerfile.api -t xray-api:latest .
docker run -p 8000:8000 xray-api:latest
```

---

## Production Considerations

### Performance Optimization

1. **Model Optimization**:
   - Use ONNX format for faster inference
   - Quantize models (INT8) for smaller size
   - Enable GPU acceleration

2. **Caching**:
   ```python
   @st.cache_resource
   def load_model():
       # Model loads once and is cached
       pass
   ```

3. **Batch Processing**:
   - Process multiple images in one batch
   - Reduces overhead

### Monitoring

1. **Application Logs**:
   ```python
   import logging
   
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   logger.info(f"Prediction: {result}")
   ```

2. **Metrics**:
   - Track inference time
   - Monitor CPU/GPU usage
   - Log prediction distribution

3. **Error Tracking**:
   - Use Sentry or similar services
   - Alert on failures

### Scaling

1. **Horizontal Scaling**:
   - Deploy multiple containers
   - Use load balancer (Nginx, AWS ALB)

2. **Vertical Scaling**:
   - Increase instance size
   - Add GPU for faster inference

### Backup and Recovery

1. **Model Versioning**:
   - Keep multiple model versions
   - Easy rollback if issues

2. **Data Backup**:
   - Backup model files to S3/Cloud Storage
   - Regular automated backups

---

## Security Best Practices

### 1. Authentication

Add basic auth to Streamlit:

Create `.streamlit/secrets.toml`:
```toml
[passwords]
username = "admin"
password = "your-secure-password"
```

In `app.py`:
```python
import streamlit as st
import hmac

def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        if st.button("Login"):
            if (st.session_state["username"] == st.secrets["passwords"]["username"] and
                hmac.compare_digest(st.session_state["password"], 
                                   st.secrets["passwords"]["password"])):
                st.session_state["password_correct"] = True
                del st.session_state["password"]
                st.rerun()
            else:
                st.error("Incorrect username or password")
        return False
    return True

if not check_password():
    st.stop()

# Rest of your app
```

### 2. HTTPS/SSL

- Always use HTTPS in production
- Use Let's Encrypt for free SSL certificates
- Configure Nginx/Apache as reverse proxy with SSL

### 3. File Upload Security

```python
# Validate file type
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

def validate_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type")
    
    # Check file size
    if file.size > 10 * 1024 * 1024:  # 10MB
        raise ValueError("File too large")
```

### 4. Data Privacy

- Don't log patient data
- Delete uploaded files after processing
- Comply with HIPAA/GDPR if handling real patient data

### 5. Rate Limiting

Prevent abuse with rate limiting:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/predict")
@limiter.limit("10/minute")
async def predict(file: UploadFile):
    # ... prediction logic
```

---

## Cost Estimation

### Cloud Hosting Costs (Monthly)

| Platform | Instance Type | Cost | Use Case |
|----------|---------------|------|----------|
| **AWS EC2** | t3.medium | ~$30 | Basic deployment |
| **AWS EC2** | g4dn.xlarge (GPU) | ~$200 | High performance |
| **GCP Cloud Run** | 2 vCPU, 2GB | ~$10-50 | Low to medium traffic |
| **Azure Container** | 2 vCPU, 4GB | ~$40 | Medium traffic |
| **Digital Ocean** | Basic Droplet | ~$12 | Small deployments |

### Cost Optimization

- Use **spot instances** for non-critical workloads (70% cost savings)
- **Auto-scaling**: Scale down during low traffic
- **Serverless**: Only pay for actual usage (Cloud Run, Lambda)

---

## Next Steps

After deployment:

1. **Monitor Performance**: Set up logging and metrics
2. **Gather Feedback**: Collect user feedback
3. **Iterate**: Update models based on feedback
4. **Scale**: Adjust resources based on usage

---

## Support

For deployment issues:
- **GitHub Issues**: [Report a problem](https://github.com/yourusername/AI-XRay-Assistant/issues)
- **Documentation**: Check other guides in `docs/`

---

**Last Updated**: March 3, 2026  
**Deployment Guide Version**: 1.0
