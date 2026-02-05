#!/bin/bash

# Streamlit Framework Template Setup Script
# This script automates the setup process

set -e  # Exit on error

echo "================================================"
echo "  Streamlit Framework Template Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate    (macOS/Linux)"
echo "  venv\\Scripts\\activate      (Windows)"
echo ""

# Install dependencies
read -p "Install dependencies now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Installing dependencies..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
    echo ""
fi

# Initialize database
read -p "Initialize database now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Initializing database..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    python scripts/init_db.py
    echo ""
fi

echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the app:"
echo "   streamlit run app.py"
echo ""
echo "3. Login with default credentials:"
echo "   Username: admin"
echo "   Password: changeme123"
echo ""
echo "4. Change the admin password immediately!"
echo ""
echo "For more information, see QUICKSTART.md"
echo "================================================"
