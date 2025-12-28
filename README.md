# 🎫 Tokopedia Voucher Auto Claimer - Termux Edition

Script otomatis untuk mengklaim voucher Tokopedia menggunakan Termux. Script ini dirancang untuk memudahkan pengguna dalam mendapatkan voucher-voucher yang tersedia di Tokopedia secara otomatis, dengan fitur khusus untuk target voucher tertentu seperti "Belanjaanmu Dibayarin Tokopedia".

## 🚀 Fitur

- ✅ Auto-login ke akun Tokopedia
- 🔍 Scan otomatis voucher yang tersedia
- 🎯 **Target Voucher Detection** - Deteksi khusus untuk voucher target
- 🎯 **Priority Claiming** - Klaim voucher target terlebih dahulu
- 🔔 **Target Alerts** - Notifikasi khusus saat voucher target ditemukan
- 📊 Generate laporan hasil klaim
- 🛡️ Anti-detection dengan delay random
- 📱 Mobile view untuk compatibility Termux
- 📝 Logging lengkap untuk troubleshooting
- ⚙️ Konfigurasi mudah dengan file .env
- 👥 Multi-account support

## 📋 Persyaratan

### Untuk Termux (Android)
- Android device dengan Termux terinstall
- Python 3.7+ 
- Koneksi internet yang stabil
- Akun Tokopedia yang aktif

### Untuk PC (Windows/macOS/Linux)
- Python 3.7+ 
- Browser modern (Chrome, Firefox, atau Edge)
- Koneksi internet yang stabil
- Akun Tokopedia yang aktif
- (Opsional) Git untuk cloning

## 📦 Cara Install

### 🖥️ Untuk PC (Windows/macOS/Linux)

#### Method 1: Automated Installation (Recommended)

**Windows:**
```cmd
# Download atau clone repository
git clone https://github.com/Navyy-ai/tokopedia-voucher-claimer.git
cd tokopedia-voucher-claimer

# Run automated installer
setup_windows.bat
```

**macOS/Linux:**
```bash
# Download atau clone repository
git clone https://github.com/Navyy-ai/tokopedia-voucher-claimer.git
cd tokopedia-voucher-claimer

# Make script executable
chmod +x setup_pc.sh

# Run automated installer
./setup_pc.sh
```

#### Method 2: Manual Installation

1. **Install Python 3.7+**
   - **Windows:** Download dari https://www.python.org/downloads/
   - **macOS:** `brew install python3`
   - **Linux:** `sudo apt install python3 python3-pip`

2. **Install Browser**
   - **Chrome:** https://www.google.com/chrome/
   - **Firefox:** https://www.mozilla.org/firefox/
   - **Edge:** https://www.microsoft.com/edge/

3. **Clone Repository**
   ```bash
   git clone https://github.com/Navyy-ai/tokopedia-voucher-claimer.git
   cd tokopedia-voucher-claimer
   ```

4. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   
   # Windows
   venv\Scripts\activate.bat
   
   # macOS/Linux
   source venv/bin/activate
   ```

5. **Install Dependencies**
   ```bash
   pip install -r requirements_pc.txt
   ```

6. **Setup Configuration**
   ```bash
   # Copy configuration file
   cp config/.env.example .env
   
   # Edit dengan credentials Anda
   # Windows: notepad .env
   # macOS/Linux: nano .env
   ```

### 📱 Untuk Termux (Android)

#### 1. Install Termux
Download Termux dari F-Droid (direkomendasikan) atau dari GitHub Releases.

#### 2. Clone repository
```bash
pkg install git
git clone https://github.com/Navyy-ai/tokopedia-voucher-claimer.git
cd tokopedia-voucher-claimer
```

#### 3. Run installation script
```bash
chmod +x install.sh
./install.sh
```

#### 4. Konfigurasi kredensial
```bash
# Copy file konfigurasi
cp config/.env.example .env

