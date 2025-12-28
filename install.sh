#!/bin/bash

# Tokopedia Voucher Claimer - Termux Installation Script
# Author: AI Assistant
# Version: 1.0

echo "🚀 Installing Tokopedia Voucher Claimer for Termux..."
echo "=================================================="

# Check if running on Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "❌ This script is designed for Termux environment"
    echo "   Please install Termux from F-Droid or GitHub"
    exit 1
fi

# Update packages
echo "📦 Updating Termux packages..."
pkg update -y && pkg upgrade -y

# Install required packages
echo "📦 Installing required packages..."
pkg install -y python python-pip git wget curl chromium

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment
echo "⚙️  Setting up environment..."
mkdir -p logs data

# Copy example config
if [ ! -f ".env" ]; then
    cp config/.env.example .env
    echo "📝 Created .env file - Please edit with your credentials"
fi

# Make scripts executable
chmod +x run.sh
chmod +x src/voucher_claimer.py

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your Tokopedia credentials"
echo "2. Run: ./run.sh"
echo ""
echo "🔧 For troubleshooting, check logs/ directory"
echo "📖 Read README.md for detailed instructions"
echo ""
echo "⚠️  Disclaimer: Use at your own risk"
echo "   This script is for educational purposes only"