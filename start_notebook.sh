#!/bin/bash

# PyCon CO 2025 GIS Notebook Launcher
# This script sets up a Python virtual environment and launches the Marimo notebook

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_status "Working directory: $SCRIPT_DIR"

# Check if .venv already exists
if [ -d ".venv" ]; then
    print_warning "Virtual environment already exists at .venv"
    print_status "Skipping virtual environment creation"
else
    print_status "Creating Python virtual environment..."
    python3 -m venv .venv
    print_success "Virtual environment created successfully"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

print_success "Dependencies installed successfully"

# Check if required data files exist
print_status "Checking for required data files..."

MISSING_FILES=()

if [ ! -f "col_relative_wealth_index.csv" ]; then
    MISSING_FILES+=("col_relative_wealth_index.csv")
fi

if [ ! -f "col_ppp_2020_1km_Aggregated_UNadj.tif" ]; then
    MISSING_FILES+=("col_ppp_2020_1km_Aggregated_UNadj.tif")
fi

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    print_warning "The following data files are missing:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    print_warning "Some parts of the notebook may not work without these files."
    print_status "You can download them or the notebook will attempt to use remote data sources where available."
fi

# Launch Marimo notebook
print_status "Launching Marimo notebook..."
print_success "Starting PyCon CO 2025 GIS Notebook"
echo ""
echo "The notebook will open in your default web browser."
echo "To stop the notebook, press Ctrl+C in this terminal."
echo ""

# Run the marimo notebook
marimo run pycon_co.py
