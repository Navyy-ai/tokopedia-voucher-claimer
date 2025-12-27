#!/usr/bin/env python3
"""
Tokopedia Multi-Account Voucher Claimer
Script untuk mengklaim voucher menggunakan multiple accounts
"""

import os
import sys
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from voucher_claimer import TokopediaVoucherClaimer
import logging
from datetime import datetime

class MultiAccountClaimer:
    def __init__(self):
        self.accounts = []
        self.results = []
        self.setup_logging()
        self.load_accounts()
        
    def setup_logging(self):
        """Setup logging for multi-claimer"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_filename = f"{log_dir}/multi_claim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [%(account)s] - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def load_accounts(self):
        """Load multiple accounts from configuration"""
        try:
            # Try to load from accounts.json
            accounts_file = "config/accounts.json"
            if os.path.exists(accounts_file):
                with open(accounts_file, 'r') as f:
                    accounts_data = json.load(f)
                    self.accounts = accounts_data.get('accounts', [])
            
            # Also check environment variables for multiple accounts
            env_accounts = []
            i = 1
            while True:
                email = os.getenv(f'TOKOPEDIA_EMAIL_{i}')
                password = os.getenv(f'TOKOPEDIA_PASSWORD_{i}')
                
                if not email or not password:
                    break
                
                env_accounts.append({
                    'email': email,
                    'password': password,
                    'name': f'Account_{i}'
                })
                i += 1
            
            # Combine accounts
            self.accounts.extend(env_accounts)
            
            # Add single account from env if no multi accounts found
            if not self.accounts and os.getenv('TOKOPEDIA_EMAIL'):
                self.accounts.append({
                    'email': os.getenv('TOKOPEDIA_EMAIL'),
                    'password': os.getenv('TOKOPEDIA_PASSWORD'),
                    'name': 'Default_Account'
                })
            
            self.logger.info(f"📋 Loaded {len(self.accounts)} accounts")
            
        except Exception as e:
            self.logger.error(f"❌ Error loading accounts: {e}")
            self.accounts = []
    
    def claim_for_account(self, account):
        """Claim vouchers for a single account"""
        account_name = account.get('name', 'Unknown')
        email = account['email']
        password = account['password']
        
        # Create logger adapter for this account
        account_logger = logging.LoggerAdapter(self.logger, {'account': account_name})
        
        result = {
            'account': account_name,
            'email': email,
            'success': False,
            'claimed_vouchers': [],
            'failed_vouchers': [],
            'error': None,
            'start_time': datetime.now(),
            'end_time': None
        }
        
        try:
            account_logger.info("🚀 Starting claim process...")
            
            # Create claimer instance
            claimer = TokopediaVoucherClaimer()
            
            # Set credentials
            os.environ['TOKOPEDIA_EMAIL'] = email
            os.environ['TOKOPEDIA_PASSWORD'] = password
            
            # Run claim process
            success = claimer.run_auto_claim(email, password)
            
            if success:
                result['success'] = True
                result['claimed_vouchers'] = claimer.claimed_vouchers
                result['failed_vouchers'] = claimer.failed_vouchers
                
                account_logger.info(f"✅ Successfully claimed {len(claimer.claimed_vouchers)} vouchers")
            else:
                result['error'] = "Claim process failed"
                account_logger.error("❌ Claim process failed")
            
            # Cleanup
            claimer.cleanup()
            
        except Exception as e:
            result['error'] = str(e)
            account_logger.error(f"❌ Error: {e}")
        
        finally:
            result['end_time'] = datetime.now()
            result['duration'] = (result['end_time'] - result['start_time']).total_seconds()
        
        return result
    
    def run_parallel_claims(self, max_workers=3):
        """Run claim process for all accounts in parallel"""
        if not self.accounts:
            self.logger.error("❌ No accounts found!")
            return False
        
        self.logger.info(f"🚀 Starting parallel claims for {len(self.accounts)} accounts (max_workers: {max_workers})")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_account = {
                executor.submit(self.claim_for_account, account): account 
                for account in self.accounts
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_account):
                account = future_to_account[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    
                    # Log immediate result
                    if result['success']:
                        self.logger.info(f"✅ {result['account']}: {len(result['claimed_vouchers'])} vouchers claimed")
                    else:
                        self.logger.error(f"❌ {result['account']}: {result['error']}")
                        
                except Exception as e:
                    self.logger.error(f"❌ Exception for account {account.get('name', 'Unknown')}: {e}")
        
        # Generate summary report
        self.generate_summary_report()
        return True
    
    def run_sequential_claims(self):
        """Run claim process for all accounts sequentially"""
        if not self.accounts:
            self.logger.error("❌ No accounts found!")
            return False
        
        self.logger.info(f"🚀 Starting sequential claims for {len(self.accounts)} accounts")
        
        for i, account in enumerate(self.accounts, 1):
            self.logger.info(f"📋 Processing account {i}/{len(self.accounts)}: {account.get('name', 'Unknown')}")
            
            result = self.claim_for_account(account)
            self.results.append(result)
            
            # Delay between accounts to avoid detection
            if i < len(self.accounts):
                delay = 30  # 30 seconds delay
                self.logger.info(f"⏳ Waiting {delay} seconds before next account...")
                time.sleep(delay)
        
        # Generate summary report
        self.generate_summary_report()
        return True
    
    def generate_summary_report(self):
        """Generate summary report for all accounts"""
        if not self.results:
            return
        
        total_claimed = sum(len(r['claimed_vouchers']) for r in self.results)
        total_failed = sum(len(r['failed_vouchers']) for r in self.results)
        successful_accounts = sum(1 for r in self.results if r['success'])
        
        report = f"""
