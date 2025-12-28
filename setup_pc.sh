#!/bin/bash

# Tokopedia Voucher Claimer - PC Setup Script
# Automated installation for macOS and Linux

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
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

# Banner
print_banner() {
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║       TOKOPEDIA VOUCHER CLAIMER - PC SETUP               ║"
    echo "║              macOS & Linux Installer                      ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        INSTALL_CMD="brew install"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        # Detect distribution
        if command -v apt-get &> /dev/null; then
            INSTALL_CMD="sudo apt-get install -y"
        elif command -v dnf &> /dev/null; then
            INSTALL_CMD="sudo dnf install -y"
        elif command -v yum &> /dev/null; then
            INSTALL_CMD="sudo yum install -y"
        else
            print_error "Unsupported Linux distribution"
            exit 1
        fi
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    
    print_success "Detected OS: $OS"
}

# Check Python installation
check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python found: $PYTHON_VERSION"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version | cut -d' ' -f2)
        print_success "Python found: $PYTHON_VERSION"
        PYTHON_CMD="python"
    else
        print_error "Python not found!"
        echo ""
        echo "Please install Python 3.7+:"
        if [[ "$OS" == "macos" ]]; then
            echo "  brew install python3"
        elif [[ "$OS" == "linux" ]]; then
            echo "  sudo apt-get install python3 python3-pip"
        fi
        exit 1
    fi
}

# Check pip
check_pip() {
    print_status "Checking pip..."
    
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
        print_success "pip3 found"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
        print_success "pip found"
    else
        print_error "pip not found!"
        echo ""
        echo "Please install pip:"
        if [[ "$OS" == "macos" ]]; then
            echo "  brew install python3"
        elif [[ "$OS" == "linux" ]]; then
            echo "  sudo apt-get install python3-pip"
        fi
        exit 1
    fi
}

# Check browsers
check_browsers() {
    print_status "Checking installed browsers..."
    
    # Check if platform_utils.py exists and run it
    if [[ -f "src/platform_utils.py" ]]; then
        $PYTHON_CMD src/platform_utils.py
    fi
    
    # Try to detect browsers manually
    browsers_found=()
    
    if [[ "$OS" == "macos" ]]; then
        if command -v /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome &> /dev/null || \
           command -v google-chrome &> /dev/null; then
            browsers_found+=("Chrome")
        fi
        
        if command -v /Applications/Firefox.app/Contents/MacOS/firefox &> /dev/null || \
           command -v firefox &> /dev/null; then
            browsers_found+=("Firefox")
        fi
        
        if command -v /Applications/Safari.app/Contents/MacOS/Safari &> /dev/null; then
            browsers_found+=("Safari")
        fi
        
    elif [[ "$OS" == "linux" ]]; then
        if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
            browsers_found+=("Chrome/Chromium")
        fi
        
        if command -v firefox &> /dev/null; then
            browsers_found+=("Firefox")
        fi
    fi
    
    if [[ ${#browsers_found[@]} -gt 0 ]]; then
        print_success "Found browsers: ${browsers_found[*]}"
    else
        print_warning "No compatible browsers found"
        echo ""
        echo "Please install one of the following browsers:"
        if [[ "$OS" == "macos" ]]; then
            echo "  brew install --cask google-chrome"
            echo "  brew install --cask firefox"
        elif [[ "$OS" == "linux" ]]; then
            echo "  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -"
            echo "  echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list"
            echo "  sudo apt-get update && sudo apt-get install google-chrome-stable"
        fi
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [[ ! -d "venv" ]]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    print_success "pip upgraded"
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Use PC requirements
    if [[ -f "requirements_pc.txt" ]]; then
        pip install -r requirements_pc.txt
        print_success "Dependencies installed (PC version)"
    elif [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        print_success "Dependencies installed (standard version)"
    else
        print_warning "No requirements file found, installing basic dependencies..."
        pip install requests beautifulsoup4 selenium webdriver-manager lxml python-dotenv colorama psutil
    fi
}

# Setup directories
setup_directories() {
    print_status "Setting up directories..."
    
    mkdir -p logs data backups
    print_success "Directories created"
}

# Setup configuration
setup_config() {
    print_status "Setting up configuration..."
    
    # Copy configuration files
    if [[ ! -f ".env" ]]; then
        cp config/.env.example .env
        print_success "Created .env file"
        print_warning "Please edit .env file with your Tokopedia credentials"
    else
        print_success ".env file already exists"
    fi
    
    if [[ ! -f "config/accounts.json" ]]; then
        cp config/accounts.json.example config/accounts.json
        print_success "Created accounts.json example"
    fi
    
    if [[ -f "config/target_voucher.json" ]]; then
        print_success "target_voucher.json found"
    fi
}

# Create launch scripts
create_launchers() {
    print_status "Creating launch scripts..."
    
    # Main launcher
    cat > start_claimer.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python src/voucher_claimer.py
EOF

    # Target claimer launcher
    cat > start_target_claimer.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python src/target_claimer.py
EOF

    # Monitor launcher
    cat > start_monitor.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python src/monitor.py
EOF

    # Make them executable
    chmod +x start_claimer.sh start_target_claimer.sh start_monitor.sh
    
    print_success "Launch scripts created"
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    source venv/bin/activate
    
    if python -c "import requests, selenium, bs4, platform_utils" 2>/dev/null; then
        print_success "Installation test passed"
    else
        print_error "Installation test failed!"
        exit 1
    fi
}

# Create desktop shortcut (optional)
create_desktop_shortcut() {
    if [[ "$OS" == "linux" ]] && [[ -d "$HOME/Desktop" ]]; then
        print_status "Creating desktop shortcut..."
        
        cat > "$HOME/Desktop/TokopediaClaimer.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Tokopedia Voucher Claimer
Comment=Auto claim Tokopedia vouchers
Exec=$(pwd)/start_claimer.sh
Icon=$(pwd)/icon.png
Terminal=true
Categories=Utility;
EOF
        
        chmod +x "$HOME/Desktop/TokopediaClaimer.desktop"
        print_success "Desktop shortcut created"
    fi
}

# Main installation function
main() {
    print_banner
    
    print_status "Starting PC installation..."
    echo ""
    
    # Run all setup steps
    detect_os
    check_python
    check_pip
    check_browsers
    create_venv
    install_dependencies
    setup_directories
    setup_config
    create_launchers
    test_installation
    
    # Optional desktop shortcut
    if [[ "$1" != "--no-desktop" ]]; then
        create_desktop_shortcut
    fi
    
    echo ""
    print_success "🎉 Installation completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Edit .env file with your Tokopedia credentials:"
    echo "   nano .env"
    echo ""
    echo "2. Run one of these launchers:"
    echo "   ./start_claimer.sh        (Regular voucher claimer)"
    echo "   ./start_target_claimer.sh (Target voucher claimer)"
    echo "   ./start_monitor.sh        (Voucher monitor)"
    echo ""
    echo "3. Or run manually:"
    echo "   source venv/bin/activate"
    echo "   python src/voucher_claimer.py"
    echo ""
    echo "📚 Documentation: README.md"
    echo "📄 Logs: logs/ directory"
    echo "📊 Reports: data/ directory"
    echo ""
    print_warning "⚠️  Disclaimer: Use at your own risk"
    print_warning "   This script is for educational purposes only"
}

# Handle command line arguments
case "$1" in
    "--help"|"-h")
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h      Show this help message"
        echo "  --no-desktop    Don't create desktop shortcut"
        echo ""
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac