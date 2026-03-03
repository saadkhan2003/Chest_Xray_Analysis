#!/bin/bash
echo "=================================================="
echo "       AI X-Ray Assistant - Smart Launcher"
echo "=================================================="
echo ""

# ── Navigate to script directory ─────────────────────
cd "$(dirname "$0")"

# ── Find Python ──────────────────────────────────────
PYTHON_CMD=""

# Common candidate commands, in preference order
for cmd in python3.12 python3.11 python3.10 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON_CMD="$cmd"
        break
    fi
done

# Also check common non-PATH install locations
if [ -z "$PYTHON_CMD" ]; then
    for path in \
        "$HOME/.pyenv/shims/python3" \
        "/usr/local/bin/python3" \
        "/opt/homebrew/bin/python3" \
        "/usr/bin/python3"; do
        if [ -x "$path" ]; then
            PYTHON_CMD="$path"
            break
        fi
    done
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "[ERROR] Python not found on this system."
    echo "  Ubuntu/Debian : sudo apt install python3"
    echo "  Fedora/RHEL   : sudo dnf install python3"
    echo "  macOS         : brew install python or https://www.python.org/downloads/"
    exit 1
fi

PY_VER=$("$PYTHON_CMD" --version 2>&1)
echo "[INFO] Found: $PY_VER at $(command -v $PYTHON_CMD 2>/dev/null || echo $PYTHON_CMD)"

# ── Detect OS ────────────────────────────────────────
OS_TYPE="$(uname -s)"
case "$OS_TYPE" in
    Linux*)   OS_NAME="Linux" ;;
    Darwin*)  OS_NAME="macOS" ;;
    MINGW*|MSYS*|CYGWIN*) OS_NAME="Windows" ;;
    *)        OS_NAME="Unknown" ;;
esac
echo "[INFO] OS detected: $OS_NAME"

# ── Venv Setup ───────────────────────────────────────
if [ -f "venv/bin/python" ] || [ -f "venv/Scripts/python.exe" ]; then
    echo "[INFO] Existing virtual environment found. Reusing it."
else
    echo "[INFO] No virtual environment found. Creating one..."

    # On Debian/Ubuntu, python3-venv might be missing — give a clear hint
    if ! "$PYTHON_CMD" -m venv --help &>/dev/null; then
        echo "[WARN] The 'venv' module is missing."
        if [ "$OS_NAME" = "Linux" ]; then
            echo "  Try: sudo apt install python3-venv  (Debian/Ubuntu)"
            echo "       sudo dnf install python3       (Fedora/RHEL)"
        fi
        exit 1
    fi

    echo "[1/3] Creating virtual environment..."
    "$PYTHON_CMD" -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment."
        exit 1
    fi
    echo "       Done."
fi

# ── Activate ─────────────────────────────────────────
echo "[2/3] Activating environment..."
# Windows-style (Git Bash / Cygwin) or Unix-style
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

# ── Install / Update Dependencies ────────────────────
echo "[3/3] Installing / updating dependencies..."
pip install --upgrade pip -q
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

# ── Launch Streamlit ─────────────────────────────────
streamlit run app.py
