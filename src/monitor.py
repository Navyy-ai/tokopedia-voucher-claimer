#!/usr/bin/env python3
"""
Tokopedia Voucher Monitor
Script untuk monitoring voucher baru secara berkala
"""

import time
import os
import sys
import logging
from datetime import datetime, timedelta
from voucher_claimer import TokopediaVoucherClaimer
import json

class VoucherMonitor:
    def __init__(self):
        self.claimer = None
        self.monitored_vouchers = []
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self):
        """Load monitoring configuration"""
        default_config = {
            'check_interval': 300,  # 5 minutes
            'max_checks': 100,      # Maximum checks per session
            'auto_claim': True,     # Auto-claim new vouchers
            'notification': True    # Enable notifications
        }
        
        # Load from file if exists
        config_file = "config/monitor_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except:
                pass
        
        return default_config
    
    def setup_logging(self):
        """Setup logging for monitor"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_filename = f"{log_dir}/monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def initialize_claimer(self):
        """Initialize voucher claimer"""
        try:
            self.claimer = TokopediaVoucherClaimer()
            
            # Load credentials
            email = os.getenv('TOKOPEDIA_EMAIL')
            password = os.getenv('TOKOPEDIA_PASSWORD')
            
            if not email or not password:
                self.logger.error("❌ Credentials not found in environment variables")
                return False
            
            # Login
            if not self.claimer.login_tokopedia(email, password):
                self.logger.error("❌ Login failed")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing claimer: {e}")
            return False
    
    def get_current_vouchers(self):
        """Get current list of vouchers"""
        try:
            # Navigate to voucher page
            self.claimer.find_voucher_page()
            
            # Scan vouchers
            vouchers = self.claimer.scan_available_vouchers()
            
            # Create simple list for comparison
            voucher_list = []
            for voucher in vouchers:
                voucher_list.append({
                    'title': voucher['title'],
                    'discount': voucher['discount'],
                    'expiry': voucher['expiry'],
                    'claimed': voucher['claimed']
                })
            
            return voucher_list
            
        except Exception as e:
            self.logger.error(f"❌ Error getting current vouchers: {e}")
            return []
    
    def compare_vouchers(self, old_vouchers, new_vouchers):
        """Compare old and new voucher lists"""
        new_found = []
        
        # Convert to sets for comparison
        old_set = set()
        for v in old_vouchers:
            key = f"{v['title']}|{v['discount']}|{v['expiry']}"
            old_set.add(key)
        
        # Find new vouchers
        for v in new_vouchers:
            key = f"{v['title']}|{v['discount']}|{v['expiry']}"
            if key not in old_set:
                new_found.append(v)
        
        return new_found
    
    def claim_new_vouchers(self, new_vouchers):
        """Claim newly found vouchers"""
        if not new_vouchers:
            return
        
        self.logger.info(f"🎯 Found {len(new_vouchers)} new vouchers!")
        
        for voucher in new_vouchers:
            try:
                # Re-scan vouchers to get fresh element references
                current_vouchers = self.claimer.scan_available_vouchers()
                
                # Find matching voucher
                for cv in current_vouchers:
                    if (cv['title'] == voucher['title'] and 
                        cv['discount'] == voucher['discount'] and
                        not cv['claimed']):
                        
                        success = self.claimer.claim_voucher(cv)
                        if success:
                            self.logger.info(f"✅ Successfully claimed new voucher: {voucher['title']}")
                        else:
                            self.logger.warning(f"⚠️  Failed to claim: {voucher['title']}")
                        break
                
                # Delay between claims
                time.sleep(3)
                
            except Exception as e:
                self.logger.error(f"❌ Error claiming voucher {voucher['title']}: {e}")
    
    def save_monitored_data(self, vouchers):
        """Save monitored voucher data"""
        try:
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            filename = f"{data_dir}/monitored_vouchers_{datetime.now().strftime('%Y%m%d')}.json"
            
            data = {
                'timestamp': datetime.now().isoformat(),
                'vouchers': vouchers,
                'total_count': len(vouchers),
                'unclaimed_count': len([v for v in vouchers if not v['claimed']])
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            self.logger.error(f"❌ Error saving monitored data: {e}")
    
    def run_monitoring(self):
        """Main monitoring loop"""
        self.logger.info("🔍 Starting voucher monitoring...")
        
        # Initialize claimer
        if not self.initialize_claimer():
            return False
        
        # Get initial voucher list
        self.logger.info("📋 Getting initial voucher list...")
        current_vouchers = self.get_current_vouchers()
        self.monitored_vouchers = current_vouchers
        
        self.logger.info(f"📊 Monitoring {len(current_vouchers)} vouchers")
        self.save_monitored_data(current_vouchers)
        
        check_count = 0
        
        try:
            while check_count < self.config['max_checks']:
                check_count += 1
                self.logger.info(f"🔄 Check #{check_count} - Waiting {self.config['check_interval']} seconds...")
                
                # Wait for next check
                time.sleep(self.config['check_interval'])
                
                # Get new voucher list
                new_vouchers = self.get_current_vouchers()
                
                # Compare with previous
                newly_found = self.compare_vouchers(self.monitored_vouchers, new_vouchers)
                
                if newly_found:
                    self.logger.info(f"🎉 {len(newly_found)} new vouchers found!")
                    
                    # Save updated list
                    self.monitored_vouchers = new_vouchers
                    
                    # Auto-claim if enabled
                    if self.config['auto_claim']:
                        self.claim_new_vouchers(newly_found)
                    
                    # Save monitored data
                    self.save_monitored_data(new_vouchers)
                    
                    # Send notification (placeholder)
                    if self.config['notification']:
                        self.send_notification(newly_found)
                else:
                    self.logger.info("📭 No new vouchers found")
                
        except KeyboardInterrupt:
            self.logger.info("⚠️  Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Error in monitoring loop: {e}")
        
        finally:
            # Cleanup
            if self.claimer:
                self.claimer.cleanup()
        
        return True
    
    def send_notification(self, new_vouchers):
        """Send notification about new vouchers (placeholder)"""
        try:
            message = f"🎫 {len(new_vouchers)} new vouchers found!\n\n"
            for voucher in new_vouchers:
                message += f"• {voucher['title']} - {voucher['discount']}\n"
            
            # In a real implementation, you could:
            # - Send email notification
            # - Send Telegram message
            # - Send push notification
            # - Play sound
            
            self.logger.info(f"📢 Notification: {message}")
            
        except Exception as e:
            self.logger.error(f"❌ Error sending notification: {e}")


def main():
    """Main function"""
    print("🔍 Tokopedia Voucher Monitor")
    print("=============================")
    
    # Check credentials
    email = os.getenv('TOKOPEDIA_EMAIL')
    password = os.getenv('TOKOPEDIA_PASSWORD')
    
    if not email or not password:
        print("❌ Please set TOKOPEDIA_EMAIL and TOKOPEDIA_PASSWORD environment variables")
        return
    
    # Initialize and run monitor
    monitor = VoucherMonitor()
    
    try:
        success = monitor.run_monitoring()
        
        if success:
            print("✅ Monitoring completed successfully!")
        else:
            print("❌ Monitoring failed!")
            
    except KeyboardInterrupt:
        print("⚠️  Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()