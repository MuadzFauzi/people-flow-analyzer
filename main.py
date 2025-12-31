import cv2
import time
import yaml
import os
import sys

# Fix path import
sys.path.append(os.getcwd())

from src.preprocessing import Preprocessor
from src.tracker import PeopleTracker
from src.feature_extract import FeatureExtractor
from src.counter import FlowCounter
from src.visualizer import Visualizer

def load_config():
    try:
        with open("config/settings.yml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: Config file tidak ditemukan.")
        sys.exit(1)

def main():
    cfg = load_config()
    os.makedirs("data", exist_ok=True)
    
    video_path = cfg['video_path']
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Gagal membuka video: {video_path}")
        return

    # Ambil resolusi video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Resolusi Video: {width}x{height}")

    # Inisialisasi Modul
    preprocessor = Preprocessor()
    tracker = PeopleTracker(model_path=cfg['model_path'])
    extractor = FeatureExtractor()
    visualizer = Visualizer()
    
    # Setup Counter dengan Validasi Tepi
    c_conf = cfg.get('counting', {})
    counter = FlowCounter(width, height, 
                          exit_threshold=c_conf.get('exit_threshold', 2.0),
                          border_margin=c_conf.get('border_margin', 50))
    
    start_time = time.time()
    window_name = "People Flow Analyzer"

    print("Program Berjalan... Tekan 'q', 'ESC', atau tombol 'X' window untuk berhenti.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Video selesai.")
            break
        
        current_time = time.time() - start_time
        
        # 1. Preprocessing & Detection
        clean_frame = preprocessor.apply_filter(frame)
        tracks = tracker.track(clean_frame)
        
        # 2. Fitur Tambahan (Opsional)
        for track in tracks:
            x1, y1, x2, y2, track_id = track
            # Hanya proses ID yang valid agar hemat resource
            if track_id in counter.valid_ids:
                h_img, w_img, _ = frame.shape
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w_img, x2), min(h_img, y2)
                
                person_crop = frame[y1:y2, x1:x2]
                color = extractor.get_shirt_color(person_crop)
                
                if color == "RED":
                    cv2.putText(frame, "RED", (x1, y1-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        
        # 3. Update Counter (Logika Inti)
        counter.update(tracks, current_time)
        
        # 4. Visualisasi
        final_frame = visualizer.draw_overlays(frame, tracks, counter)
        cv2.imshow(window_name, final_frame)
        
        # --- LOGIKA KELUAR (EXIT) ---
        key = cv2.waitKey(1) & 0xFF
        # Tekan 'q' atau ESC (27)
        if key == ord('q') or key == 27:
            print("Berhenti via Keyboard.")
            break
        
        # Tekan tombol 'X' window
        try:
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                print("Berhenti via Window Close.")
                break
        except Exception:
            pass

    # Generate Grafik
    counter.log_data.append({'time': current_time, 'type': 'END', 'total': 0})
    visualizer.generate_report(counter.log_data)
    
    cap.release()
    cv2.destroyAllWindows()
    print("Selesai.")

if __name__ == "__main__":
    main()