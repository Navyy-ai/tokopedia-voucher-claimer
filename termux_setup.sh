#!/bin/bash

# Complete Termux Setup for Tokopedia Voucher Claimer
# This script handles the entire setup process for Termux

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
    echo "║         TOKOPEDIA VOUCHER CLAIMER - TERMUX SETUP          ║"
    echo "║                    Complete Installation                  ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if running on Termux
check_termux() {
    print_status "Checking Termux environment..."
    
    if [ ! -d "/data/data/com.termux" ]; then
        print_error "This script is designed for Termux environment"
        print_error "Please install Termux from F-Droid or GitHub"
        exit 1
    fi
    
    print_success "Termux environment detected"
}

# Update Termux packages
update_packages() {
    print_status "Updating Termux packages..."
    
    pkg update -y
    pkg upgrade -y
    
    print_success "Termux packages updated"
}

# Install required packages
install_packages() {
    print_status "Installing required packages..."
    
    # Core packages
    pkg install -y python python-pip git wget curl
    
    # Browser and dependencies
    pkg install -y chromium libandroid-spawn
    
    # Additional utilities
    pkg install -y nano vim tar
    
    print_success "Required packages installed"
}

# Setup Python environment
setup_python() {
    print_status "Setting up Python environment..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install wheel for faster installations
    pip install wheel
    
    print_success "Python environment setup completed"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Additional dependencies for Termux
    pip install --upgrade urllib3 certifi
    
    print_success "Python dependencies installed"
}

# Setup directories
setup_directories() {
    print_status "Setting up directories..."
    
    # Create necessary directories
    mkdir -p logs data backups
    
    # Set permissions
    chmod 755 src config logs data backups
    
    print_success "Directories setup completed"
}

# Setup configuration files
setup_config() {
    print_status "Setting up configuration files..."
    
    # Copy example configurations
    if [ ! -f ".env" ]; then
        cp config/.env.example .env
        print_warning "Created .env file - Please edit with your credentials"
    fi
    
    if [ ! -f "config/accounts.json" ]; then
        cp config/accounts.json.example config/accounts.json
        print_warning "Created accounts.json example - Edit for multi-account use"
    fi
    
    if [ ! -f "config/monitor_config.json" ]; then
        print_status "Monitor configuration already exists"
    fi
    
    print_success "Configuration files setup completed"
}

# Set executable permissions
set_permissions() {
    print_status "Setting executable permissions..."
    
    chmod +x install.sh
    chmod +x run.sh
    chmod +x maintenance.sh
    chmod +x termux_setup.sh
    chmod +x src/*.py
    
    print_success "Permissions set"
}

# Create desktop shortcut (if supported)
create_shortcut() {
    print_status "Creating desktop shortcut..."
    
    # Check if desktop directory exists
    if [ -d "$HOME/Desktop" ]; then
        cat > "$HOME/Desktop/TokopediaClaimer.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Tokopedia Voucher Claimer
Comment=Auto claim Tokopedia vouchers
Exec=$(pwd)/run.sh
Icon=$(pwd)/icon.png
Terminal=true
Categories=Utility;
EOF
        
        chmod +x "$HOME/Desktop/TokopediaClaimer.desktop"
        print_success "Desktop shortcut created"
    else
        print_warning "Desktop directory not found, skipping shortcut creation"
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test Python
    if python3 --version > /dev/null 2>&1; then
        print_success "Python is working"
    else
        print_error "Python is not working properly"
        return 1
    fi
    
    # Test Chrome
    if chromium --version > /dev/null 2>&1; then
        print_success "Chromium is working"
    else
        print_warning "Chromium might need additional setup"
    fi
    
    # Test Python imports
    if python3 -c "import requests, selenium, bs4" > /dev/null 2>&1; then
        print_success "Python dependencies are working"
    else
        print_error "Python dependencies are not working properly"
        return 1
    fi
    
    print_success "Installation test completed"
}

# Create first run script
create_first_run() {
    print_status "Creating first run script..."
    
    cat > "first_run.sh" << 'EOF'
#!/bin/bash

# First Run Script for Tokopedia Voucher Claimer
echo "🎫 Welcome to Tokopedia Voucher Claimer!"
echo "======================================"
echo ""
echo "📝 Before running the claimer, you need to:"
echo "1. Edit .env file with your Tokopedia credentials"
echo "2. (Optional) Edit config/accounts.json for multiple accounts"
echo ""
echo "🔧 Let's open the configuration file for you..."

# Check if nano is available
if command -v nano &> /dev/null; then
    nano .env
else
    echo "Please manually edit the .env file with your credentials:"
    echo "TOKOPEDIA_EMAIL=your_email@example.com"
    echo "TOKOPEDIA_PASSWORD=your_password"
fi

echo ""
echo "✅ Configuration completed! You can now run:"
echo "   ./run.sh"
EOF
    
    chmod +x first_run.sh
    print_success "First run script created"
}

# Main installation function
main() {
    print_banner
    
    print_status "Starting complete Termux setup..."
    echo ""
    
    # Run all setup steps
    check_termux
    update_packages
    install_packages
    setup_python
    install_dependencies
    setup_directories
    setup_config
    set_permissions
    create_shortcut
    create_first_run
    
    echo ""
    print_status "Running installation test..."
    test_installation
    
    echo ""
    print_success "🎉 Installation completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Run ./first_run.sh to configure your credentials"
    echo "2. Or manually edit .env file with your Tokopedia email and password"
    echo "3. Run ./run.sh to start the voucher claimer"
    echo ""
    echo "🔧 Additional commands:"
    echo "   ./run.sh maintenance - Run maintenance tasks"
    echo "   ./run.sh monitor     - Start voucher monitor"
    echo "   ./run.sh multi       - Run multi-account claimer"
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
        echo "  --help, -h     Show this help message"
        echo "  --test-only    Only test existing installation"
        echo "  --update       Update existing installation"
        echo ""
        echo "Default behavior: Complete fresh installation"
        exit 0
        ;;
    "--test-only")
        print_status "Testing existing installation..."
        test_installation
        exit $?
        ;;
    "--update")
        print_status "Updating existing installation..."
        update_packages
        setup_python
        install_dependencies
        set_permissions
        test_installation
        print_success "Update completed!"
        exit 0
        ;;
    *)
        main
        ;;
esac