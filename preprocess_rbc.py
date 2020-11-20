import numpy as np 
import cv2 

# read original image 
image = cv2.imread('bloodcell.jpg')#cv2.imread("dataset-master/dataset-master/JPEGImages/BloodImage_00004.jpg") 
img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
rlower = np.array([160, 60, 100])#, dtype = "uint8") #np.array([110, 100, 200], dtype = "uint8")
rupper = np.array([180, 200, 255])#, dtype = "uint8") #np.array([130, 120, 230], dtype = "uint8")
# find the colors within the specified boundaries and apply
# the mask
rmask = cv2.inRange(img, rlower, rupper)
'''
kernel = np.ones((5, 5), np.uint8)
mask = cv2.erode(mask, kernel)

kernel = np.ones((3, 3), np.uint8)
mask = cv2.dilate(mask, kernel)
'''
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#cnts = sorted(contours, key=cv2.contourArea, reverse= True)#[:5]
print(len(contours))
cv2.drawContours(image, contours, -1, (255, 0, 0), 3)
black_image = np.zeros(image.shape)#, np.uint8)
cv2.drawContours(black_image, contours[:1], -1, (255, 255, 255), -1)

kernel = np.ones((7, 7), np.uint8)
eroded = cv2.dilate(mask, kernel)
#dilated = cv2.dilate(black_image, kernel)
output = cv2.bitwise_and(img, img, mask = mask)

def detect_circles(image, threshed):
	# Apply Hough transform on the blurred image. 
	detected_circles = cv2.HoughCircles(threshed, cv2.HOUGH_GRADIENT, 1, 5, param1 = 80, param2 = 15, minRadius = 5, maxRadius = 25)
	print(len(detected_circles[0]))

	# Draw circles that are detected. 
	if detected_circles is not None: 

		# Convert the circle parameters a, b and r to integers. 
		detected_circles = np.uint16(np.around(detected_circles)) 

		for pt in detected_circles[0, :]: 
			a, b, r = pt[0], pt[1], pt[2] 

			# Draw the circumference of the circle. 
			cv2.circle(image, (a, b), r, (0, 255, 0), 2) 

			# Draw a small circle (of radius 1) to show the center. 
			cv2.circle(image, (a, b), 1, (0, 0, 255), 3) 

detect_circles(image, mask)

while True:
	cv2.imshow('Threshed', output)
	#cv2.imshow('Dilated', dilated)
	cv2.imshow('Image', image)
	cv2.imshow('HSV', img)
	cv2.imshow('Mask', mask)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break

cv2.destroyAllWindows()