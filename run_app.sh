#!/bin/bash
echo "=================================================="
echo "       AI X-Ray Assistant - Launcher"
echo "=================================================="
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "[INFO] Virtual environment not found. Setting up fresh environment..."
    echo ""

    # Check if Python is available
    if ! command -v py &> /dev/null && ! command -v python3 &> /dev/null; then
        echo "[ERROR] Python is not installed or not in PATH."
        echo "Please install Python from https://www.python.org/downloads/"
        exit 1
    fi

    # Determine python command
    if command -v py &> /dev/null; then
        PYTHON_CMD="py"
    else
        PYTHON_CMD="python3"
    fi

    # Create venv
    echo "[1/3] Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment."
        exit 1
    fi
    echo "      Done."

    # Activate
    echo "[2/3] Activating environment..."
    source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

    # Install requirements
    echo "[3/3] Installing dependencies (this may take a few minutes)..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies."
        exit 1
    fi

    echo ""
    echo "=================================================="
    echo "  Setup complete! Launching app..."
    echo "=================================================="
    echo ""
else
    echo "[INFO] Virtual environment found."
    source venv/Scripts/activate 2>/dev/null || source venv/bin/activate
fi

# Launch the app
echo "Starting Streamlit app..."
streamlit run app.py
