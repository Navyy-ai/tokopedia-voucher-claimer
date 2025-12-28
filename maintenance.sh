#!/bin/bash

# Tokopedia Voucher Claimer - Maintenance Script
# For cleaning logs, updating dependencies, etc.

echo "🔧 Tokopedia Voucher Claimer - Maintenance"
echo "=========================================="

# Function to clean old logs
clean_logs() {
    echo "🧹 Cleaning old logs (older than 7 days)..."
    find logs/ -name "*.log" -mtime +7 -delete
    echo "✅ Old logs cleaned"
}

# Function to clean old reports
clean_reports() {
    echo "🧹 Cleaning old reports (older than 30 days)..."
    find data/ -name "*.txt" -mtime +30 -delete
    echo "✅ Old reports cleaned"
}

# Function to update dependencies
update_deps() {
    echo "📦 Updating Python dependencies..."
    pip install --upgrade -r requirements.txt
    echo "✅ Dependencies updated"
}

# Function to check installation
check_install() {
    echo "🔍 Checking installation..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        echo "✅ Python3 installed"
    else
        echo "❌ Python3 not found"
        return 1
    fi
    
    # Check Chrome/Chromium
    if command -v chromium &> /dev/null; then
        echo "✅ Chromium installed"
    else
        echo "❌ Chromium not found - run ./install.sh"
        return 1
    fi
    
    # Check Python packages
    echo "🔍 Checking Python packages..."
    python3 -c "import requests, selenium, bs4" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Python packages OK"
    else
        echo "❌ Missing Python packages - run pip install -r requirements.txt"
        return 1
    fi
    
    echo "✅ Installation check completed"
}

# Function to backup data
backup_data() {
    echo "💾 Creating backup..."
    backup_name="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "backups/$backup_name"
    
    # Copy important files
    cp -r logs/ "backups/$backup_name/" 2>/dev/null
    cp -r data/ "backups/$backup_name/" 2>/dev/null
    cp .env "backups/$backup_name/" 2>/dev/null
    
    # Create backup archive
    tar -czf "backups/${backup_name}.tar.gz" -C "backups/$backup_name" .
    rm -rf "backups/$backup_name"
    
    echo "✅ Backup created: backups/${backup_name}.tar.gz"
}

# Main menu
case "$1" in
    "clean-logs")
        clean_logs
        ;;
    "clean-reports")
        clean_reports
        ;;
    "clean-all")
        clean_logs
        clean_reports
        ;;
    "update")
        update_deps
        ;;
    "check")
        check_install
        ;;
    "backup")
        backup_data
        ;;
    "all")
        clean_logs
        clean_reports
        update_deps
        check_install
        backup_data
        ;;
    *)
        echo "Usage: $0 {clean-logs|clean-reports|clean-all|update|check|backup|all}"
        echo ""
        echo "Options:"
        echo "  clean-logs    - Clean log files older than 7 days"
        echo "  clean-reports - Clean report files older than 30 days"
        echo "  clean-all     - Clean both logs and reports"
        echo "  update        - Update Python dependencies"
        echo "  check         - Check installation status"
        echo "  backup        - Create backup of data"
        echo "  all           - Run all maintenance tasks"
        exit 1
        ;;
esac