#!/bin/bash

# Git repository URL
REPO_URL="https://github.com/tu_usuario/tu_repositorio.git"

# Temporary directory to clone the repository
TEMP_DIR=$(mktemp -d)

# Check if Python is installed
if ! command -v python &> /dev/null
then
    echo "Python is not installed. Please install Python first."
    exit 1
fi

# Clone the repository excluding the venv folder
git clone --depth 1 --no-checkout $REPO_URL $TEMP_DIR
cd $TEMP_DIR
git sparse-checkout init --cone
git sparse-checkout set app install.sh requirements.txt setup.py

if [ $? -ne 0 ]; then
    echo "Failed to clone the repository."
    exit 1
fi

# Install dependencies
if command -v pip &> /dev/null
then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "Dependencies installed successfully with pip."
    else
        echo "Failed to install dependencies with pip."
        exit 1
    fi
else
    echo "pip is not installed. Please install pip first."
    exit 1
fi

# Install the package
if command -v pip &> /dev/null
then
    pip install .
    if [ $? -eq 0 ]; then
        echo "Package installed successfully with pip."
    else
        echo "Failed to install the package with pip."
        exit 1
    fi
else
    echo "pip is not installed. Please install pip first."
    exit 1
fi

# Clean up the temporary directory
rm -rf $TEMP_DIR

echo "Installation completed."
