import requests
import numpy as np
from pyzbar.pyzbar import decode
import time
import cv2


def check_qr():
    x = requests.get('http://192.168.1.67:8080/?action=snapshot')
    byte_arr = x.content
    img = cv2.imdecode(np.frombuffer(byte_arr, np.uint8), -1)

    for barcode in decode(img):
        my_data = barcode.data.decode('utf-8')
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        pts2 = barcode.rect
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        cv2.putText(img, my_data, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 255), 2)

    return img

while True:
    start = time.monotonic()
    img = check_qr()
    end = time.monotonic()
    print((end - start) * 1000)
    cv2.imshow('Result', img)
    cv2.waitKey(50)
