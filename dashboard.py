# dashboard.py
from flask import Flask, render_template_string
import re
from datetime import datetime

app = Flask(__name__)
LOG_FILE = 'security.log'

def get_analysis_data():
    """Membaca data log dan mengembalikannya sebagai dictionary."""
    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.readlines()
    except FileNotFoundError:
        return {'error': f"File log '{LOG_FILE}' tidak ditemukan."}

    # Salin logika analisis dari log_analyzer.py
    verified_ok = 0
    integrity_failed = 0
    unknown_files = 0
    last_anomaly_time = "N/A"
    
    anomalies_found = []

    log_pattern = re.compile(r'\[(.*?)\] (WARNING|CRITICAL|ALERT): (.*)')
    
    for line in logs:
        if "terverifikasi OK" in line:
            verified_ok += 1
        match = log_pattern.match(line)
        if match:
            timestamp_str, level, message = match.groups()
            anomalies_found.append(timestamp_str)
            if "GAGAL" in message or "DIHAPUS" in message:
                integrity_failed += 1
            elif "file baru yang tidak dikenal" in message:
                unknown_files += 1
    
    if anomalies_found:
        last_anomaly_time = max(anomalies_found)

    return {
        'verified_ok': verified_ok,
        'integrity_failed': integrity_failed,
        'unknown_files': unknown_files,
        'last_anomaly_time': last_anomaly_time
    }

@app.route('/')
def dashboard():
    data = get_analysis_data()
    
    # Template HTML sederhana untuk ditampilkan di browser
    html_template = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="10"> <!-- Refresh halaman setiap 10 detik -->
        <title>Dashboard Keamanan File</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f0f2f5; color: #1c1e21; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .container { width: 600px; padding: 30px; background: #fff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; border-bottom: 1px solid #ddd; padding-bottom: 15px; margin-bottom: 25px; }
            .metric { display: flex; justify-content: space-between; align-items: center; font-size: 1.2em; padding: 15px; margin-bottom: 10px; border-radius: 8px; }
            .metric-ok { background-color: #e7f3ff; color: #1877f2; }
            .metric-warn { background-color: #fffbe2; color: #f7b928; }
            .metric-alert { background-color: #ffebe2; color: #d93025; }
            .metric-time { background-color: #f0f0f0; color: #555; }
            strong { font-weight: 600; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Dashboard Pemantauan Integritas File</h1>
            {% if data.error %}
                <p class="metric-alert"><strong>Error:</strong> {{ data.error }}</p>
            {% else %}
                <div class="metric metric-ok"><span>File Aman (Verifikasi OK)</span> <strong>{{ data.verified_ok }}</strong></div>
                <div class="metric {{ 'metric-warn' if data.integrity_failed > 0 else 'metric-ok' }}"><span>File Rusak / Dihapus</span> <strong>{{ data.integrity_failed }}</strong></div>
                <div class="metric {{ 'metric-alert' if data.unknown_files > 0 else 'metric-ok' }}"><span>File Baru Tak Dikenal</span> <strong>{{ data.unknown_files }}</strong></div>
                <div class="metric metric-time"><span>Anomali Terakhir Terdeteksi</span> <strong>{{ data.last_anomaly_time }}</strong></div>
            {% endif %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, data=data)

if __name__ == '__main__':
    print("Dashboard berjalan...")
    print("Buka http://127.0.0.1:5000 di browser Anda.")
    print("Tekan CTRL+C untuk menghentikan server.")
    app.run(debug=False, host='0.0.0.0')