#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting TradeNote setup..."

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3 to continue."
    exit 1
fi

echo "Python 3 found."

# Backend setup
echo "Setting up backend..."

# Create a virtual environment
echo "Creating virtual environment in backend/venv..."
python3 -m venv backend/venv

# Activate the virtual environment and install dependencies
echo "Installing backend dependencies from requirements.txt..."
source backend/venv/bin/activate
pip install -r backend/requirements.txt

echo "Backend setup complete."

echo "----------------------------------------"
echo "Setup finished successfully!"
echo "To run the application, execute: ./tradenote.sh"
echo "----------------------------------------"
