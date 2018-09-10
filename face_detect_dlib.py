import cv2
import dlib
import sys

# Get user supplied values
imagePath = sys.argv[1]

# Create dlib face detector
detector=dlib.get_frontal_face_detector()

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
rects = detector(gray, 0)

print("Found {0} faces!".format(len(rects)))

# Draw a rectangle around the faces
i = 0
for rect in rects:
	i = i + 1
	cv2.rectangle(
		image, 
		(rect.left(), rect.top()), 
		(rect.right(), rect.bottom()), 
		(0, 255, 0), 
		2
	)
	cv2.putText(
		image, 
		"Face@{}".format(i), 
		(rect.left(), rect.top()), 
		cv2.FONT_HERSHEY_SIMPLEX, 
		0.5, 
		(255, 0, 255), 
		1
	)

cv2.imshow("Faces found Result", image)
cv2.waitKey(0)
