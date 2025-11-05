# integrity_monitor.py

import os
import hashlib
import json
import logging
from datetime import datetime

# --- Konfigurasi ---
SECURE_FOLDER = './secure_files/'
HASH_DB_FILE = 'hash_db.json'
LOG_FILE = 'security.log'

def setup_logging():
    """
    Mengkonfigurasi sistem logging untuk menulis ke file dan menampilkan di konsol.
    """
    # Menghapus handler yang ada untuk mencegah duplikasi log jika fungsi ini dipanggil berulang kali.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

def calculate_hash(filepath: str) -> str | None:
    """
    Menghitung hash SHA-256 dari sebuah file.
    Membaca file dalam bentuk chunk untuk efisiensi memori pada file besar.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError:
        logging.error(f'Tidak dapat membaca file "{os.path.basename(filepath)}". Mungkin file terkunci atau hilang.')
        return None

def load_baseline() -> dict:
    """
    Memuat baseline hash dari file JSON.
    Mengembalikan dictionary kosong jika file tidak ada atau rusak.
    """
    if os.path.exists(HASH_DB_FILE):
        with open(HASH_DB_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logging.error(f"Gagal membaca {HASH_DB_FILE}. File mungkin rusak.")
                return {}
    return {}

def save_baseline(hashes: dict):
    """
    Menyimpan baseline hash (dalam format dictionary) ke file JSON.
    """
    with open(HASH_DB_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)
    logging.info(f'Baseline hash baru telah disimpan di {HASH_DB_FILE}.')

def create_baseline():
    """
    Membuat baseline awal dari semua file di dalam folder aman.
    Secara otomatis akan membuat folder aman jika belum ada.
    """
    os.makedirs(SECURE_FOLDER, exist_ok=True)
    logging.info(f'Membuat baseline untuk folder "{SECURE_FOLDER}"...')
    baseline_hashes = {}
    files_in_folder = os.listdir(SECURE_FOLDER)
    
    if not files_in_folder:
        logging.warning(f'Folder "{SECURE_FOLDER}" kosong. Baseline akan kosong.')
    
    for filename in files_in_folder:
        filepath = os.path.join(SECURE_FOLDER, filename)
        if os.path.isfile(filepath):
            file_hash = calculate_hash(filepath)
            if file_hash:
                baseline_hashes[filename] = file_hash
    save_baseline(baseline_hashes)

def monitor_folder():
    """
    Fungsi utama untuk membandingkan kondisi folder saat ini dengan baseline.
    Mendeteksi file yang diubah, dihapus, atau ditambahkan.
    """
    if not os.path.exists(SECURE_FOLDER):
        logging.error(f'Folder pemantauan "{SECURE_FOLDER}" tidak ditemukan. Pengecekan dibatalkan.')
        return

    logging.info('--- Memulai Pengecekan Integritas File ---')
    baseline_hashes = load_baseline()

    if not baseline_hashes:
        logging.warning(f'File baseline {HASH_DB_FILE} tidak ditemukan atau kosong. Jalankan ulang untuk membuat baseline baru.')
        return

    current_files_on_disk = {f for f in os.listdir(SECURE_FOLDER) if os.path.isfile(os.path.join(SECURE_FOLDER, f))}
    baseline_files = set(baseline_hashes.keys())

    # 1. Cek file yang DIUBAH (hash berbeda) atau DIHAPUS (tidak ada di disk)
    for filename, baseline_hash in baseline_hashes.items():
        if filename not in current_files_on_disk:
            logging.warning(f'File "{filename}" telah DIHAPUS!')
            continue

        filepath = os.path.join(SECURE_FOLDER, filename)
        current_hash = calculate_hash(filepath)

        if current_hash != baseline_hash:
            logging.warning(f'Integritas file "{filename}" GAGAL! Hash tidak cocok.')
        else:
            logging.info(f'File "{filename}" terverifikasi OK.')

    # 2. Cek file BARU (ada di disk tapi tidak ada di baseline)
    new_files = current_files_on_disk - baseline_files
    for filename in new_files:
        logging.critical(f'ALERT: Ditemukan file baru yang tidak dikenal: "{filename}".')

    logging.info('--- Pengecekan Selesai ---')

def main():
    """
    Fungsi pembungkus (wrapper) untuk menjalankan logika utama.
    Berguna agar skrip ini bisa diimpor dan dijalankan dari skrip lain.
    """
    setup_logging()
    
    if not os.path.exists(HASH_DB_FILE):
        print(f"File {HASH_DB_FILE} tidak ditemukan. Membuat baseline awal...")
        create_baseline()
    else:
        monitor_folder()

if __name__ == '__main__':
    # Blok ini hanya akan dieksekusi jika file ini dijalankan secara langsung
    # (misal: python integrity_monitor.py)
    main()