class FlowCounter:
    def __init__(self, width, height, exit_threshold=2.0, border_margin=50):
        self.width = width
        self.height = height
        self.exit_threshold = exit_threshold
        self.border_margin = border_margin
        
        self.count_in = 0
        self.count_out = 0
        
        # Set ID yang VALID (Benar-benar manusia yang masuk dari pinggir)
        self.valid_ids = set()
        
        # Set ID yang pernah dilihat (termasuk ghost/noise)
        self.seen_ids = set()
        self.exited_ids = set()
        
        self.last_seen = {} # {id: timestamp}
        self.log_data = []

    def is_near_border(self, cx, cy):
        """Cek apakah koordinat berada di area pinggir frame"""
        m = self.border_margin
        return (cx < m) or (cx > self.width - m) or (cy < m) or (cy > self.height - m)

    def update(self, tracks, current_time):
        # 1. LOOP TRACKING SAAT INI
        for track in tracks:
            x1, y1, x2, y2, track_id = track
            track_id = int(track_id)
            
            # Gunakan titik tengah bawah (kaki) untuk posisi yang lebih akurat
            cx = (x1 + x2) // 2
            cy = y2 
            
            self.last_seen[track_id] = current_time

            # --- LOGIKA VALIDASI MASUK ---
            if track_id not in self.seen_ids:
                self.seen_ids.add(track_id)
                
                # Syarat hitung MASUK: Harus muncul dari pinggiran
                if self.is_near_border(cx, cy):
                    self.valid_ids.add(track_id)
                    self.count_in += 1
                    self.log_data.append({'time': current_time, 'type': 'IN', 'total': self.count_in})
                    print(f"[INFO] ID {track_id} Valid MASUK (Area Tepi).")
                else:
                    # Jika muncul tiba-tiba di tengah, abaikan (ID Switch)
                    # print(f"[DEBUG] ID {track_id} Diabaikan (Muncul di Tengah).")
                    pass

        # 2. PROSES KELUAR (Cek timeout)
        all_ids = list(self.last_seen.keys())
        
        for track_id in all_ids:
            if track_id in self.exited_ids:
                continue
            
            time_since_seen = current_time - self.last_seen[track_id]
            
            if time_since_seen > self.exit_threshold:
                self.exited_ids.add(track_id)
                
                # Syarat hitung KELUAR: ID tersebut haruslah ID yang Valid
                if track_id in self.valid_ids:
                    self.count_out += 1
                    self.log_data.append({'time': current_time, 'type': 'OUT', 'total': self.count_out})
                    print(f"[INFO] ID {track_id} Valid KELUAR.")

        return self.count_in, self.count_out