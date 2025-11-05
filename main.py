# main.py
import argparse
import time
import subprocess
import threading
from integrity_monitor import main as run_integrity_check

def run_monitoring_loop(interval: int):
    """
    Menjalankan pengecekan integritas secara berulang dalam sebuah loop.
    """
    print(f"--- Sistem Pemantauan Otomatis Aktif ---")
    print(f"Pengecekan akan dilakukan setiap {interval} detik.")
    print("Tekan CTRL+C untuk berhenti.")
    
    while True:
        try:
            print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Menjalankan pengecekan integritas...")
            run_integrity_check()
            print(f"Pengecekan selesai. Pengecekan berikutnya dalam {interval} detik.")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n--- Sistem Pemantauan Dihentikan oleh Pengguna ---")
            break
        except Exception as e:
            print(f"Terjadi error: {e}")
            print(f"Mencoba lagi dalam {interval} detik...")
            time.sleep(interval)

def run_dashboard():
    """
    Menjalankan server dashboard Flask sebagai proses terpisah.
    """
    print("--- Memulai Server Dashboard ---")
    print("Silakan buka http://127.0.0.1:5000 di browser Anda.")
    try:
        # Menggunakan subprocess agar tidak memblokir skrip utama
        subprocess.run(["python", "dashboard.py"], check=True)
    except FileNotFoundError:
        print("Error: Pastikan 'dashboard.py' berada di direktori yang sama.")
    except subprocess.CalledProcessError as e:
        print(f"Dashboard berhenti dengan error: {e}")
    except KeyboardInterrupt:
        print("\n--- Server Dashboard Dihentikan ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sistem Deteksi Integritas File.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "action",
        choices=["monitor", "dashboard", "start"],
        help=(
            "Aksi yang ingin dijalankan:\n"
            "monitor   - Menjalankan pemantauan berkelanjutan di terminal.\n"
            "dashboard - Hanya menjalankan dashboard web.\n"
            "start     - Menjalankan dashboard DAN pemantauan di latar belakang."
        )
    )
    
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=30,
        help="Interval waktu (dalam detik) untuk pemantauan berkelanjutan. Default: 30 detik."
    )

    args = parser.parse_args()

    if args.action == "monitor":
        run_monitoring_loop(args.interval)
        
    elif args.action == "dashboard":
        run_dashboard()
        
    elif args.action == "start":
        # Jalankan pemantauan di thread latar belakang
        # daemon=True berarti thread akan berhenti jika skrip utama berhenti
        monitor_thread = threading.Thread(
            target=run_monitoring_loop, 
            args=(args.interval,), 
            daemon=True
        )
        monitor_thread.start()
        
        # Jalankan dashboard di thread utama
        run_dashboard()