#!/usr/bin/env python3
"""
Tokopedia War Voucher Auto Claimer
Script otomatis untuk mengklaim voucher Tokopedia menggunakan Termux
"""

import os
import sys
import time
import random
import logging
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import colorama
from colorama import Fore, Style

# Inisialisasi colorama
colorama.init()

class TokopediaVoucherClaimer:
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self.wait = None
        self.claimed_vouchers = []
        self.failed_vouchers = []
        
        # Setup logging
        self.setup_logging()
        
        # Setup browser
        self.setup_browser()
        
    def setup_logging(self):
        """Setup logging untuk monitoring"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_filename = f"{log_dir}/voucher_claim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def setup_browser(self):
        """Setup Chrome WebDriver untuk mobile view"""
        try:
            chrome_options = Options()
            
            # Mobile user agent untuk Termux compatibility
            mobile_user_agent = "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
            chrome_options.add_argument(f"--user-agent={mobile_user_agent}")
            
            # Additional options for headless mode
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=360,640")
            
            # Install ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            self.logger.info("✅ Browser setup successful")
            
        except Exception as e:
            self.logger.error(f"❌ Browser setup failed: {e}")
            sys.exit(1)
    
    def login_tokopedia(self, email, password):
        """Login ke Tokopedia"""
        try:
            self.logger.info(f"🔐 Attempting login with email: {email}")
            
            # Navigate to login page
            self.driver.get("https://www.tokopedia.com/login")
            
            # Wait for email input
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']"))
            )
            
            # Input email
            email_input.clear()
            email_input.send_keys(email)
            
            # Click continue
            continue_btn = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='btn-login-continue']")
            continue_btn.click()
            
            # Wait for password input
            password_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            
            # Input password
            password_input.clear()
            password_input.send_keys(password)
            
            # Click login button
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='btn-login']")
            login_btn.click()
            
            # Wait for login success
            time.sleep(3)
            
            # Check if login successful
            if "tokopedia.com" in self.driver.current_url and "login" not in self.driver.current_url:
                self.logger.info("✅ Login successful!")
                return True
            else:
                self.logger.error("❌ Login failed!")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Login error: {e}")
            return False
    
    def find_voucher_page(self):
        """Navigate to voucher/war page"""
        try:
            self.logger.info("🔍 Navigating to voucher page...")
            
            # Go to Tokopedia homepage
            self.driver.get("https://www.tokopedia.com")
            
            # Look for voucher/menu button
            try:
                voucher_menu = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'voucher') or contains(text(), 'Voucher')]"))
                )
                voucher_menu.click()
            except:
                # Alternative method
                self.driver.get("https://www.tokopedia.com/voucher")
            
            time.sleep(2)
            self.logger.info("✅ Successfully navigated to voucher page")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error navigating to voucher page: {e}")
            return False
    
    def scan_available_vouchers(self):
        """Scan for available vouchers on the page"""
        vouchers = []
        
        try:
            self.logger.info("🔍 Scanning for available vouchers...")
            
            # Scroll to load more vouchers
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Find voucher elements
            voucher_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "[data-testid*='voucher'], .voucher-card, [class*='voucher']")
            
            for element in voucher_elements:
                try:
                    voucher_data = self.extract_voucher_data(element)
                    if voucher_data:
                        vouchers.append(voucher_data)
                except Exception as e:
                    self.logger.warning(f"Error extracting voucher: {e}")
                    continue
            
            self.logger.info(f"📊 Found {len(vouchers)} vouchers")
            return vouchers
            
        except Exception as e:
            self.logger.error(f"❌ Error scanning vouchers: {e}")
            return []
    
    def extract_voucher_data(self, element):
        """Extract voucher information from element"""
        try:
            voucher_info = {}
            
            # Get voucher title/name
            try:
                title = element.find_element(By.CSS_SELECTOR, "[class*='title'], h2, h3, .name")
                voucher_info['title'] = title.text.strip()
            except:
                voucher_info['title'] = "Unknown Voucher"
            
            # Get voucher value/discount
            try:
                discount = element.find_element(By.CSS_SELECTOR, "[class*='discount'], [class*='value'], .amount")
                voucher_info['discount'] = discount.text.strip()
            except:
                voucher_info['discount'] = "Unknown"
            
            # Get voucher expiry
            try:
                expiry = element.find_element(By.CSS_SELECTOR, "[class*='expiry'], [class*='valid'], .date")
                voucher_info['expiry'] = expiry.text.strip()
            except:
                voucher_info['expiry'] = "Unknown"
            
            # Check if already claimed
            try:
                claimed_text = element.find_element(By.CSS_SELECTOR, "[class*='claimed'], [class*='used']")
                voucher_info['claimed'] = "claimed" in claimed_text.text.lower()
            except:
                voucher_info['claimed'] = False
            
            # Store element reference
            voucher_info['element'] = element
            
            return voucher_info
            
        except Exception as e:
            self.logger.warning(f"Error extracting voucher data: {e}")
            return None
    
    def claim_voucher(self, voucher):
        """Claim a specific voucher"""
        try:
            self.logger.info(f"🎯 Attempting to claim: {voucher['title']}")
            
            if voucher['claimed']:
                self.logger.info(f"⚠️  Voucher already claimed: {voucher['title']}")
                return False
            
            # Click on voucher to claim
            voucher['element'].click()
            time.sleep(2)
            
            # Look for claim button
            try:
                claim_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Klaim') or contains(text(), 'Claim') or contains(text(), 'Ambil')]"))
                )
                claim_btn.click()
                
                # Wait for claim confirmation
                time.sleep(3)
                
                # Check if claim successful
                success_indicators = [
                    "berhasil diklaim", "successfully claimed", "voucher kamu",
                    "success", "berhasil"
                ]
                
                page_text = self.driver.page_source.lower()
                if any(indicator in page_text for indicator in success_indicators):
                    self.logger.info(f"✅ Successfully claimed: {voucher['title']}")
                    self.claimed_vouchers.append(voucher)
                    return True
                else:
                    self.logger.warning(f"⚠️  Claim may have failed for: {voucher['title']}")
                    self.failed_vouchers.append(voucher)
                    return False
                    
            except TimeoutException:
                self.logger.warning(f"⚠️  Could not find claim button for: {voucher['title']}")
                self.failed_vouchers.append(voucher)
                return False
            
        except Exception as e:
            self.logger.error(f"❌ Error claiming voucher {voucher['title']}: {e}")
            self.failed_vouchers.append(voucher)
            return False
    
    def run_auto_claim(self, email, password):
        """Run the complete auto-claim process"""
        try:
            self.logger.info("🚀 Starting Tokopedia Voucher Auto Claimer")
            
            # Login
            if not self.login_tokopedia(email, password):
                return False
            
            # Navigate to voucher page
            if not self.find_voucher_page():
                return False
            
            # Scan for vouchers
            vouchers = self.scan_available_vouchers()
            
            if not vouchers:
                self.logger.info("📭 No vouchers found")
                return True
            
            # Claim available vouchers
            unclaimed_vouchers = [v for v in vouchers if not v['claimed']]
            
            self.logger.info(f"🎯 Found {len(unclaimed_vouchers)} unclaimed vouchers")
            
            for voucher in unclaimed_vouchers:
                success = self.claim_voucher(voucher)
                
                # Random delay between claims to avoid detection
                delay = random.uniform(2, 5)
                time.sleep(delay)
            
            # Generate report
            self.generate_report()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error in auto-claim process: {e}")
            return False
    
    def generate_report(self):
        """Generate claim report"""
        report = f"""
