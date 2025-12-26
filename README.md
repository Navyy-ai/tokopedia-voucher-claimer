# 🎫 Tokopedia Voucher Auto Claimer - Termux Edition

Script otomatis untuk mengklaim voucher Tokopedia menggunakan Termux. Script ini dirancang untuk memudahkan pengguna dalam mendapatkan voucher-voucher yang tersedia di Tokopedia secara otomatis.

## 🚀 Fitur

- ✅ Auto-login ke akun Tokopedia
- 🔍 Scan otomatis voucher yang tersedia
- 🎯 Klaim voucher secara otomatis
- 📊 Generate laporan hasil klaim
- 🛡️ Anti-detection dengan delay random
- 📱 Mobile view untuk compatibility Termux
- 📝 Logging lengkap untuk troubleshooting
- ⚙️ Konfigurasi mudah dengan file .env

## 📋 Persyaratan

- Android device dengan Termux terinstall
- Python 3.7+ 
- Koneksi internet yang stabil
- Akun Tokopedia yang aktif

## 📦 Cara Install

### 1. Install Termux
Download Termux dari F-Droid (direkomendasikan) atau dari GitHub Releases.

### 2. Clone repository
```bash
pkg install git
git clone https://github.com/username/tokopedia-voucher-claimer.git
cd tokopedia-voucher-claimer
```

### 3. Run installation script
```bash
chmod +x install.sh
./install.sh
```

### 4. Konfigurasi kredensial
```bash
# Copy file konfigurasi
cp config/.env.example .env

# Edit file .env dengan text editor
nano .env
```

Isi dengan email dan password Tokopedia Anda:
```
TOKOPEDIA_EMAIL=email_anda@example.com
TOKOPEDIA_PASSWORD=password_anda
```

## 🎮 Cara Penggunaan

### Method 1: Direct Run
```bash
./run.sh
```

### Method 2: Python Direct
```bash
python3 src/voucher_claimer.py
```

### Method 3: With Environment Variables
```bash
export TOKOPEDIA_EMAIL="email_anda@example.com"
export TOKOPEDIA_PASSWORD="password_anda"
python3 src/voucher_claimer.py
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