import cv2
import numpy as np

img = cv2.imread('./bin/robocup2025_raspberrypi_program/bin/1762419270.788_original.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = np.array([40, 20, 5])
upper_green = np.array([150, 255, 255])

mask = cv2.inRange(hsv, lower_green, upper_green)
cv2.imwrite('green_mask_visualization.jpg', mask)
print("Saved: green_mask_visualization.jpg")