📊 VOUCHER CLAIM REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

✅ SUCCESSFULLY CLAIMED: {len(self.claimed_vouchers)}
❌ FAILED TO CLAIM: {len(self.failed_vouchers)}

CLAIMED VOUCHERS:
{'-'*30}
"""
        
        for voucher in self.claimed_vouchers:
            report += f"🎫 {voucher['title']} - {voucher['discount']}\n"
        
        report += f"""
FAILED VOUCHERS:
{'-'*30}
"""
        
        for voucher in self.failed_vouchers:
            report += f"❌ {voucher['title']} - {voucher['discount']}\n"
        
        report += f"\n{'='*50}\n"
        
        # Save report to file
        report_filename = f"data/claim_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        
        self.logger.info("📄 Report saved to: " + report_filename)
        print(report)
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()
        self.logger.info("🧹 Cleanup completed")


def main():
    """Main function"""
    print(f"""
{Fore.GREEN}╔════════════════════════════════════════════════════════════╗
║                TOKOPEDIA VOUCHER AUTO CLAIMER                  ║
║                     Termux Edition                            ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    # Load credentials from environment or config
    email = os.getenv('TOKOPEDIA_EMAIL')
    password = os.getenv('TOKOPEDIA_PASSWORD')
    
    if not email or not password:
        print(f"{Fore.RED}❌ Please set TOKOPEDIA_EMAIL and TOKOPEDIA_PASSWORD environment variables{Style.RESET_ALL}")
        print("Or create .env file with your credentials")
        return
    
    # Initialize claimer
    claimer = TokopediaVoucherClaimer()
    
    try:
        # Run auto-claim
        success = claimer.run_auto_claim(email, password)
        
        if success:
            print(f"{Fore.GREEN}✅ Auto-claim process completed successfully!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Auto-claim process failed!{Style.RESET_ALL}")
            
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}⚠️  Process interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
    finally:
        claimer.cleanup()


if __name__ == "__main__":
    main()