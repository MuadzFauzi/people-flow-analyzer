# People Flow Analyzer 🚶‍♂️📊

**Sistem Deteksi, Tracking, dan Penghitungan Orang Otomatis Menggunakan Computer Vision.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-green)
![OpenCV](https://img.shields.io/badge/CV-OpenCV-red)

## 📋 Deskripsi
Proyek ini adalah sistem pemantauan cerdas yang mengubah video CCTV menjadi data statistik pengunjung. Menggunakan algoritma **YOLOv8** untuk deteksi dan **ByteTrack** untuk pelacakan, sistem ini mampu menghitung jumlah orang masuk dan keluar secara akurat dengan metode **Border Validation** (Validasi Tepi) untuk mencegah penghitungan ganda.

## ✨ Fitur Utama
*   **Real-time Detection:** Mendeteksi manusia dalam frame video.
*   **Robust Tracking:** Melacak ID unik setiap orang (tidak berubah meski bergerak).
*   **Anti-Double Counting:** Logika validasi tepi memastikan orang hanya dihitung saat benar-benar masuk dari pintu.
*   **Reporting:** Menghasilkan grafik laporan jumlah pengunjung otomatis.

## 🛠️ Instalasi

1.  **Clone Repository**
    ```bash
    git clone https://github.com/USERNAME_ANDA/people-flow-analyzer.git
    cd people-flow-analyzer
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Siapkan Video**
    *   Siapkan video CCTV/sampel (format .mp4).
    *   Simpan di folder `assets/` dengan nama `video_sample.mp4` (atau sesuaikan di `config/settings.yaml`).

## 🚀 Cara Menjalankan

Jalankan perintah berikut di terminal:

```bash
python main.py