import numpy as np
import cv2
import time
import glob, os

def get_keypoints(org_img, comp_img):
    '''
    ****** Take one image and call twice refactor this function *************

    Takes two images and returns two touples of keypoints and descriptors
    
    org_img: cv2.imread object
    comp_img: cv2.imread object

    returns: ((matrix of key points, matrix of descriptors), 
              (matrix of key points, matrix of descriptors))
    '''
    # Load the sift algorithm
    sift = cv2.xfeatures2d.SIFT_create()

    # Find keypoints and descriptors of org image and image to compare
    key_points1, desc1 = sift.detectAndCompute(org_img, None)
    key_points2, desc2 = sift.detectAndCompute(comp_img, None)

    return ((key_points1, desc1), (key_points2, desc2))
    
def get_match(desc1, desc2):
    '''
    Takes two matrixes of descriptors about and image and uses a Flann based matcher
    to match these matrixes

    desc1: matrix of descriptors
    desc2: matrix of descriptors

    returns: list of matching descriptors
    '''
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
    return good_points

def rotate_img(image):
    '''
    Will rotate a matrix corresponding to an image

    image: Matrix corresponding to an image

    returns: Rotated matrix corresponding to an image
    '''
    rows,cols,u = image.shape
    rot_image = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    return cv2.warpAffine(image,rot_image,(cols,rows))

def match_images(img1, img2):
    ''' 
    Will attempt to match two images

    img1: string corresponding to filename of image
    img2: string corresponding to filename of image
 
    results: String, Percentage accuracy
    '''
    org_img = cv2.imread(img1)
    comp_img = cv2.imread(img2)

        # Check images are exactly equal to each other
    if org_img.shape == comp_img.shape:
        diff = cv2.subtract(org_img, comp_img)
        b, g, r = cv2.split(diff)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            return "Images Exactly Identical"
           
        # Will get the matching points of two images
        # for all orientations and return a percentage 
    max_points = 0
    for i in range(0, 1):
        org_keypoints, comp_keypoints = get_keypoints(org_img, comp_img)
        key_points1, desc1 = org_keypoints
        key_points2, desc2 = comp_keypoints
        good_points = get_match(desc1, desc2)
        max_points += min([len(desc1), len(desc2)])
        relevence = (len(good_points) / max_points) * 4
    
        comp_img = rotate_img(comp_img)

    return relevence

if __name__ == '__main__':
    print(match_images('default.jpg', 'upside.jpg'))
