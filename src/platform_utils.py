#!/usr/bin/env python3
"""
Platform Detection and Utilities
Multi-platform support for Tokopedia Voucher Claimer
"""

import os
import sys
import platform
import subprocess
import json
from typing import Dict, List, Optional, Tuple

class PlatformDetector:
    """Detect current platform and provide platform-specific utilities"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        self.python_version = platform.python_version()
        self.is_termux = self._detect_termux()
        
    def _detect_termux(self) -> bool:
        """Detect if running in Termux environment"""
        return (
            os.path.exists("/data/data/com.termux") or
            "termux" in os.environ.get("PREFIX", "").lower() or
            "com.termux" in os.environ.get("ANDROID_ROOT", "")
        )
    
    def get_platform_info(self) -> Dict[str, str]:
        """Get comprehensive platform information"""
        return {
            "system": self.system,
            "machine": self.machine,
            "python_version": self.python_version,
            "is_termux": self.is_termux,
            "is_windows": self.system == "windows",
            "is_macos": self.system == "darwin", 
            "is_linux": self.system == "linux" and not self.is_termux,
            "is_64bit": "64" in self.machine or "amd64" in self.machine,
        }
    
    def get_supported_browsers(self) -> List[str]:
        """Get list of supported browsers for current platform"""
        browsers = []
        
        if self.system == "windows":
            browsers.extend(["chrome", "chromium", "firefox", "edge"])
        elif self.system == "darwin":
            browsers.extend(["chrome", "chromium", "firefox", "safari"])
        elif self.system == "linux":
            browsers.extend(["chrome", "chromium", "firefox"])
        elif self.is_termux:
            browsers.extend(["chrome", "chromium"])
        
        return browsers
    
    def check_browser_installed(self, browser_name: str) -> bool:
        """Check if specific browser is installed"""
        try:
            if self.system == "windows":
                return self._check_windows_browser(browser_name)
            elif self.system == "darwin":
                return self._check_macos_browser(browser_name)
            elif self.system == "linux":
                return self._check_linux_browser(browser_name)
            elif self.is_termux:
                return self._check_termux_browser(browser_name)
        except:
            return False
        return False
    
    def _check_windows_browser(self, browser_name: str) -> bool:
        """Check browser on Windows"""
        browser_paths = {
            "chrome": [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv("USERNAME", ""))
            ],
            "firefox": [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
            ],
            "edge": [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            ],
            "chromium": [
                r"C:\Program Files\Chromium\Application\chrome.exe",
                r"C:\Program Files (x86)\Chromium\Application\chrome.exe"
            ]
        }
        
        paths = browser_paths.get(browser_name.lower(), [])
        return any(os.path.exists(path) for path in paths)
    
    def _check_macos_browser(self, browser_name: str) -> bool:
        """Check browser on macOS"""
        try:
            result = subprocess.run(
                ["mdfind", f"kMDItemDisplayName == '{browser_name}' && kMDItemKind == 'Application'"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0 and len(result.stdout.strip()) > 0
        except:
            return False
    
    def _check_linux_browser(self, browser_name: str) -> bool:
        """Check browser on Linux"""
        try:
            commands = {
                "chrome": ["google-chrome", "--version"],
                "chromium": ["chromium-browser", "--version"],
                "firefox": ["firefox", "--version"]
            }
            
            cmd = commands.get(browser_name.lower())
            if cmd:
                result = subprocess.run(cmd, capture_output=True, timeout=10)
                return result.returncode == 0
        except:
            return False
        return False
    
    def _check_termux_browser(self, browser_name: str) -> bool:
        """Check browser on Termux"""
        try:
            commands = {
                "chrome": ["chromium", "--version"],
                "chromium": ["chromium", "--version"]
            }
            
            cmd = commands.get(browser_name.lower())
            if cmd:
                result = subprocess.run(cmd, capture_output=True, timeout=10)
                return result.returncode == 0
        except:
            return False
        return False
    
    def get_default_browser(self) -> Optional[str]:
        """Get default browser for current platform"""
        supported = self.get_supported_browsers()
        
        # Priority order
        priority = ["chrome", "chromium", "firefox", "edge", "safari"]
        
        for browser in priority:
            if browser in supported and self.check_browser_installed(browser):
                return browser
        
        # Return first available
        for browser in supported:
            if self.check_browser_installed(browser):
                return browser
        
        return None
    
    def get_installation_commands(self, browser_name: str) -> List[str]:
        """Get installation commands for browser"""
        commands = []
        
        if self.system == "windows":
            commands.append(f"# Download {browser_name} from official website")
            if browser_name == "chrome":
                commands.append("# https://www.google.com/chrome/")
            elif browser_name == "firefox":
                commands.append("# https://www.mozilla.org/firefox/")
            elif browser_name == "edge":
                commands.append("# https://www.microsoft.com/edge/")
                
        elif self.system == "darwin":
            if browser_name in ["chrome", "firefox"]:
                commands.append(f"brew install --cask {browser_name}")
            else:
                commands.append(f"# Download {browser_name} from official website")
                
        elif self.system == "linux":
            distro = self._get_linux_distro()
            if distro in ["ubuntu", "debian"]:
                if browser_name == "chrome":
                    commands.extend([
                        "wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -",
                        "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list",
                        "sudo apt update",
                        "sudo apt install google-chrome-stable"
                    ])
                elif browser_name == "firefox":
                    commands.append("sudo apt install firefox")
                elif browser_name == "chromium":
                    commands.append("sudo apt install chromium-browser")
                    
            elif distro in ["fedora", "centos", "rhel"]:
                if browser_name == "chrome":
                    commands.append("sudo dnf install google-chrome-stable")
                elif browser_name == "firefox":
                    commands.append("sudo dnf install firefox")
                elif browser_name == "chromium":
                    commands.append("sudo dnf install chromium")
                    
        elif self.is_termux:
            commands.append("pkg install chromium")
        
        return commands
    
    def _get_linux_distro(self) -> str:
        """Get Linux distribution name"""
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("ID="):
                        return line.split("=")[1].strip().strip('"')
        except:
            pass
        return "unknown"
    
    def get_python_install_command(self) -> str:
        """Get Python installation command for current platform"""
        if self.system == "windows":
            return "# Download Python from https://www.python.org/downloads/"
        elif self.system == "darwin":
            return "brew install python3"
        elif self.system == "linux":
            distro = self._get_linux_distro()
            if distro in ["ubuntu", "debian"]:
                return "sudo apt install python3 python3-pip"
            elif distro in ["fedora", "centos", "rhel"]:
                return "sudo dnf install python3 python3-pip"
            else:
                return "# Use your distribution's package manager to install python3"
        elif self.is_termux:
            return "pkg install python python-pip"
        else:
            return "# Please install Python 3.7+ manually"
    
    def get_platform_specific_user_agent(self) -> str:
        """Get appropriate user agent for current platform"""
        if self.is_termux:
            return "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
        elif self.system == "windows":
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        elif self.system == "darwin":
            return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        elif self.system == "linux":
            return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        else:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def main():
    """Test platform detection"""
    detector = PlatformDetector()
    
    print("🖥️  Platform Detection Results:")
    print("=" * 50)
    
    info = detector.get_platform_info()
    for key, value in info.items():
        print(f"{key:20}: {value}")
    
    print("\n🌐 Browser Detection:")
    print("=" * 50)
    
    supported_browsers = detector.get_supported_browsers()
    print(f"Supported browsers: {', '.join(supported_browsers)}")
    
    default_browser = detector.get_default_browser()
    if default_browser:
        print(f"Default browser: {default_browser}")
        print(f"Browser installed: {detector.check_browser_installed(default_browser)}")
    else:
        print("No suitable browser found")
    
    print(f"\nPlatform user agent: {detector.get_platform_specific_user_agent()}")


if __name__ == "__main__":
    main()