# Edit file .env dengan text editor
nano .env
```

### 🔐 Konfigurasi Kredensial (Untuk Semua Platform)

Isi dengan email dan password Tokopedia Anda:
```bash
TOKOPEDIA_EMAIL=email_anda@example.com
TOKOPEDIA_PASSWORD=password_anda
```

### 🔧 Additional PC Configuration

Untuk PC, Anda bisa mengatur browser dan mode eksekusi di file `.env`:
```bash
# Browser choice (chrome, firefox, edge)
BROWSER_TYPE=chrome

# Headless mode (true/false) - false akan membuka browser GUI
HEADLESS_MODE=true

# Window size untuk non-headless mode
WINDOW_WIDTH=1280
WINDOW_HEIGHT=720
```

## 🎮 Cara Penggunaan

### 🖥️ PC Usage

#### Method 1: Using Launch Scripts (Recommended)

**Windows:**
```cmd
# Activate virtual environment
venv\Scripts\activate.bat

# Run launcher
start_claimer.bat          # Regular voucher claimer
start_target_claimer.bat   # Target voucher claimer
start_monitor.bat          # Voucher monitor
```

**macOS/Linux:**
```bash
# Activate virtual environment
source venv/bin/activate

# Run launcher
./start_claimer.sh          # Regular voucher claimer
./start_target_claimer.sh   # Target voucher claimer
./start_monitor.sh          # Voucher monitor
```

#### Method 2: Direct Python Execution

**Windows:**
```cmd
venv\Scripts\activate.bat
python src\voucher_claimer.py
python src\target_claimer.py
python src\monitor.py
```

**macOS/Linux:**
```bash
source venv/bin/activate
python src/voucher_claimer.py
python src/target_claimer.py
python src/monitor.py
```

#### Method 3: Interactive Menu
```bash
source venv/bin/activate  # Windows: venv\Scripts\activate.bat
python run.py
```

### 📱 Termux Usage

#### Method 1: Direct Run
```bash
./run.sh
```

#### Method 2: Python Direct
```bash
python3 src/voucher_claimer.py
```

#### Method 3: With Environment Variables
```bash
export TOKOPEDIA_EMAIL="email_anda@example.com"
export TOKOPEDIA_PASSWORD="password_anda"
python3 src/voucher_claimer.py
```

### 🔧 Platform-Specific Features

#### PC Only Features:
- **GUI Browser Mode**: Set `HEADLESS_MODE=false` untuk melihat browser berjalan
- **Multiple Browser Support**: Chrome, Firefox, Edge
- **Desktop Shortcuts**: Automatic creation (Windows/Linux)
- **Virtual Environment**: Isolated Python environment

#### Termux Only Features:
- **Mobile View**: Optimized for mobile user agent
- **Chromium Browser**: Uses Termux-optimized Chromium
- **Battery Saving**: Lightweight resource usage

## 🎯 Target Voucher Configuration

Script ini mendukung konfigurasi untuk voucher target tertentu, seperti "Belanjaanmu Dibayarin Tokopedia".

### Setup Target Voucher

Edit file `config/target_voucher.json`:

```json
{
  "target_vouchers": [
    {
      "name": "Belanjaanmu Dibayarin Tokopedia",
      "keywords": [
        "Belanjaanmu Dibayarin",
        "Belanjaanmu dibayarin",
        "dibayarin tokopedia",
        "Dibayarin Tokopedia"
      ],
      "priority": 1,
      "enabled": true,
      "auto_claim": true,
      "notification": {
        "enabled": true,
        "sound": true,
        "message": "TARGET VOUCHER FOUND!"
      }
    }
  ],
  "settings": {
    "scan_mode": "targeted",
    "priority_claim": true,
    "retry_on_fail": true,
    "max_retries": 5
  }
}
```

### Fitur Target Voucher

- **Priority Claiming**: Voucher target akan diklaim terlebih dahulu
- **Keyword Matching**: Deteksi berdasarkan kata kunci yang dikonfigurasi
- **Special Alerts**: Notifikasi khusus saat voucher target ditemukan
- **Dedicated Reports**: Pemisahan laporan untuk target dan regular voucher

### Menambahkan Target Voucher Baru

Tambahkan entry baru di `config/target_voucher.json`:

```json
{
  "name": "Nama Voucher Baru",
  "keywords": ["keyword1", "keyword2"],
  "priority": 1,
  "enabled": true,
  "auto_claim": true,
  "notification": {
    "enabled": true,
    "sound": true,
    "message": "VOUCHER DITEMUKAN!"
  }
}
```

## ⚙️ Konfigurasi

Edit file `.env` untuk mengatur pengaturan:

```bash
# Account Credentials
TOKOPEDIA_EMAIL=your_email@example.com
TOKOPEDIA_PASSWORD=your_password

