import cv2
import numpy as np

img = cv2.imread('static\assets\triangletest.jpg')
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(img1,150,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
print("Number of contours detected:",len(contours))

for cnt in contours:
	approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
	if len(approx) == 3:
		img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
		M = cv2.moments(cnt)
		if M['m00'] != 0.0:
			x = int(M['m10']/M['m00'])
			y = int(M['m01']/M['m00'])
	cv2.putText(img, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

cv2.imshow("Triangles", img)
cv2.waitKey(0)
cv2.destroyAllWindows()