import cv2
import pytesseract
import numpy as np
import cv2
import threading
import time

CAMERA = 0

file_name = 'test2.mp4'
SLEEP_INTERVAL = 0.001
deviceType = file_name

class Ocr(threading.Thread):
    device = deviceType

    def __init__(self):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(self.device)

        self.scan_page = False
        self.ocr_text = ''
        print('ocr on method')

    def _ocr_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text

    def run(self):
        threading.Thread.run(self)
        frame_ocr = []
        print('run')
        while self.cap.isOpened():
            _, frame = self.cap.read()

            time.sleep(SLEEP_INTERVAL)
            if frame is not None:
                if self.scan_page:
                    frame_ocr = frame
                    print('scan page == true')
                    break
        self.cap.release()
        print('scanned page method start')
        self.ocr_text = self._ocr_frame(frame_ocr)
        print('scanned page method start')

    def make_scan_page(self):
        self.scan_page = True
        print('make_scan_page method')

    def join(self):
        threading.Thread.join(self)
        print('ocr off method')
        return self.ocr_text

if __name__ == '__main__':
    ocr_thread = Ocr()
    ocr_thread.start()

    while True:
        time.sleep(2)
        ocr_thread.make_scan_page()
        break

    print(ocr_thread.join())


