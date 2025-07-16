#!/bin/bash

# RoboCup 2025 Raspberry Pi Program Installation Script

set -e  # Exit on any error

echo "=== RoboCup 2025 Raspberry Pi Program Installation ==="

# Check if we're on a Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "Warning: This script is designed for Raspberry Pi. Some features may not work on other systems."
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

echo "✓ Python version: $python_version"

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    git \
    rsync \
    python3-opencv \
    python3-numpy

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

# Initialize git submodules
echo "Initializing git submodules..."
git submodule update --init --recursive

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p bin
mkdir -p logs

# Set up environment
echo "Setting up environment..."
if [ -f .envrc ]; then
    echo "✓ .envrc file found"
else
    echo "Warning: .envrc file not found. You may need to set up environment variables manually."
fi

# Make scripts executable
echo "Making scripts executable..."
chmod +x fetch.sh send.sh install.sh

# Test imports
echo "Testing module imports..."
python3 -c "
import sys
try:
    import modules.uart
    import modules.log
    import modules.camera
    import modules.settings
    print('✓ All modules imported successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "1. Connect your cameras and UART devices"
echo "2. Configure camera parameters in modules/settings.py"
echo "3. Run the program: python3 main.py"
echo ""
echo "For more information, see README.md"