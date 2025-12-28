# 🔧 Windows Installation Fix Guide

## Masalah Umum: "ERROR: No matching distribution found for platform==1.0.8"

### ✅ Solusi Cepat (Recommended)

#### Metode 1: Gunakan Setup Script yang Sudah Di-Fixed
```cmd
# Langsung jalankan setup script yang sudah diperbaiki
setup_windows.bat
```

#### Metode 2: Edit Manual requirements_pc.txt
1. Buka file `requirements_pc.txt` dengan Notepad:
   ```cmd
   notepad requirements_pc.txt
   ```

2. Hapus baris ini:
   ```
   platform==1.0.8
   ```

3. Save dan jalankan installer:
   ```cmd
   setup_windows.bat
   ```

#### Metode 3: Manual Installation
```cmd
# Buat virtual environment
python -m venv venv

# Aktifkan
venv\Scripts\activate.bat

# Install dependencies tanpa file requirements
pip install requests beautifulsoup4 selenium webdriver-manager lxml python-dotenv colorama psutil packaging

# Test installation
python -c "import requests, selenium, bs4; import sys; sys.path.insert(0, 'src'); import platform_utils; print('Installation successful!')"
```

## 🧪 Verification Steps

Setelah installation:

```cmd
# 1. Aktifkan virtual environment
venv\Scripts\activate.bat

# 2. Test imports
python -c "import requests, selenium, bs4; import sys; sys.path.insert(0, 'src'); import platform_utils; print('All imports OK!')"

# 3. Test platform detection
python src\platform_utils.py

# 4. Test main application
python run.py
```

## 🚀 Setelah Berhasil

```cmd
# Jalankan launcher scripts:
run_menu.bat              # Interactive menu (Recommended)
start_claimer.bat        # Regular claimer
start_target_claimer.bat # Target voucher claimer
```

## 🔍 Troubleshooting Lengkap

### Issue 1: "ModuleNotFoundError: No module named 'selenium'"
```cmd
pip install selenium webdriver-manager
```

### Issue 2: "ModuleNotFoundError: No module named 'platform_utils'"
Ini adalah error normal karena module berada di folder src:
```cmd
# Tidak perlu install via pip
# Import dengan cara ini:
import sys
sys.path.insert(0, 'src')
import platform_utils
```

### Issue 3: Virtual Environment Error
```cmd
# Delete dan recreate
rmdir /s venv
python -m venv venv
venv\Scripts\activate.bat
pip install requests beautifulsoup4 selenium webdriver-manager lxml python-dotenv colorama psutil packaging
```

### Issue 4: Browser Error
```cmd
# Install browser
# Chrome: https://www.google.com/chrome/
# Firefox: https://www.mozilla.org/firefox/
# Edge: https://www.microsoft.com/edge/

# Test browser detection
python run.py
# Pilih menu 6: Platform Info
# Pilih menu 7: Browser Test
```

## 📝 Checklist Sebelum Menjalankan

- [ ] Python 3.7+ sudah terinstall
- [ ] pip sudah terinstall
- [ ] Virtual environment sudah dibuat dan diaktifkan
- [ ] Dependencies sudah terinstall
- [ ] Browser (Chrome/Firefox/Edge) sudah terinstall
- [ ] File .env sudah dikonfigurasi dengan credentials
- [ ] Test installation berhasil

## 💡 Tips Tambahan

1. **Jalankan sebagai Administrator** jika mengalami permission error
2. **Matikan antivirus** sementara jika installation blocked
3. **Gunakan Command Prompt** bukan PowerShell untuk script .bat
4. **Pastikan koneksi internet stabil** saat installing dependencies
5. **Restart Command Prompt** setelah editing requirements file

## 📞 Masih Ada Masalah?

1. Cek file logs di `logs\` directory
2. Run `python run.py` dan pilih "Platform Info" untuk debugging
3. Baca error message dengan teliti
4. Report issue di GitHub dengan detail error

**Status Script: FIXED ✅** - Semua error installation sudah diperbaiki