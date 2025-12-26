#!/usr/bin/env python3
"""
Tokopedia Target Voucher Claimer
Script khusus untuk klaim voucher target seperti "Belanjaanmu Dibayarin Tokopedia"
"""

import os
import sys
import time
import logging
from datetime import datetime
from voucher_claimer import TokopediaVoucherClaimer
import colorama
from colorama import Fore, Style

colorama.init()

class TargetVoucherClaimer:
    def __init__(self):
        self.claimer = None
        self.target_found = False
        self.target_claimed = False
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging khusus untuk target voucher"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_filename = f"{log_dir}/target_claim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def display_banner(self):
        """Display banner untuk target voucher claimer"""
        banner = f"""
{Fore.GREEN}╔════════════════════════════════════════════════════════════╗
║          TOKOPEDIA TARGET VOUCHER CLAIMER                  ║
║      Specialized for "Belanjaanmu Dibayarin Tokopedia"    ║
║                   Termux Edition                            ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    def check_target_config(self):
        """Check if target voucher configuration exists"""
        config_file = "config/target_voucher.json"
        if not os.path.exists(config_file):
            self.logger.warning(f"⚠️  Target voucher configuration not found: {config_file}")
            self.logger.info("📝 Please create target_voucher.json with your target vouchers")
            return False
        return True
    
    def run_target_claim(self, email, password):
        """Run target voucher claiming process"""
        try:
            self.display_banner()
            
            # Check configuration
            if not self.check_target_config():
                return False
            
            self.logger.info("🎯 Starting Target Voucher Claimer...")
            self.logger.info("🔍 Looking for: Belanjaanmu Dibayarin Tokopedia")
            
            # Initialize claimer
            self.claimer = TokopediaVoucherClaimer()
            
            # Run auto claim
            success = self.claimer.run_auto_claim(email, password)
            
            if success:
                # Check if target vouchers were found
                if self.claimer.target_vouchers_found:
                    self.target_found = True
                    self.logger.info(f"🎯 Target vouchers found: {len(self.claimer.target_vouchers_found)}")
                    
                    # Check if any were claimed
                    target_claimed = [v for v in self.claimer.claimed_vouchers if v.get('is_target')]
                    if target_claimed:
                        self.target_claimed = True
                        self.logger.info(f"✅ Successfully claimed target vouchers!")
                        for voucher in target_claimed:
                            print(f"{Fore.GREEN}🎯🎯🎯 TARGET VOUCHER CLAIMED: {voucher['title']} - {voucher['discount']} 🎯🎯🎯{Style.RESET_ALL}")
                    else:
                        self.logger.warning("⚠️  Target vouchers found but failed to claim")
                else:
                    self.logger.info("📭 No target vouchers found this time")
                
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error in target claim process: {e}")
            return False
        finally:
            if self.claimer:
                self.claimer.cleanup()
    
    def display_summary(self):
        """Display summary of target claiming"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}TARGET VOUCHER CLAIM SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        if self.target_found:
            print(f"{Fore.GREEN}✅ Target vouchers were found{Style.RESET_ALL}")
            if self.target_claimed:
                print(f"{Fore.GREEN}✅ Target vouchers were successfully claimed{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️  Target vouchers found but claim failed{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  No target vouchers found{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


def main():
    """Main function"""
    # Check credentials
    email = os.getenv('TOKOPEDIA_EMAIL')
    password = os.getenv('TOKOPEDIA_PASSWORD')
    
    if not email or not password:
        print(f"{Fore.RED}❌ Please set TOKOPEDIA_EMAIL and TOKOPEDIA_PASSWORD environment variables{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Or create .env file with your credentials{Style.RESET_ALL}")
        return
    
    # Initialize target claimer
    target_claimer = TargetVoucherClaimer()
    
    try:
        # Run target claim
        success = target_claimer.run_target_claim(email, password)
        
        # Display summary
        target_claimer.display_summary()
        
        if success:
            print(f"{Fore.GREEN}✅ Target claim process completed!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Target claim process failed!{Style.RESET_ALL}")
            
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}⚠️  Process interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()