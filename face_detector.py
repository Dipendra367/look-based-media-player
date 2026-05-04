import cv2
import time

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.cap = cv2.VideoCapture(0)
        self._looking = False
        self._last_check = 0
        self.check_interval = 0.3  # check every 300ms

    def is_looking(self):
        now = time.time()
        if now - self._last_check < self.check_interval:
            return self._looking  # return last result, don't re-check

        ret, frame = self.cap.read()
        if not ret:
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )
        self._looking = len(faces) > 0
        self._last_check = now
        return self._looking

    def release(self):
        self.cap.release()