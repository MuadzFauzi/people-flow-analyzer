import cv2

class Preprocessor:
    def __init__(self):
        # Background subtraction untuk visualisasi/debug area gerak
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)

    def apply_filter(self, frame, kernel_size=5):
        # Gaussian blur untuk mengurangi noise
        return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

    def detect_edges(self, frame):
        # Canny edge detection untuk visualisasi struktur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 50, 150)