*Simple File Integrity Monitor*

Sebuah sistem sederhana berbasis Python untuk memantau integritas file dalam sebuah direktori. Sistem ini dapat mendeteksi file yang diubah, ditambahkan, atau dihapus, mencatat semua aktivitas, dan menyajikan laporan melalui dashboard web sederhana.

**Fitur Utama**

- Baseline Hashing: Membuat "snapshot" aman dari direktori menggunakan hash SHA-256.

- Deteksi Anomali: Memberi peringatan jika ada file yang diubah, dihapus, atau file baru yang tidak dikenal muncul.

- Logging: Semua aktivitas dicatat ke security.log dengan timestamp dan level (INFO, WARNING, CRITICAL).

- Dashboard Web: Visualisasi status keamanan yang mudah dibaca melalui browser.

- CLI Terpusat: Semua perintah dijalankan melalui main.py untuk kemudahan penggunaan.

**Struktur Proyek**
```
    
.
├── secure_files/       # Folder yang dipantau (letakkan file Anda di sini)
├── integrity_monitor.py  # Logika inti untuk hashing dan verifikasi
├── log_analyzer.py     # Skrip untuk meringkas log
├── dashboard.py        # Server web Flask untuk dashboard
├── main.py             # Titik masuk utama (CLI)
├── hash_db.json        # (Dibuat otomatis) Database baseline hash
└── security.log        # (Dibuat otomatis) File log aktivitas
```
  

**Cara Menjalankan**
1. Persiapan Awal

a. Clone Repositori
```bash
git clone [URL_REPOSITORI]
cd [NAMA_FOLDER_REPOSITORI]
```
  

b. Instal Dependensi
Sistem ini hanya membutuhkan Flask untuk dashboard.
```bash
pip install Flask
```
  

2. Penggunaan

a. Letakkan File
Tempatkan file-file yang ingin dipantau ke dalam folder secure_files/.

b. Buat Baseline Awal
Jalankan perintah ini hanya sekali saat pertama kali memulai untuk membuat database hash (hash_db.json).
```bash
python integrity_monitor.py
```
  

Penting: Jika ingin me-reset baseline (misalnya setelah menambahkan file baru secara sah), hapus file hash_db.json dan jalankan kembali perintah di atas.

c. Jalankan Sistem Pemantauan
Gunakan main.py untuk menjalankan sistem. Pilih salah satu mode berikut:

    Mode 1: Monitor dan Dashboard (Direkomendasikan)
    Menjalankan pemantauan di latar belakang (setiap 60 detik) dan meluncurkan dashboard web.
```bash   
python main.py start --interval 60
```
  

Buka http://127.0.0.1:5000 di browser

Mode 2: Hanya Monitor di Terminal
Menjalankan pengecekan setiap 10 detik dan menampilkan output langsung di terminal.
```bash    
python main.py monitor --interval 10
```
  

Mode 3: Hanya Dashboard
Hanya menjalankan dashboard untuk melihat status terakhir dari security.log.
```bash   
python main.py dashboard
```
      

Untuk menghentikan semua proses, tekan CTRL + C di terminal.