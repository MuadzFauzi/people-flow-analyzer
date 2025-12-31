from ultralytics import YOLO

class PeopleTracker:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)

    def track(self, frame):
        # classes=0 (Person only)
        # persist=True (Wajib untuk tracking ID)
        # conf=0.3 (Abaikan deteksi yang kurang yakin)
        # iou=0.5 (Ambang batas tumpang tindih)
        results = self.model.track(frame, persist=True, classes=0, verbose=False, 
                                   conf=0.3, iou=0.5, tracker="bytetrack.yaml")
        
        tracked_objects = []
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().numpy()
            
            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = map(int, box)
                tracked_objects.append([x1, y1, x2, y2, track_id])
                
        return tracked_objects