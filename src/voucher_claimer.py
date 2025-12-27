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
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import colorama
from colorama import Fore, Style
from platform_utils import PlatformDetector

# Inisialisasi colorama
colorama.init()

class TokopediaVoucherClaimer:
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self.wait = None
        self.claimed_vouchers = []
        self.failed_vouchers = []
        self.target_vouchers_config = self.load_target_voucher_config()
        self.target_vouchers_found = []
        
        # Setup logging
        self.setup_logging()
        
        # Setup browser
        self.setup_browser()
    
    def load_target_voucher_config(self):
        """Load target voucher configuration"""
        try:
            config_file = "config/target_voucher.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                self.logger.info("✅ Target voucher configuration loaded")
                return config
            else:
                self.logger.info("📋 No target voucher configuration found, using general scan mode")
                return None
        except Exception as e:
            self.logger.error(f"❌ Error loading target voucher config: {e}")
            return None
        
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
        
    def setup_browser(self, browser_type: str = None):
        """Setup WebDriver untuk multi-platform support"""
        try:
            self.platform_detector = PlatformDetector()
            platform_info = self.platform_detector.get_platform_info()
            
            # Determine browser type
            if not browser_type:
                browser_type = self.platform_detector.get_default_browser()
                if not browser_type:
                    browser_type = "chrome"  # fallback
            
            self.logger.info(f"🌐 Setting up {browser_type} browser for {platform_info['system']}")
            
            # Setup based on browser type
            if browser_type.lower() in ["chrome", "chromium"]:
                success = self._setup_chrome_browser()
            elif browser_type.lower() == "firefox":
                success = self._setup_firefox_browser()
            elif browser_type.lower() == "edge":
                success = self._setup_edge_browser()
            else:
                self.logger.error(f"❌ Unsupported browser: {browser_type}")
                success = False
            
            if success:
                self.wait = WebDriverWait(self.driver, 10)
                self.logger.info(f"✅ {browser_type} browser setup successful")
            else:
                self.logger.error(f"❌ Browser setup failed")
                sys.exit(1)
                
        except Exception as e:
            self.logger.error(f"❌ Browser setup failed: {e}")
            sys.exit(1)
    
    def _setup_chrome_browser(self) -> bool:
        """Setup Chrome/Chromium browser"""
        try:
            chrome_options = Options()
            
            # Get platform-specific user agent
            user_agent = self.platform_detector.get_platform_specific_user_agent()
            chrome_options.add_argument(f"--user-agent={user_agent}")
            
            # Platform-specific options
            if self.platform_detector.is_termux:
                # Termux specific options
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=360,640")
            else:
                # PC options -可以选择是否headless
                headless = os.getenv("HEADLESS_MODE", "true").lower() == "true"
                if headless:
                    chrome_options.add_argument("--headless")
                
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                # Window size for desktop
                if not headless:
                    chrome_options.add_argument("--window-size=1280,720")
                else:
                    chrome_options.add_argument("--window-size=1366,768")
            
            # Setup service and driver
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e:
                self.logger.warning(f"ChromeDriverManager failed: {e}")
                # Try system chromedriver
                self.driver = webdriver.Chrome(options=chrome_options)
            
            # Set page load timeout
            self.driver.set_page_load_timeout(30)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Chrome setup failed: {e}")
            return False
    
    def _setup_firefox_browser(self) -> bool:
        """Setup Firefox browser"""
        try:
            firefox_options = FirefoxOptions()
            
            # Get platform-specific user agent
            user_agent = self.platform_detector.get_platform_specific_user_agent()
            firefox_options.set_preference("general.useragent.override", user_agent)
            
            # Firefox options
            firefox_options.set_preference("dom.webdriver.enabled", False)
            firefox_options.set_preference("useAutomationExtension", False)
            
            headless = os.getenv("HEADLESS_MODE", "true").lower() == "true"
            if headless:
                firefox_options.add_argument("--headless")
            
            # Setup service and driver
            try:
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=firefox_options)
            except Exception as e:
                self.logger.warning(f"GeckoDriverManager failed: {e}")
                self.driver = webdriver.Firefox(options=firefox_options)
            
            self.driver.set_page_load_timeout(30)
            return True
            
        except Exception as e:
            self.logger.error(f"Firefox setup failed: {e}")
            return False
    
    def _setup_edge_browser(self) -> bool:
        """Setup Microsoft Edge browser"""
        try:
            edge_options = EdgeOptions()
            
            # Get platform-specific user agent
            user_agent = self.platform_detector.get_platform_specific_user_agent()
            edge_options.add_argument(f"--user-agent={user_agent}")
            
            # Edge options
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--disable-blink-features=AutomationControlled")
            
            headless = os.getenv("HEADLESS_MODE", "true").lower() == "true"
            if headless:
                edge_options.add_argument("--headless")
            
            # Setup service and driver
            try:
                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=edge_options)
            except Exception as e:
                self.logger.warning(f"EdgeDriverManager failed: {e}")
                self.driver = webdriver.Edge(options=edge_options)
            
            self.driver.set_page_load_timeout(30)
            return True
            
        except Exception as e:
            self.logger.error(f"Edge setup failed: {e}")
            return False
    
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
        target_vouchers = []
        
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
                        
                        # Check if this is a target voucher
                        if voucher_data['is_target']:
                            target_vouchers.append(voucher_data)
                            self.logger.info(f"🎯 TARGET VOUCHER FOUND: {voucher_data['title']}")
                except Exception as e:
                    self.logger.warning(f"Error extracting voucher: {e}")
                    continue
            
            # Sort vouchers by priority (target vouchers first)
            vouchers.sort(key=lambda x: x['priority'], reverse=True)
            
            self.logger.info(f"📊 Found {len(vouchers)} vouchers total")
            if target_vouchers:
                self.logger.info(f"🎯 Found {len(target_vouchers)} target vouchers!")
                self.target_vouchers_found = target_vouchers
            
            return vouchers
            
        except Exception as e:
            self.logger.error(f"❌ Error scanning vouchers: {e}")
            return []
    
    def is_target_voucher(self, voucher_info):
        """Check if voucher matches target configuration"""
        if not self.target_vouchers_config:
            return False
        
        target_vouchers = self.target_vouchers_config.get('target_vouchers', [])
        
        for target in target_vouchers:
            if not target.get('enabled', True):
                continue
            
            keywords = target.get('keywords', [])
            voucher_title = voucher_info.get('title', '').lower()
            
            # Check if any keyword matches
            for keyword in keywords:
                if keyword.lower() in voucher_title:
                    return target
        
        return None
    
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
            
            # Check if this is a target voucher
            target_config = self.is_target_voucher(voucher_info)
            if target_config:
                voucher_info['is_target'] = True
                voucher_info['target_config'] = target_config
                voucher_info['priority'] = target_config.get('priority', 0)
            else:
                voucher_info['is_target'] = False
                voucher_info['target_config'] = None
                voucher_info['priority'] = 0
            
            # Store element reference
            voucher_info['element'] = element
            
            return voucher_info
            
        except Exception as e:
            self.logger.warning(f"Error extracting voucher data: {e}")
            return None
    
    def claim_voucher(self, voucher):
        """Claim a specific voucher"""
        try:
            # Check if this is a target voucher and add special logging
            if voucher.get('is_target', False):
                self.logger.info(f"🎯🎯🎯 TARGET VOUCHER ATTEMPT: {voucher['title']} 🎯🎯🎯")
                target_config = voucher.get('target_config', {})
                
                # Play sound notification if enabled
                if target_config.get('notification', {}).get('sound', False):
                    self.logger.info("🔔 TARGET VOUCHER ALERT!")
            else:
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
                    if voucher.get('is_target', False):
                        self.logger.info(f"✅✅✅ TARGET VOUCHER SUCCESSFULLY CLAIMED: {voucher['title']} ✅✅✅")
                    else:
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
            
            # Check if target vouchers are configured
            if self.target_vouchers_config:
                target_names = [v['name'] for v in self.target_vouchers_config.get('target_vouchers', []) if v.get('enabled')]
                if target_names:
                    self.logger.info(f"🎯 Target vouchers configured: {', '.join(target_names)}")
            
            # Login
            if not self.login_tokopedia(email, password):
                return False
            
            # Navigate to voucher page
            if not self.find_voucher_page():
                return False
            
            # Scan for vouchers (sorted by priority)
            vouchers = self.scan_available_vouchers()
            
            if not vouchers:
                self.logger.info("📭 No vouchers found")
                return True
            
            # Separate target and regular vouchers
            target_vouchers = [v for v in vouchers if v.get('is_target', False) and not v['claimed']]
            regular_vouchers = [v for v in vouchers if not v.get('is_target', False) and not v['claimed']]
            
            # Claim target vouchers first
            if target_vouchers:
                self.logger.info(f"🎯🎯🎯 CLAIMING {len(target_vouchers)} TARGET VOUCHERS FIRST! 🎯🎯🎯")
                
                for voucher in target_vouchers:
                    success = self.claim_voucher(voucher)
                    
                    # Shorter delay for target vouchers (priority)
                    delay = random.uniform(1, 3)
                    time.sleep(delay)
                
                # Check results
                claimed_targets = [v for v in target_vouchers if v in self.claimed_vouchers]
                if claimed_targets:
                    self.logger.info(f"✅ Successfully claimed {len(claimed_targets)} target vouchers!")
                else:
                    self.logger.warning(f"⚠️  Failed to claim any target vouchers")
            
            # Claim regular vouchers
            if regular_vouchers:
                self.logger.info(f"🎫 Claiming {len(regular_vouchers)} regular vouchers...")
                
                for voucher in regular_vouchers:
                    success = self.claim_voucher(voucher)
                    
                    # Regular delay
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
        # Separate target and regular vouchers
        target_claimed = [v for v in self.claimed_vouchers if v.get('is_target', False)]
        regular_claimed = [v for v in self.claimed_vouchers if not v.get('is_target', False)]
        target_failed = [v for v in self.failed_vouchers if v.get('is_target', False)]
        regular_failed = [v for v in self.failed_vouchers if not v.get('is_target', False)]
        
        report = f"""
📊 VOUCHER CLAIM REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

🎯 TARGET VOUCHERS:
✅ Claimed: {len(target_claimed)}
❌ Failed: {len(target_failed)}

🎫 REGULAR VOUCHERS:
✅ Claimed: {len(regular_claimed)}
❌ Failed: {len(regular_failed)}

📊 TOTAL:
✅ SUCCESSFULLY CLAIMED: {len(self.claimed_vouchers)}
❌ FAILED TO CLAIM: {len(self.failed_vouchers)}
{'='*60}

TARGET VOUCHERS CLAIMED:
{'-'*30}
"""
        
        for voucher in target_claimed:
            report += f"🎯🎯🎯 {voucher['title']} - {voucher['discount']}\n"
        
        report += "\nTARGET VOUCHERS FAILED:\n"
        report += f"{'-'*30}\n"
        
        for voucher in target_failed:
            report += f"❌ {voucher['title']} - {voucher['discount']}\n"
        
        report += f"\nREGULAR VOUCHERS CLAIMED:\n"
        report += f"{'-'*30}\n"
        
        for voucher in regular_claimed:
            report += f"🎫 {voucher['title']} - {voucher['discount']}\n"
        
        report += f"\nREGULAR VOUCHERS FAILED:\n"
        report += f"{'-'*30}\n"
        
        for voucher in regular_failed:
            report += f"❌ {voucher['title']} - {voucher['discount']}\n"
        
        report += f"\n{'='*60}\n"
        
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