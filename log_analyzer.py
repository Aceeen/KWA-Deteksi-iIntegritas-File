# log_analyzer.py
import re
from datetime import datetime

LOG_FILE = 'security.log'

def analyze_log():
    """Membaca dan menganalisis file log untuk memberikan ringkasan."""
    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.readlines()
    except FileNotFoundError:
        print(f"Error: File log '{LOG_FILE}' tidak ditemukan. Jalankan integrity_monitor.py terlebih dahulu.")
        return

    verified_ok = 0
    integrity_failed = 0 # Mencakup file diubah + dihapus
    unknown_files = 0
    last_anomaly_time = None

    # Pola regex untuk mengekstrak timestamp dari log anomali
    log_pattern = re.compile(r'\[(.*?)\] (WARNING|CRITICAL|ALERT): (.*)')

    for line in logs:
        if "terverifikasi OK" in line:
            verified_ok += 1
        
        match = log_pattern.match(line)
        if match:
            timestamp_str = match.group(1)
            message = match.group(3)
            
            # Simpan timestamp anomali terakhir
            last_anomaly_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            
            if "GAGAL" in message or "DIHAPUS" in message:
                integrity_failed += 1
            elif "file baru yang tidak dikenal" in message:
                unknown_files += 1

    print("\n--- Laporan Analisis Log Keamanan ---")
    print(f"Jumlah Verifikasi Berhasil (OK): {verified_ok}")
    print(f"Jumlah File Rusak/Dihapus:       {integrity_failed}")
    print(f"Jumlah File Baru Tak Dikenal:    {unknown_files}")
    if last_anomaly_time:
        print(f"Waktu Terakhir Terdeteksi Anomali: {last_anomaly_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("Tidak ada anomali yang tercatat.")
    print("-------------------------------------\n")

if __name__ == '__main__':
    analyze_log()