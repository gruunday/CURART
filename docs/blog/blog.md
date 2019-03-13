# Blog: Visual Search for Stolen Artworks

**TOM DOYLE**

## Blog One : The Idea

In this blog I hope to explore how my idea has come into fruition and where it stems from. The project is to be able to identify if an image is visually similar enough to be called the same image. This would use several image vision algorithms and would ideally be automatic. But what do I mean by automatic? I mean that you should be able to check one image against a database of hundreds or thousands. Ideally you could have regular checks run weekly or monthly to find a stolen images. 

There is also the question of where does the database come from. This is also a problem. I hope to implement a rudimentary web crawler to collect metadata about the images and where it has seen the image. By pre computing the information on the way into the database I hope this will speed up the final solution. In response to the question "Are you going to download every image on the internet?" No, I am not. Ideally you would start with the most popular sites and work down to the less popular ones. This is because the more people that see the stolen image, to more revenue the original owner stands to lose out on.

It is an idea that I have been curious about for quite a while and would love to see a solution to. I know a lot of photographers would also be interested in finding a solution to this problem as it stops many great photographers sharing their most prised images online. It also hurts online sales when you can see an image of the image before you buy the image. It leads to photographers putting heavy watermarks on their images and going through great lengths to stop them being used elsewhere. 

Other solutions out there may include reverse image search, such as Google's solution. I have researched these implementations and they seem to have more emphasis on semantic matching, meaning if you searched for an image of an orange cat in a tree it would be less concerned with that cat in that tree but more so any orange cat in any tree. The context matters but the specific subject can change. This is not what I want to implement. I was to compare the visual similarity of these images and be able to say with a percentage of confidence that the first image is the exact same image. 

You could just say why can't you take the hash of both of the images? But this is not ideal because even if one pixel of the image is changed the hashes won't match. This means the stolen images could elude the system if a watermark was added, the hue was changed or even if it was cropped the smallest amount. There is also another solution were you can match several histograms based on RGB values, textures and vectors. This solution can deal with small amounts of cropping but a watermark of hue will fool the solution into being a different image. 

In the next blog I will go into a proposed immature solution, and one that I will attempt to deploy. 


## Blog Two : Compiling OpenCV 3.4.0 on Ubuntu 18.04.1 LTS for Python 3.6

