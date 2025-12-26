#!/bin/bash

# Tokopedia Voucher Claimer - Enhanced Run Script
# Launcher for various voucher claiming modes

echo "🎫 Tokopedia Voucher Auto Claimer - Enhanced"
echo "=========================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please copy config/.env.example to .env and configure it"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Check if credentials are set
if [ -z "$TOKOPEDIA_EMAIL" ] || [ -z "$TOKOPEDIA_PASSWORD" ]; then
    echo "❌ TOKOPEDIA_EMAIL or TOKOPEDIA_PASSWORD not set in .env file!"
    exit 1
fi

# Function to show menu
show_menu() {
    echo ""
    echo "🚀 Select execution mode:"
    echo "1) Single Account Claim (default)"
    echo "2) Multi-Account Claim"
    echo "3) Voucher Monitor"
    echo "4) Maintenance Tasks"
    echo "5) Installation Check"
    echo "6) Exit"
    echo ""
}

# Function to run single account claim
run_single() {
    echo "🎯 Running single account claim..."
    python3 src/voucher_claimer.py
}

# Function to run multi-account claim
run_multi() {
    echo "👥 Running multi-account claim..."
    
    # Check if accounts.json exists
    if [ ! -f "config/accounts.json" ]; then
        echo "📋 accounts.json not found. Using environment variables for multiple accounts..."
        echo "   Make sure to set TOKOPEDIA_EMAIL_1, TOKOPEDIA_PASSWORD_1, etc."
    fi
    
    python3 src/multi_claimer.py
}

# Function to run monitor
run_monitor() {
    echo "🔍 Starting voucher monitor..."
    
    # Check if monitor config exists
    if [ ! -f "config/monitor_config.json" ]; then
        echo "📝 monitor_config.json not found, using default settings"
    fi
    
    python3 src/monitor.py
}

# Function to run maintenance
run_maintenance() {
    echo "🔧 Maintenance tasks:"
    echo "1) Clean logs"
    echo "2) Clean reports"
    echo "3) Update dependencies"
    echo "4) Check installation"
    echo "5) Backup data"
    echo "6) Run all maintenance"
    echo ""
    
    read -p "Choose maintenance task (1-6): " maint_choice
    
    case $maint_choice in
        1) ./maintenance.sh clean-logs ;;
        2) ./maintenance.sh clean-reports ;;
        3) ./maintenance.sh update ;;
        4) ./maintenance.sh check ;;
        5) ./maintenance.sh backup ;;
        6) ./maintenance.sh all ;;
        *) echo "❌ Invalid choice" ;;
    esac
}

# Function to check installation
check_installation() {
    echo "🔍 Checking installation..."
    ./maintenance.sh check
}

# Main execution
if [ $# -eq 0 ]; then
    # Interactive mode
    while true; do
        show_menu
        read -p "Enter your choice (1-6) [default: 1]: " choice
        choice=${choice:-1}
        
        case $choice in
            1)
                run_single
                break
                ;;
            2)
                run_multi
                break
                ;;
            3)
                run_monitor
                break
                ;;
            4)
                run_maintenance
                ;;
            5)
                check_installation
                ;;
            6)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid choice. Please try again."
                ;;
        esac
    done
else
    # Command line mode
    case $1 in
        "single")
            run_single
            ;;
        "multi")
            run_multi
            ;;
        "monitor")
            run_monitor
            ;;
        "maintenance")
            run_maintenance
            ;;
        "check")
            check_installation
            ;;
        *)
            echo "Usage: $0 {single|multi|monitor|maintenance|check}"
            echo "  single      - Run single account claim"
            echo "  multi       - Run multi-account claim"
            echo "  monitor     - Start voucher monitor"
            echo "  maintenance - Run maintenance tasks"
            echo "  check       - Check installation"
            exit 1
            ;;
    esac
fi

echo ""
echo "✅ Process completed!"
echo "📄 Check logs/ directory for detailed logs"
echo "📊 Check data/ directory for claim reports"