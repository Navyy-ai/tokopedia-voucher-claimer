#!/usr/bin/env python3
"""
Multi-Platform Runner for Tokopedia Voucher Claimer
Supports both Termux and PC environments
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from platform_utils import PlatformDetector
from voucher_claimer import TokopediaVoucherClaimer
from target_claimer import TargetVoucherClaimer
from monitor import VoucherMonitor
from multi_claimer import MultiAccountClaimer

class MultiPlatformRunner:
    def __init__(self):
        self.detector = PlatformDetector()
        self.platform_info = self.detector.get_platform_info()
        
    def display_banner(self):
        """Display platform-specific banner"""
        if self.platform_info['is_termux']:
            banner = """
╔════════════════════════════════════════════════════════════╗
║         TOKOPEDIA VOUCHER CLAIMER - TERMUX                ║
║                 Mobile Edition                             ║
╚════════════════════════════════════════════════════════════╝
"""
        else:
            banner = """
╔════════════════════════════════════════════════════════════╗
║         TOKOPEDIA VOUCHER CLAIMER - PC EDITION              ║
║               Windows/macOS/Linux                          ║
╚════════════════════════════════════════════════════════════╝
"""
        
        print(banner)
        print(f"🖥️  Platform: {self.platform_info['system'].title()}")
        print(f"🐍 Python: {self.platform_info['python_version']}")
        print(f"🌐 Default Browser: {self.detector.get_default_browser()}")
        print()
    
    def check_environment(self):
        """Check if environment is properly set up"""
        print("🔍 Checking environment...")
        
        # Check credentials
        email = os.getenv('TOKOPEDIA_EMAIL')
        password = os.getenv('TOKOPEDIA_PASSWORD')
        
        if not email or not password:
            print("❌ TOKOPEDIA_EMAIL and TOKOPEDIA_PASSWORD environment variables not set!")
            print("\n💡 Solutions:")
            
            if self.platform_info['is_termux']:
                print("   1. Edit .env file")
                print("   2. Run: export TOKOPEDIA_EMAIL='your@email.com'")
                print("   3. Run: export TOKOPEDIA_PASSWORD='your_password'")
            else:
                print("   1. Edit .env file")
                print("   2. Activate venv and run: source .env")
                print("   3. Set environment variables manually")
            
            return False
        
        print("✅ Credentials found")
        
        # Check browser
        default_browser = self.detector.get_default_browser()
        if not default_browser:
            print("⚠️  No compatible browser found!")
            print("💡 Please install Chrome, Firefox, or Edge")
            return False
        
        print(f"✅ Browser available: {default_browser}")
        
        # Check dependencies
        try:
            import requests, selenium, bs4
            print("✅ Dependencies available")
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            print("💡 Run: pip install -r requirements_pc.txt")
            return False
        
        print("✅ Environment check passed")
        return True
    
    def show_menu(self):
        """Show interactive menu"""
        print("🚀 Select execution mode:")
        
        if self.platform_info['is_termux']:
            print("1) Target Voucher Claim (Belanjaanmu Dibayarin Tokopedia)")
            print("2) Single Account Claim (All Vouchers)")
            print("3) Multi-Account Claim")
            print("4) Voucher Monitor")
            print("5) Maintenance Tasks")
            print("6) Platform Info")
            print("7) Exit")
        else:
            print("1) Target Voucher Claim (Belanjaanmu Dibayarin Tokopedia)")
            print("2) Single Account Claim (All Vouchers)")
            print("3) Multi-Account Claim")
            print("4) Voucher Monitor")
            print("5) Maintenance Tasks")
            print("6) Platform Info")
            print("7) Browser Test")
            print("8) Exit")
        
        print()
    
    def run_target_claimer(self):
        """Run target voucher claimer"""
        print("🎯 Running Target Voucher Claimer...")
        try:
            claimer = TargetVoucherClaimer()
            email = os.getenv('TOKOPEDIA_EMAIL')
            password = os.getenv('TOKOPEDIA_PASSWORD')
            success = claimer.run_target_claim(email, password)
            claimer.display_summary()
            return success
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run_single_claimer(self):
        """Run single account voucher claimer"""
        print("🎫 Running Single Account Voucher Claimer...")
        try:
            claimer = TokopediaVoucherClaimer()
            email = os.getenv('TOKOPEDIA_EMAIL')
            password = os.getenv('TOKOPEDIA_PASSWORD')
            success = claimer.run_auto_claim(email, password)
            claimer.generate_report()
            return success
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run_multi_claimer(self):
        """Run multi-account voucher claimer"""
        print("👥 Running Multi-Account Voucher Claimer...")
        try:
            claimer = MultiAccountClaimer()
            if not claimer.accounts:
                print("❌ No accounts configured!")
                print("💡 Edit config/accounts.json or set environment variables")
                return False
            
            # Choose execution mode
            print("Execution mode:")
            print("1) Sequential (safer)")
            print("2) Parallel (faster)")
            
            try:
                choice = input("Choose mode (1 or 2) [default: 1]: ").strip()
                if not choice:
                    choice = "1"
                
                if choice == "1":
                    success = claimer.run_sequential_claims()
                else:
                    success = claimer.run_parallel_claims(max_workers=3)
                
                return success
            except KeyboardInterrupt:
                print("\n⚠️  Process interrupted")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run_monitor(self):
        """Run voucher monitor"""
        print("🔍 Starting Voucher Monitor...")
        try:
            monitor = VoucherMonitor()
            success = monitor.run_monitoring()
            return success
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run_maintenance(self):
        """Run maintenance tasks"""
        print("🔧 Running Maintenance Tasks...")
        
        if self.platform_info['is_termux']:
            # Termux maintenance
            try:
                subprocess.run(["./maintenance.sh"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Maintenance failed: {e}")
                return False
        else:
            # PC maintenance
            print("PC Maintenance Tasks:")
            print("1. Clean logs")
            print("2. Clean reports")
            print("3. Update dependencies")
            print("4. Check installation")
            print("5. Backup data")
            
            try:
                choice = input("Choose task (1-5): ").strip()
                
                if choice == "1":
                    import shutil
                    for file in Path("logs").glob("*.log"):
                        file.unlink()
                    print("✅ Logs cleaned")
                elif choice == "2":
                    for file in Path("data").glob("*.txt"):
                        file.unlink()
                    print("✅ Reports cleaned")
                elif choice == "3":
                    subprocess.run(["pip", "install", "--upgrade", "-r", "requirements_pc.txt"])
                    print("✅ Dependencies updated")
                elif choice == "4":
                    # Check installation
                    self.check_environment()
                elif choice == "5":
                    import shutil
                    from datetime import datetime
                    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    shutil.make_archive(f"backups/{backup_name}", 'zip', '.', exclude=["backups/*", "venv/*", "__pycache__/*"])
                    print(f"✅ Backup created: {backup_name}.zip")
                
                return True
            except Exception as e:
                print(f"❌ Error: {e}")
                return False
    
    def show_platform_info(self):
        """Display platform information"""
        print("🖥️  Platform Information:")
        print("=" * 50)
        
        for key, value in self.platform_info.items():
            print(f"{key:20}: {value}")
        
        print("\n🌐 Browser Information:")
        print("=" * 50)
        
        supported_browsers = self.detector.get_supported_browsers()
        print(f"Supported browsers: {', '.join(supported_browsers)}")
        
        default_browser = self.detector.get_default_browser()
        print(f"Default browser: {default_browser}")
        
        for browser in supported_browsers:
            installed = self.detector.check_browser_installed(browser)
            status = "✅ Installed" if installed else "❌ Not found"
            print(f"  {browser:15}: {status}")
    
    def test_browser(self):
        """Test browser functionality (PC only)"""
        if self.platform_info['is_termux']:
            print("❌ Browser test not available on Termux")
            return False
        
        print("🌐 Testing browser functionality...")
        
        try:
            claimer = TokopediaVoucherClaimer()
            print("✅ Browser setup successful")
            
            # Test navigation
            claimer.driver.get("https://www.google.com")
            print("✅ Navigation successful")
            
            claimer.driver.get("https://www.tokopedia.com")
            print("✅ Tokopedia accessible")
            
            claimer.cleanup()
            return True
            
        except Exception as e:
            print(f"❌ Browser test failed: {e}")
            return False
    
    def run(self):
        """Main runner function"""
        self.display_banner()
        
        # Check environment
        if not self.check_environment():
            input("\nPress Enter to exit...")
            return
        
        # Interactive menu
        while True:
            self.show_menu()
            
            try:
                if self.platform_info['is_termux']:
                    choice = input("Enter your choice (1-7): ").strip()
                else:
                    choice = input("Enter your choice (1-8): ").strip()
                
                if not choice:
                    continue
                
                if choice == "1":
                    self.run_target_claimer()
                elif choice == "2":
                    self.run_single_claimer()
                elif choice == "3":
                    self.run_multi_claimer()
                elif choice == "4":
                    self.run_monitor()
                elif choice == "5":
                    self.run_maintenance()
                elif choice == "6":
                    self.show_platform_info()
                elif choice == "7":
                    if not self.platform_info['is_termux']:
                        self.test_browser()
                    else:
                        print("👋 Goodbye!")
                        break
                elif choice == "8":
                    if not self.platform_info['is_termux']:
                        print("👋 Goodbye!")
                        break
                    else:
                        print("❌ Invalid choice")
                else:
                    print("❌ Invalid choice")
                
                if choice not in ["7", "8"] or (self.platform_info['is_termux'] and choice == "7") or (not self.platform_info['is_termux'] and choice == "8"):
                    input("\nPress Enter to continue...")
                    print("\n" + "="*60 + "\n")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Process interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    runner = MultiPlatformRunner()
    runner.run()


if __name__ == "__main__":
    main()