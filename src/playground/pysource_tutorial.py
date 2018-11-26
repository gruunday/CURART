# This is code from a tutorial found at 
# https://pysource.com/2018/07/20/find-similarities-between-two-images-with-opencv-and-python/

import numpy as np
import cv2

org_img = cv2.imread("orginal.jpg")
comp_img = cv2.imread("photo.jpg")

# Check images are equal to each other
if org_img.shape == comp_img.shape:
    print("Same size and channels")
    diff = cv2.subtract(org_img, comp_img)
    b, g, r = cv2.split(diff)

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        print("Images Equal")
    else:
        print("No Equal")

# Load the sift algorithm
sift = cv2.xfeatures2d.SIFT_create()
# Find keypoints and descriptors of org image and image to compare
key_points1, desc1 = sift.detectAndCompute(org_img, None)
key_points2, desc2 = sift.detectAndCompute(comp_img, None)

# Load FlannBasedMatcher method used to find the matches between descriptors and 2 images
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)

# Find matches between 2 images and store in array
matches = flann.knnMatch(desc1, desc2, k=2)

good_points = []
ratio = 0.6
for m, n in matches:
    if m.distance < ratio * n.distance:
        good_points.append(m)
print(len(good_points))

results = cv2.drawMatches(org_img, key_points1, comp_img, key_points2, good_points, None)


cv2.imshow("Org", org_img)
cv2.imshow("Dup", comp_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
