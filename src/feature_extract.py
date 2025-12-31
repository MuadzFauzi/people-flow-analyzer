import cv2
import numpy as np

class FeatureExtractor:
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=100)

    def get_shirt_color(self, img_crop):
        if img_crop.size == 0: return ""
        
        # Analisis area tengah torso
        h, w, _ = img_crop.shape
        center_crop = img_crop[int(h*0.2):int(h*0.6), int(w*0.3):int(w*0.7)]
        
        if center_crop.size == 0: return ""

        hsv = cv2.cvtColor(center_crop, cv2.COLOR_BGR2HSV)
        
        # Contoh: Deteksi Merah
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        mask = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
        
        if cv2.countNonZero(mask) > (center_crop.size / 3) * 0.1:
            return "RED"
        return ""