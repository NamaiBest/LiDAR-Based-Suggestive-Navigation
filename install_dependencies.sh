#!/bin/bash

# Installation script for LiDAR-Based Suggestive Navigation
# This script installs YDLidar SDK and required Python packages

set -e  # Exit on error

echo "=========================================="
echo "LiDAR-Based Suggestive Navigation Setup"
echo "=========================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Error: This script is designed for Linux systems"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Installing in: $SCRIPT_DIR"
echo ""

# Install system dependencies
echo "[1/5] Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y cmake pkg-config python3-dev swig git

# Install Python packages
echo ""
echo "[2/5] Installing Python packages..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    # On Raspbian Bookworm, use apt for system packages
    sudo apt-get install -y python3-matplotlib python3-numpy
fi

# Clone YDLidar SDK into a temporary location
echo ""
echo "[3/5] Downloading YDLidar SDK..."
TEMP_SDK_DIR="$SCRIPT_DIR/YDLidar-SDK"
if [ -d "$TEMP_SDK_DIR" ]; then
    echo "YDLidar-SDK directory already exists, using existing copy..."
else
    git clone https://github.com/YDLIDAR/YDLidar-SDK.git "$TEMP_SDK_DIR"
fi

# Build and install YDLidar SDK (installs to /usr/local/)
echo ""
echo "[4/5] Building and installing YDLidar SDK..."
cd "$TEMP_SDK_DIR"
mkdir -p build
cd build
cmake ..
make
sudo make install

echo ""
echo "YDLidar SDK installed to:"
echo "  - Libraries: /usr/local/lib/"
echo "  - Headers: /usr/local/include/"
echo "  - Python bindings: /usr/local/lib/python3/dist-packages/"

# Add user to dialout group for serial port access
echo ""
echo "[5/5] Configuring permissions..."
if ! groups | grep -q dialout; then
    echo "Adding user to dialout group..."
    sudo usermod -a -G dialout $USER
    echo "WARNING: You need to log out and log back in for group changes to take effect!"
else
    echo "User already in dialout group"
fi

# Ask if user wants to clean up SDK source
cd "$SCRIPT_DIR"
echo ""
read -p "Remove YDLidar-SDK source folder? (it's no longer needed after installation) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$TEMP_SDK_DIR"
    echo "YDLidar-SDK source removed."
else
    echo "YDLidar-SDK source kept in: $TEMP_SDK_DIR"
fi

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Connect your YDLidar X2 to a USB port"
echo "2. If you were added to dialout group, log out and log back in"
echo "3. Run: cd my_scripts && ./run.sh plot_tri_maxfreq.py"
echo ""