OpenCV is the Open Source Computer Vision Library used for computer vision and machine learning. It was built to "provide a common infrastructure for computer vision applicatoins and to accelerate the use of machine perception in comercial products". - [About OpenCV](https://opencv.org/about.html).

This suits my projects needs and aligns with what I want to do given the very short time span of the project and the vast amount of ground that I am trying to cover in the project. 

Unfortunatly being an open source library anything that is not always open source was taken out in version 3.0.0 and so we need to compile our own version with the opencv_contrib modules included. This is because we want to use an alogorithm called SIFT, a propriatary module but free to use for accademic use. 

* These steps are quiet easy to follow if you pay careful attention to what you are doing the first time you are doing them.
* This becomes a lot more complicated if you have multiple versions of python installed. It resulted in my not being able to install OpenCV for python3 at all and I had to reload the OS because you cannot remove python easily from an Ubuntu System.

* My first interaction with opencv was installing via:
```bash
$ sudo apt install python-opencv
```

* This worked great but I wanted access to the SIFT algorithm, a propriety algorithm unless being used in research. 
* The default package does not contain this module any more as of version opencv-3.0.0
* It now means that if one wants access to this module you have to compile it yourself.

*Note*: I did not use a virtualenv but they are a good idea.

### Installing dependencies

* Start by updateing your system
```bash
$ sudo apt-get update
$ sudo apt-get upgrade
```

* Install developer tooling
```bash
$ sudo apt-get install build-essential cmake git pkg-config
```

* Install libraries to read from disk
```bash
$ sudo apt-get install libjpeg8-dev libtiff5-dev:i386 libtiff5-dev \
                       libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
```

* Install GTK for GUI features of opencv
```bash
$ sudo apt-get install libgtk2.0-dev libcanberra-gtk-module \
                       libcanberra-gtk3-module
```

* And Finally install packages that perform optimisations in opencv
```bash
$ sudo apt-get install libatlas-base-dev gfortran
```

### Getting Pip

* If you do not have pip it would suggest getting pip
```bash
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py
```

### Setting up our Python

* Before we can compile opencv we need python headers
```bash
$ sudo apt-get install python3.6-dev
```

* And we can also now use pip to install numpy, as opencv uses numpy arrays for represent images
```bash
$ sudo -H pip3 install numpy
```

### Building and installing opencv

* Here we are going to pull down the source code and compile our opencv
* We will be building the lastest at the time of this being written 3.4

```bash
$ cd ~/
$ git clone https://github.com/Itseez/opencv.git
$ cd opencv
$ git checkout 3.4.0
```

* We also need the extra modules that we want when we are compiling 
* They are kept in a seperate repository and we will go get them now

```bash
$ cd ~/
$ git clone https://github.com/Itseez/opencv_contrib.git
$ cd opencv
$ git checkout 3.4.0
```

* Now that we have everything that we need we will configure opencv

```bash
$ cd ~/opencv
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D INSTALL_C_EXAMPLES=ON \
        -D INSTALL_PYTHON_EXAMPLES=ON \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
        -D PYTHON_EXECUTABLE=/usr/bin/python3.6 \
        -D BUILD_EXAMPLES=ON ..
```

![cmake output screenshot](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/raw/master/docs/blog/images/cmakeScreenshot.png)

* Once configurationg is done you must ensure that the output is the same in the photo concerning python. Check that python3 is the python that is being found and that it is infact being found
* You may run into a lot of errors if you have more than one version of python (especially if you have two version of python3, i.e 3.5 and 3.6)

* Once you are ready to do you can compile opencv with the following
```bash
$ make -j4
```
*Where 4 is the number of cores your processor has*

* Once that step has completed and there are no error you can install the newly compiled opencv

```bash
$ sudo make install 
$ sudo ldconfig
```

### Testing OpenCV

```bash
$ python3
>>> import cv2
>>> cv2.__version__
'3.4.0'
```

* After this you are ready to go

You should now have OpenCV installed on your system and usable for python3. The next blog should be an introduction tutorial on how to use it.


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

# Ten Errors Getting OpenCV on AWS Lambda

In this blog we are exploring the use of Amazon Web Services’ (AWS) function as a service (FAAS) feature called lambda functions. This has presented multiple problems in this project and has set the project back a month. The following blog will be a breakdown of errors encountered and how they have been overcome or how a workaround has come about. 
	
	The design was conceived with no prior hands on experience with AWS Lambda but a solid linux and development operations (DevOps) knowledge, including container technologies such as Docker. It was decided that one particularly intensive function would be done by a lambda function. This would mean that if there were to be a heavy amount of users on the application this function would not become a bottleneck and the application would scale out to huge numbers. Without this the application would remain a research “toy” on a server and work for demonstration purposes but not scale. 
	
	One of the very first errors encountered with this project was attempting to compile opencv locally on a local machine. Compilation was necessary because of the extra modules that are not included in the default installation of opencv, a module vital for the success of this project. The module in question is xfeatures, containing an algorithm called SIFT. It is not included in the default package because it is a patented, non-free algorithm. It is to be used only for research and not commercial purposes. This is perfect for this project’s requirements but requires you to compile opencv with the OPENCV_ENABLE_NON_FREE flag set to true.
	
	Another set back was encountered here when there were multiple versions of python on the local machine and the discovery built into cmake was thrown off. Initially it found no valid versions of python and after several days* of work, cmake discovered python2.7. With only nine months at the time of writing [1] until the end of life of python2 this was not going to be an option to continue with this version of python and the decision was made to keep trying to attempt to get cmake to recognise python3. The end solution to this problem was to backup all important files and completely wipe the local machine clean and install python once and correctly. This solved this issue and cmake could discover python3.
	
	Once opencv was working locally, mockup functions were designed and code to create image “fingerprints” were created. These worked well and quickly to find an image across a file system. Following this, the attempt to implement the now working code on AWS Lambda was undertaken. No previous knowledge was known about lambda, and subsequently there were days* of trial and error until a working hello world toy was created. The learning curve for this was steep as there is a lot of documentation but there are a lot of prerequisites to know before any working solution can take shape.
	
	During the next phase it was a steep learning curve about what it was going to take to package the opencv library and ship it to the lambda function. Hundreds of articles were consulted to attempt to find a working solution. Finally one was found in the form of a bash script. After reading this script it became apparent the steps it was taking, and although it did not suit my needs as a whole it had two beneficial lines.[2] From this it was apparent what files needed to be included in the package along with my python function. A simple error that stunted progress was a misconfiguration between the name of the python file in this package and the name of the function on the AWS Lambda console page. 
	
	An error in thinking that should have been caught sooner was the fact that the package of python code and the opencv library that had just been created was compiled for the local machine and would not run on AWS Lambda. After reading a readme about a project that had attempted this previous you can create an Elastic Compute Cloud (EC2) from Amazon and compile the code there and package that for the lambda function. The documentation followed specifically cited a C4.2xlarge Amazon Linux machine.[3]
	
	Once the software was compiled and packaged there was an error encountered while uploading this to the lambda function. This was cited as the package being too large. Packages for AWS Lambda have to be less that 50M, this package was coming to 58M. The workaround for this was going back to the large library of opencv functions, many of which were unnecessary. They were each looked at and modules that were not used were removed from the opencv_contrib repo on the local machine and opencv was re-compiled without these once more. This brought the package size down to 48M, enough to test it on the lambda function. 
This did not work and had similar issues as before with the packages that were compiled for the local machine. The errors were in relation to shared packages not being available. It was then eventually found there is one correct instance where you can compile packages for AWS Lambda and that was found in the AWS documentation.[4] It is a premade AMI. Once again the instance was destroyed and an effort to start over and reinstall the correct machine was made.

	This correct instance was then used to attempt a compilation although very slow. But because this instance was restricted to 1GB of memory, the compilation could not complete with an “out of virtual memory” error at 86% completion. A local docker container was also used trying to compile with the amazon linux docker image. This compiled successfully and looked promising and working locally. But when uploaded to a Lambda function this failed due to not having access to shared libraries that it had locally that is did not have in the Lambda function as with all other versions not compiled on the specific AMI. 
It is at this point that we stand at the point of no return. We have fallen dangerously close to the deadline and we have to make a sacrifice that this is not worth continuing with lambda functions because the risk of not succeeding is too high and for the deadline there needs to be working software. If time permits we may consider coming back but for now AWS lambda functions are off the table in this project.
For now a plan has been put in place to create a custom docker image based off ubuntu with python and opencv. This means that the project can run in a docker container and possibly be managed by a container management system like kubernetes. This would allow scaling and growth that the project had intended to have originally and may be a solution just as good.
 
\* We do not work full time on the project we have classes and assignments that have to take precedence

1. [https://hg.python.org/peps/rev/76d43e52d978](https://hg.python.org/peps/rev/76d43e52d978)
2. [https://github.com/aeddi/aws-lambda-python-opencv/blob/master/build.sh (lines37-38)](https://github.com/aeddi/aws-lambda-python-opencv/blob/master/build.sh)
3. [https://github.com/aeddi/aws-lambda-python-opencv](https://github.com/aeddi/aws-lambda-python-opencv)
4. [https://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html](https://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html)
