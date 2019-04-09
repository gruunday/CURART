# Getting started with Key Point Matching with OpenCV

In the previous blog we saw that we can install the opencv library with the xfeatures2d compiled in. In this blog I will take you through how to use these features and how I am using them in this project to try match images, not based on their semantic meaning but their actual likeness. So without further adieu.

## Comparing Images in OpenCV

So straight off we will have to import the OpenCV module and we can do that with:

```python
import cv2
```
The next thing to do will be to load in two images that we want to compare together.
We can do this with the function in cv2 called imread.

```python
# Reading in images to OpenCV
org_img = cv2.imread(“image_one.jpg”)
copy_img = cv2.imread(“image_copy.jpg”)
```

This will read in two images and will store them in a variable as matrices. This is how most images are stored in computers and allows them to perform operations on them easily with maths.

Once we have the images loaded in we can then start to perform the operations on them. For early experiments I wanted to get up and running fast so I am using low resolution images that are not incredibly big. This mean that the CPU can accomplish these task very fast without me waiting around four hours waiting on image processing. So as a tip for starting I would also start with small images to see what different experiments can be done with the OpenCV library. 

### Keypoint Detection

This first part of the process will be to analyse the images and pick out the key points of an image. OpenCV does this by using a sift algorithm which stands for scale-invariant feature transformation. It works by locating key points and then using local descriptors about them key points will make each key point as unique as possible. These descriptors should be invariant to any transformations on the image. 

The first module we will write will be to get these key points from the image. 

```python
def get_keypoints(img):
	# This will load the sift algorithm
	sift = cv2.xfeatures2d.SIFT_create()
        # Then compute key points and descriptors
	key_point, desc = sift.detectAndCompute(img, None)

	return key_point, desc
```

This will take a matrix representing an image and it will return the matrix of key points and a metrix of descriptors to go with these key points. Once we have the key points to both images then we need to match them. 

### Key point matches

We will do this with a flann based matcher. There are two popular options with OpenCV that I know of. There is the BFMatcher which stands for a brute force matcher and will find all the best matches but, as we know with the nature of brute force things they can be slow. The other option considered was the flann based matcher, which stands for Fast Library of Approximate Nearest Neighbours. This is much faster for more points than the brute force method, but we do have the cost of not necessarily finding all the best possible values. Experimentation suggests that the speed is worth the accuracy hit as it is only a slight hit.

```python
def get_match(desc1, desc2):
    # Load FlannBasedMatcher method used to find the matches between desc1 and desc2
    search_params = dict()
    index_params = desc(algorithm=0, tree=5)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Find the matches between 2 images and store in array 
    Matches = flann.knnMatch(desc1, desc2, k=2)

    good_points = []
    Ratio = 0.6
    for m,n in matches:
        if m.distance < ratio * n.distance:
            good_points.append(n)

    # Print how many matches we made
    print(len(good_points))
    return good_points
```

Here we take the descriptors about the key points (notice we don’t actually use the key points themselves here). This function then returns us an array of points that match between the two images. We can already see from the amount of good points that were found whether the images were similar enough to be a match. Generally the bigger an image has the more key points it will have and hence the amount of matches but we can see when we turn the amount of key points in the image in relation to the amount of matches made if this was a good match or not.

### Drawing results

If we wanted to visual inspect if there were good matches or not we can draw these matches on the screen with OpenCV also. 

```python
# Call the functions on the images
org_keypoints, comp_keypoints = get_keypoints(org_img, comp_img)
key_points1, desc1 = org_keypoints
key_points2, desc2 = comp_keypoints
good_points = get_match(desc1, desc2)

# Draw the results of comparing the two images side by side
results = cv2.drawMatches(org_img, key_points1, comp_img, key_points2, good_points, None)
```

![key point matches screenshot](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/raw/master/docs/blog/images/KeyPointMatches.png)


Above we see two images of different sizes, one an original of a painting. The other a camera photo of a painting but it is not framed correctly, it has flash in the centre bottom and it has been inverted. The key point matching system still finds there are key points matching in the images. 