📊 MULTI-ACCOUNT CLAIM SUMMARY REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

📈 STATISTICS:
• Total Accounts: {len(self.results)}
• Successful Accounts: {successful_accounts}
• Failed Accounts: {len(self.results) - successful_accounts}
• Total Vouchers Claimed: {total_claimed}
• Total Failed Claims: {total_failed}

{'='*60}

📋 DETAILED RESULTS:
"""
        
        for result in self.results:
            status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
            report += f"""
{status} - {result['account']} ({result['email']})
  └─ Duration: {result['duration']:.2f} seconds
  └─ Claimed: {len(result['claimed_vouchers'])} vouchers
  └─ Failed: {len(result['failed_vouchers'])} vouchers
"""
            
            if result['error']:
                report += f"  └─ Error: {result['error']}\n"
            
            if result['claimed_vouchers']:
                report += "  └─ Claimed Vouchers:\n"
                for voucher in result['claimed_vouchers']:
                    report += f"     • {voucher['title']} - {voucher['discount']}\n"
        
        report += f"\n{'='*60}\n"
        
        # Save report
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        report_filename = f"{data_dir}/multi_claim_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        
        self.logger.info(f"📄 Summary report saved to: {report_filename}")
        print(report)


def main():
    """Main function"""
    print("🎫 Tokopedia Multi-Account Voucher Claimer")
    print("=========================================")
    
    # Check if accounts are configured
    if not os.path.exists("config/accounts.json") and not os.getenv('TOKOPEDIA_EMAIL'):
        print("❌ No accounts configured!")
        print("Please either:")
        print("1. Create config/accounts.json with account details")
        print("2. Set TOKOPEDIA_EMAIL and TOKOPEDIA_PASSWORD environment variables")
        print("3. Set TOKOPEDIA_EMAIL_1, TOKOPEDIA_PASSWORD_1, etc. for multiple accounts")
        return
    
    # Initialize multi-claimer
    claimer = MultiAccountClaimer()
    
    if not claimer.accounts:
        print("❌ No accounts found!")
        return
    
    print(f"📋 Found {len(claimer.accounts)} accounts")
    
    # Choose execution mode
    print("\nExecution Mode:")
    print("1. Parallel (faster, but higher risk)")
    print("2. Sequential (slower, but safer)")
    
    try:
        choice = input("Choose mode (1 or 2) [default: 2]: ").strip()
        if not choice:
            choice = "2"
        
        if choice == "1":
            # Parallel mode
            max_workers = min(len(claimer.accounts), 3)
            print(f"🚀 Running in parallel mode (max_workers: {max_workers})")
            success = claimer.run_parallel_claims(max_workers)
        else:
            # Sequential mode
            print("🚀 Running in sequential mode")
            success = claimer.run_sequential_claims()
        
        if success:
            print("✅ Multi-account claim process completed!")
        else:
            print("❌ Multi-account claim process failed!")
            
    except KeyboardInterrupt:
        print("⚠️  Process stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()