# Claimer Settings
CLAIM_DELAY_MIN=2          # Minimum delay between claims (seconds)
CLAIM_DELAY_MAX=5          # Maximum delay between claims (seconds)
MAX_RETRY_ATTEMPTS=3       # Maximum retry attempts for failed claims

# Browser Settings
HEADLESS_MODE=true         # Run browser in headless mode
BROWSER_TIMEOUT=30         # Browser timeout in seconds

# Logging Settings
LOG_LEVEL=INFO            # Logging level (DEBUG, INFO, WARNING, ERROR)
SAVE_REPORTS=true         # Save claim reports to data/ directory
```

## 📁 Struktur Direktori

```
tokopedia-voucher-claimer/
├── src/
│   └── voucher_claimer.py    # Main script
├── config/
│   └── .env.example         # Example configuration
├── logs/                    # Log files
├── data/                    # Claim reports
├── install.sh              # Installation script
├── run.sh                  # Runner script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Troubleshooting

### Common Issues

1. **Login Gagal**
   - Pastikan email dan password benar
   - Cek apakah ada captcha atau 2FA
   - Verifikasi akun tidak diblokir

2. **Browser Error**
   - Install ulang chromium: `pkg install chromium`
   - Cek koneksi internet
   - Restart Termux

3. **Dependencies Error**
   - Run installation script ulang: `./install.sh`
   - Update pip: `pip install --upgrade pip`
   - Install manual: `pip install -r requirements.txt`

4. **Permission Denied**
   ```bash
   chmod +x install.sh run.sh src/voucher_claimer.py
   ```

### Debug Mode

Aktifkan debug logging dengan mengubah `.env`:
```
LOG_LEVEL=DEBUG
```

### Logs Location
- Activity logs: `logs/voucher_claim_YYYYMMDD_HHMMSS.log`
- Claim reports: `data/claim_report_YYYYMMDD_HHMMSS.txt`

## ⚠️ Disclaimer

- Script ini dibuat untuk tujuan edukasi saja
- Gunakan dengan resiko Anda sendiri
- Saya tidak bertanggung jawab atas penyalahgunaan
- Resiko akun terblokir tetap ada
- Gunakan dengan bijak dan sesuai ToS Tokopedia

## 🛡️ Safety Tips

1. **Gunakan akun cadangan** untuk testing terlebih dahulu
2. **Jangan terlalu sering** menjalankan script
3. **Monitor logs** untuk aktivitas mencurigakan
4. **Backup data** akun Anda secara berkala
5. **Stop script** jika ada aktivitas tidak normal

## 🔄 Update Script

Untuk update ke versi terbaru:
```bash
git pull origin main
./install.sh
```

## 📞 Support

Jika mengalami masalah:
1. Cek logs di `logs/` directory
2. Baca troubleshooting section
3. Search issue di GitHub
4. Create new issue dengan detail error

## 🤝 Kontribusi

Contributions are welcome! Silahkan:
1. Fork repository
2. Create feature branch
3. Submit pull request

## 📝 Changelog

### v1.0.0
- Initial release
- Auto-login functionality
- Voucher scanning and claiming
- Mobile view support
- Logging and reporting

---

**Made with ❤️ for Termux Users**

*Happy Voucher Hunting! 🎫*