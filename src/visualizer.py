import matplotlib.pyplot as plt
import pandas as pd
import cv2

class Visualizer:
    def draw_overlays(self, frame, tracks, counter):
        # Overlay Background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (250, 100), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
        
        # Info Teks
        cv2.putText(frame, f"TOTAL MASUK : {counter.count_in}", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"TOTAL KELUAR: {counter.count_out}", (10, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Gambar Area Margin (Visualisasi Debug - Garis Tipis Abu-abu)
        h, w, _ = frame.shape
        m = counter.border_margin
        cv2.rectangle(frame, (m, m), (w-m, h-m), (100, 100, 100), 1)

        # Draw Tracks
        for track in tracks:
            x1, y1, x2, y2, track_id = track
            
            # Warna Hijau = Valid, Kuning = Belum Valid/Ignored
            color = (0, 255, 0) if track_id in counter.valid_ids else (0, 255, 255)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"ID:{track_id}", (x1, y1-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        return frame

    def generate_report(self, log_data, output_path='data/report_graph.png'):
        if not log_data:
            print("Tidak ada data untuk dibuat grafik.")
            return

        try:
            df = pd.DataFrame(log_data)
            plt.figure(figsize=(10, 5))
            
            df_in = df[df['type'] == 'IN']
            if not df_in.empty:
                plt.plot(df_in['time'], df_in['total'], label='Total Masuk', color='green', marker='.')
                
            df_out = df[df['type'] == 'OUT']
            if not df_out.empty:
                plt.plot(df_out['time'], df_out['total'], label='Total Keluar', color='red', marker='.')
            
            plt.title("Analisis People Flow (Validasi Tepi)")
            plt.xlabel("Waktu (Detik)")
            plt.ylabel("Jumlah Orang")
            plt.legend()
            plt.grid(True)
            plt.savefig(output_path)
            print(f"Grafik laporan tersimpan di: {output_path}")
        except Exception as e:
            print(f"Gagal membuat grafik: {e}")