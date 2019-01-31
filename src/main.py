import numpy as np
import cv2
import time
import glob, os

def get_keypoints(org_img, comp_img):
    # Load the sift algorithm
    sift = cv2.xfeatures2d.SIFT_create()

    # Find keypoints and descriptors of org image and image to compare
    key_points1, desc1 = sift.detectAndCompute(org_img, None)
    key_points2, desc2 = sift.detectAndCompute(comp_img, None)

    return ((key_points1, desc1), (key_points2, desc2))
    
def get_match(desc1, desc2):
    # Load FlannBasedMatcher method used to find the matches between descriptors and 2 images
    search_params = dict()
    index_params = dict(algorithm=0, trees=5)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    # Find matches between 2 images and store in array
    matches = flann.knnMatch(desc1, desc2, k=2)
    
    good_points = []
    ratio = 0.6
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good_points.append(m)
    print(len(good_points))
    return good_points

def rotate_img(image):
    rows,cols,u = image.shape
    rot_image = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    return cv2.warpAffine(image,rot_image,(cols,rows))


if __name__ == '__main__':
    org_img = cv2.imread("orginal.jpg")
    comp_img = cv2.imread("upside.jpg")

#  Implementing finding an image in a directory of images
#    file_lst = []
#    os.chdir("/mydir")
#    for f in glob.glob("*.jpg"):
#        file_lst.append(f)
#
#    for f in file_lst:
#

    # Check images are equal to each other
#    if org_img.shape == comp_img.shape:
#        print("Same size and channels")
#        diff = cv2.subtract(org_img, comp_img)
#        b, g, r = cv2.split(diff)
#    
#        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
#            print("Images Equal")
#        else:
#            print("No Equal")
    
    
    for i in range(0, 1):
        org_keypoints, comp_keypoints = get_keypoints(org_img, comp_img)
        key_points1, desc1 = org_keypoints
        key_points2, desc2 = comp_keypoints
        good_points = get_match(desc1, desc2)
        
        results = cv2.drawMatches(org_img, key_points1, comp_img, key_points2, good_points, None)
   
        cv2.imshow("result", results)
        cv2.imshow("Org", org_img)
        cv2.imshow("Dup", comp_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
        comp_img = rotate_img(comp_img)
