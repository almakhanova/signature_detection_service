import cv2
import os
import numpy as np

def detect_signature(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to open image file: {image_path}")
        return []

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    signatures = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        if 100 < w < 600 and 30 < h < 200 and 1 < aspect_ratio < 5:  
            area = cv2.contourArea(contour)
            if area > 1000: 
                signatures.append((x, y, w, h))

    return signatures

if __name__ == "__main__":
    image_path = os.path.abspath('task_5/signature_example.png')  
    detected_signatures = detect_signature(image_path)
    print(f"Detected {len(detected_signatures)} signature(s): {detected_signatures}")