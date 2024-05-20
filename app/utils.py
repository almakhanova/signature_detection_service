import cv2
import numpy as np
import os

def detect_signature(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return []

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    signatures = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        if 100 < w < 600 and 30 < h < 200 and 1 < aspect_ratio < 5:
            area = cv2.contourArea(contour)
            if area > 1000:
                signature_img = image[y:y+h, x:x+w]
                signature_path = f"./uploads/signature_{i}.png"
                cv2.imwrite(signature_path, signature_img)
                signatures.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "image_path": signature_path
                })

    return signatures
