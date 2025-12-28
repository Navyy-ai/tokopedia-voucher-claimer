@echo off
REM Tokopedia Voucher Claimer - Windows Setup Script (FIXED VERSION)
REM Automated installation for Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║      TOKOPEDIA VOUCHER CLAIMER - WINDOWS SETUP              ║
echo ║                  Automated Installer                        ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.7+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

python --version
echo ✅ Python found
echo.

REM Check pip
echo [2/6] Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found!
    echo.
    echo Please ensure pip is installed with Python.
    pause
    exit /b 1
)

pip --version
echo ✅ pip found
echo.

REM Create virtual environment
echo [3/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip
echo ✅ pip upgraded
echo.

REM Fix requirements_pc.txt
echo [5/6] Installing Python dependencies...
echo Checking and fixing requirements_pc.txt...

if exist "requirements_pc.txt" (
    findstr /C:"platform==1.0.8" requirements_pc.txt >nul 2>&1
    if %errorlevel% equ 0 (
        echo Removing invalid platform package...
        powershell -Command "(Get-Content requirements_pc.txt) -replace 'platform==1\.0\.8[^\r\n]*[\r\n]*', '' | Where-Object { $_.Trim() -ne '' } | Set-Content requirements_pc.txt"
        echo ✅ Fixed requirements_pc.txt
    ) else (
        echo ✅ requirements_pc.txt is correct
    )
) else (
    echo ⚠️  requirements_pc.txt not found, using manual installation
    goto manual_install
)

echo Installing requirements for PC...
pip install requests beautifulsoup4 selenium webdriver-manager lxml python-dotenv colorama psutil packaging
echo.
echo ✅ Dependencies installed
echo.
goto install_complete

:manual_install
echo Installing dependencies manually...
pip install requests beautifulsoup4 selenium webdriver-manager lxml python-dotenv colorama psutil packaging
echo.
echo ✅ Dependencies installed
echo.

:install_complete

REM Create directories
echo Creating directories...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "backups" mkdir backups
echo ✅ Directories created
echo.

REM Create configuration files
echo Setting up configuration...
if not exist ".env" (
    copy config\.env.example .env
    echo ✅ Created .env file
    echo.
    echo ⚠️  Please edit .env file with your Tokopedia credentials:
    echo     TOKOPEDIA_EMAIL=your_email@example.com
    echo     TOKOPEDIA_PASSWORD=your_password
    echo.
) else (
    echo ✅ .env file already exists
)

if not exist "config\accounts.json" (
    copy config\accounts.json.example config\accounts.json
    echo ✅ Created accounts.json example
)

if not exist "config\target_voucher.json" (
    echo ✅ target_voucher.json already exists
)

REM Create Windows-specific launcher
echo Creating Windows launcher...
echo @echo off > start_claimer.bat
echo cd /d "%cd%" >> start_claimer.bat
echo call venv\Scripts\activate.bat >> start_claimer.bat
echo python src\voucher_claimer.py >> start_claimer.bat
echo pause >> start_claimer.bat

echo @echo off > start_target_claimer.bat
echo cd /d "%cd%" >> start_target_claimer.bat
echo call venv\Scripts\activate.bat >> start_target_claimer.bat
echo python src\target_claimer.py >> start_target_claimer.bat
echo pause >> start_target_claimer.bat

echo @echo off > start_monitor.bat
echo cd /d "%cd%" >> start_monitor.bat
echo call venv\Scripts\activate.bat >> start_monitor.bat
echo python src\monitor.py >> start_monitor.bat
echo pause >> start_monitor.bat

echo @echo off > run_menu.bat
echo cd /d "%cd%" >> run_menu.bat
echo call venv\Scripts\activate.bat >> run_menu.bat
echo python run.py >> run_menu.bat
echo pause >> run_menu.bat

echo ✅ Windows launchers created
echo.

REM Test installation
echo Testing installation...
python -c "import requests, selenium, bs4; import sys; sys.path.insert(0, 'src'); import platform_utils" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Installation test failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo ✅ Installation test passed
echo.

REM Installation complete
echo ════════════════════════════════════════════════════════════
echo ✅ Installation completed successfully!
echo ════════════════════════════════════════════════════════════
echo.
echo 📋 Next steps:
echo 1. Edit .env file with your Tokopedia credentials
echo    (Double-click .env file to edit)
echo.
echo 2. Run one of these launchers:
echo    - run_menu.bat              (Interactive menu - Recommended)
echo    - start_claimer.bat        (Regular voucher claimer)
echo    - start_target_claimer.bat (Target voucher claimer)
echo    - start_monitor.bat        (Voucher monitor)
echo.
echo 3. Or run via Command Prompt:
echo    venv\Scripts\activate.bat
echo    python run.py
echo.
echo 📚 Documentation: README.md
echo 📄 Logs: logs\ directory
echo 📊 Reports: data\ directory
echo.
echo ⚠️  Disclaimer: Use at your own risk
echo    This script is for educational purposes only
echo.
pause