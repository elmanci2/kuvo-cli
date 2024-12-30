#!/bin/bash

# Git repository URL
REPO_URL="https://github.com/elmanci2/kuvo-cli.git"

# Temporary directory to clone the repository
TEMP_DIR=$(mktemp -d)

# Logo
logo="██╗░░██╗██╗░░░██╗██╗░░░██╗░█████╗░\n██║░██╔╝██║░░░██║██║░░░██║██╔══██╗\n█████═╝░██║░░░██║╚██╗░██╔╝██║░░██║\n██╔═██╗░██║░░░██║░╚████╔╝░██║░░██║\n██║░╚██╗╚██████╔╝░░╚██╔╝░░╚█████╔╝\n╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░╚════╝░"

# Print the logo
echo -e "\n \n \n"
echo -e "$logo"
echo -e "\n \n \n"
echo -e "\nInstalling kuvo-cli..."
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

# Install the package with --break-system-packages
if command -v pip3 &> /dev/null
then
    pip3 install . --break-system-packages --user
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

# Determine the shell and update the PATH
SHELL=$(basename "$SHELL")
INSTALL_PATH="$HOME/Library/Python/3.13/bin"
EXPORT_LINE="export PATH=\"$INSTALL_PATH:\$PATH\""

if [ "$SHELL" = "zsh" ]; then
    RC_FILE="$HOME/.zshrc"
elif [ "$SHELL" = "bash" ]; then
    RC_FILE="$HOME/.bashrc"
else
    echo "Unsupported shell. Please manually add '$INSTALL_PATH' to your PATH."
    exit 1
fi

# Check if the line already exists
if ! grep -Fxq "$EXPORT_LINE" $RC_FILE; then
    echo "$EXPORT_LINE" >> $RC_FILE
    source $RC_FILE
    echo "PATH updated in $RC_FILE"
else
    echo "PATH already updated in $RC_FILE"
fi

# Clean up the temporary directory
rm -rf $TEMP_DIR

echo "Installation completed."
