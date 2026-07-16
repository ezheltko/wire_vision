import os
import cv2
import time

# 1 чтение видео с вебкамеры и сохранение кадров в папку

new_dir = 'new_dir'

if not os.path.exists(new_dir):
    os.mkdir(new_dir)

cap = cv2.VideoCapture(0)
count = 0

while True:
    success, img = cap.read()
    if success:
        cv2.imshow('video', img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord(' '):
            img_name = f'{time.time()}_{count}.jpg'
            img_path = os.path.join(new_dir, img_name)
            cv2.imwrite(img_path, img)


