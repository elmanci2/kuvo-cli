#!/bin/bash

# Git repository URL
REPO_URL="https://github.com/elmanci2/kuvo-cli.git"

# Temporary directory to clone the repository
TEMP_DIR=$(mktemp -d)

# Check if Python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
else
    echo "Python3 is installed."
fi

# Clone the repository
git clone $REPO_URL $TEMP_DIR
cd $TEMP_DIR

if [ $? -ne 0 ]; then
    echo "Failed to clone the repository."
    exit 1
fi

# Install dependencies
if command -v pip3 &> /dev/null
then
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "Dependencies installed successfully with pip3."
    else
        echo "Failed to install dependencies with pip3."
        exit 1
    fi
else
    echo "pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install the package with --break-system-packages
if command -v pip3 &> /dev/null
then
    pip3 install . --break-system-packages
    if [ $? -eq 0 ]; then
        echo "Package installed successfully with pip3."
    else
        echo "Failed to install the package with pip3."
        exit 1
    fi
else
    echo "pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Clean up the temporary directory
rm -rf $TEMP_DIR

echo "Installation completed."
