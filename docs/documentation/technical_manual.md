![CURART LOGO](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/raw/master/docs/blog/images/CURART_WIDE.png)

# Technical Manual

## Contents

1. Introduction
    - Overview
    - Context Diagram
    - Glossary
2. System Architecture
    - Language Choice
3. High-Level Design
    - Initial Design
    - Current Design
4. Problems and Resolution
5. Installation Guide
6. Configuration 
7. Testing
    - 7.1 Functional Testing
    - 7.2 Non Functional Testing 
8. Class Skeletons

## Introduction
### Overview
This project is written in python 3 to attempt to match images of artworks. The purpose of this is to attempt to find people who are using images of artworks that are in breach of copyright and modified from original or find the source of an artwork. This is implemented using the OpenCV version of the SIFT algorithm. Therefore it is not for commercial  use and purely a research project.

While the domain of this project is restricted here to the domain of just artworks, this project can easily be used for other purposes of finding images that are made up of the exact same content. It will not use context at all for matching, i.e a different angle of the same building. For this to match it is a goal of this project to only match if the images are the same.

The second aim of the project is to work at scale. If this tool is to be usable the user should not have to wait hours to find a result. This research project should be able to get matches in a reasonable amount of time.

#### Context Diagram
![Context Diagram](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-doylet9/raw/master/docs/documentation/images/Curart_context_diagram.png)
**Figure 1.1** *System context diagram*

### Glossary
OpenCV
Docker: Any reference to containers, you can presume that these are docker containers unless otherwise stated.
Container
Traefic
AWS
Postgres


## System Architecture
![System Architecture Diagram](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-doylet9/raw/master/docs/documentation/images/Curart_system_arch.png)
**Figure 2.1** *System architecture diagram*

#### Language Choice
Python is an easy to develop language but has some speed impacts when it comes to heavy computation such as images. But after research into the SIFT algorithm I saw others that had successfully implemented SIFT with python with minimal impacts to speed. [Source](http://aishack.in/tutorials/implementing-sift-opencv/) It became apparent that implementing SIFT was not new and had been done many times before. So rather than reinventing the wheel I wanted to add to work that has been done before me.

This leads to the research into previous implementations of SIFT algorithm. The OpenCV library's implementation was one that came up again and again as the most optimised and accurate. This is the one chosen and is written in C with a python interface so this allows us to use it with python. 

Python has many packages for web frame works that many other low level languages do not. This also made it ideal that we could use it for many different uses throughout the architecture of the project. 

Python is also the language I am most comfortable in, and one of the non functional requirements of this project is to meet the project deadline. There for this is the language I can get all of the features I want to add into this project in time for the final deadline. 

Python2.7 was not considered because the end of life for this version is in 8 months at time of writing.

All these points resulted in me choosing python 3 for this project. 


## High-Level Design

### Initial Design vs Current Design

The initial design of this project has changed significantly since it was first conceived. This was due to lack of experience in using the technologies and also unforeseeable issues that were encountered. We will talk about the differences in this section and we will talk about the problems encountered and why the design has changed in a later section.

![original architecture diagram](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-doylet9/raw/master/docs/documentation/images/SystemArchitecture.png)
**Figure 3.1** *Original design of the project*

The first major design change in the lack of AWS lambda functions. These have been replaced by docker containers that are load balanced by a software defined load balancer called Traefik. This will allow the same amount of scalability but does mean that the base server will have to have to be of sufficient size to handle the traffic rather than a small server that can hand off the computation to another compute module. 

![updated architecture diagram](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-doylet9/raw/master/docs/documentation/images/UpdatedSystemArchitecture.png)
**Figure 3.2** *Updated design of the project*

The datastore for this project as also changed from an amazon S3 bucket to a PostgreSQL database hosted by AWS. This pivot was due to the purpose of S3 buckets being an object store and unstructured data. This was a slow design that would involve searching the whole database if you were looking for a best match like we are rather than retrieving known data. A better solution was to hash the keypoint object on the way into a PostgreSQL database and create a structured form for the data. Then on query we use the Levenshtein distance on the hash to find the best match quickly. This still provides us with the reliability and availability of amazon services which was desirable at the beginning of this project. Postgres also has a Levenshtein function built in. So rather than retrieving all hashes and finding the best match an querying again, we can do the calculation closer to the data speeding up the data retrieval significantly.

The web server has also now been containerised to run multiple instances on the server rather than one for all incoming traffic. Each container handles its traffic internal. The Traefik load balancer for the containers passes the traffic to the container in a round robin method.


## Problems and Resolution
**TODO**
* Lambda problem
* Database problem

## Testing

### Unit Testing

* Once a project is committed to the master branch a Gitlab pipeline is run.
* The first step in this is unit testing.
* PyUnit was used to run these tests and coverage was used to measure the coverage of these tests.
* The current status of these test are:
[![pipeline status](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/badges/master/pipeline.svg)](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/commits/master) [![coverage report](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/badges/master/coverage.svg)](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/commits/master)

----

* This pipeline does only run on the master branch but could be expanded to run on any branch
* Committing to master branch is not ideal because it sometimes becomes unstable for a short amount of time
* Despite this it is felt because there is only one developer on this project it makes sense in this context

----

* The image that was used for testing is a custom image written by this development team for this project. It's files can be found [here](https://gitlab.computing.dcu.ie/doylet9/opencv-python3)
* It has it's own deployment and will automatically be uploaded to Dockerhub once the image it built
* This was necessary because the image takes over an hour to build. This includes installing all the packages necessary to run this application
* In the pipeline OpenCV is compiled and installed with extra modules
* The deployment pipeline for this project could not be run on Gitlab because it takes an hour to build and Gitlab runner timeouts are set to 10mins
* To get around this Github was used to host the source and Circleci was used to build the project


### Post Deployment Testing

* The final stage in the pipeline is to test if the deployment succeeded and it running in production environment
* If this test fails it triggers and alert that is sent to a slack channel
* There are no other alerts channels in place because they were deemed out of scope for the context of the project and timeline but is on the backlog for future work
* In the event the deployment fails the system will attempt to pull from the Gitlab API to find the commit of the last successful build
* It will the attempt a git reset and redeploy the last working version and alert the team through the slack channel it has attempted this

### User Testing
* For this project no real users we asked to complete a test of the application. Due to the limited user interaction function and intuitive design.

* This does not mean that there was no user testing done on the application. To verify this application, each user story was taken and a verified the functionality laid out in this document was easy and intuitive. No issues were found while doing these steps and it is believed that this would satisfy a users needs.

### Functional Testing
Each functional requirement was taken and after a stepping through the application it was verified if the task could be completed

- [x] Must correctly identify image as artwork
- [x] Must identify artwork as similar despite being slightly altered
- [x] Must be able to return a result within a defined reasonable time period (reasonable was defined as 10 seconds)
- [ ] Must be able to find images unsupervised
- [x] Must be able to store metadata about images not the image

During the testing it was found that one requirement was not met. This was removed because of the complexity around unsupervised web scraping within the domain. This requirement was thought of out of scope within the domain

## Non Functional Testing

### Time
- [x] The project was to be completed by the 19th of May 2019 at 23:59 and that has been completed

### Ease of Use
- [x] This tool has been created with a minimal and intuitive design. It has taken methods and minimal styles like other modern search engines to have a familiar look and feel.

### Storage
- [x] The storage on this project is hosted by AWS meaning that it is fast and reliable. It has also been small enough to stay on free tier, so it has not hurt the cost constraint.

### Costs
- [x] The cost of the virtual server is 4 euro a month. Well within a reasonable price. 

### Hardware
- [x] The hardware has been kept minimal with 2GB of RAM, 1 2GHz VCore and 20GB SSD. This means that the cost can be kept low

### Speed

| Image Size | Test One  | Test Two  | Test Three  |
| ---------- | --------- | --------- | ----------- |
| 67.4kB     | 5.34s     | 5.20s     | 5.42s       |
| 152.0kB    | 8.33s     | 8.18s     | 8.56s       |
| 109.9kB    | 9.90s     | 9.71s     | 9.52s       |
| 443.7kB    | 10.36s    | 10.11s    | 10.16s      |

* These speed I am confident can be improved on with the use of cache between the application and the database
* Currently the database is hosted in Ohio on AWS on a preview server
* A lot of the keypoints are large and similar quit often
* While there is cache on the page AWS only allows access to the database through their domain and Cloudflare could not be used as a simple fix
* This is achievable to get AWS cache service working but out of scope for this iteration of the project. 
* It will remain on the backlog for future work


## Algorithms

### SIFT (Scale Invariant Feature Transformation)

#### Why use SIFT?

The requirements laid out at the start of this project in the [Functional Spec](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-doylet9/blob/master/docs/functional-spec/functional-spec.pdf) said that for the requirement to be satisfied an accurate result would have to be returned in under 10 seconds. This was a big feat to attempt to accomplish and after much research SIFT was an algorithm that came up again and again in papers.
It was satisfactory algorithm in that it was ignorance of differences in:
   - color
   - size
   - rotation
   - perspective
   - watermarks
   - hues

For this reason it was thought of as the perfect solution to this problem if utilized correctly.

The next major decision around this algorithm was whether this project would implement it's own or if it would use a library for it.

After reading the work involved in [implementing this in python](aishack.in/tutorials/sift-scale-invariant-feature-transform-introduction/), a quick development language we were not sure if we could fulfill the rest of the requirements in the project. There were also a good few examples of other people doing have done this open source already. Therefore the decision was made to use a library for the functionality

One library came up again and again and that was OpenCV. This has a C implementation with a python interface which give all the speed of python with the ease of integration of python. This was also recommended as a previously heavily optimised version, developed over a number of years, rather than function in a college project.

This function is an extra module in OpenCV and needs to be compiled in. In this project, that is done in the custom docker image we created with OpenCV and python inside. Feel free to use that image or if you want to compile your own OpenCV check out my [blog](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-doylet9/blob/master/docs/blog/compiling_open_cv.md) on how to do that.

#### How does SIFT work?

1. Scale Space Construction
    * This is where the image is progressively blurred out more and more to have images that range from full detail to little detail in them. Then a range for each blurred image is created of different scaled images to create a scale space of several images.
2. LoG Approximations
    * We now want to make this scale space useful. We do this by attempting to find key points in it. A good way to do this is blur the image and then calculate second order derivations on it or the "laplacian". This operation is called the Laplacian of Gaussian. It is extremely sensitive to noise but the blur on the images helps this. Another problem is calculating second order derivations in computationally expensive. To generate Laplacia of Guassian images quickly we use the scale space by calculating the difference between two consecutive scales, or the difference of two Gaussians.
3. Finding Keypoints
    * A keypoint is marked as a maxima if it is the greatest of all it's neighbors including the image above and below it in the scale. The same is done for the minima. These are approimate minima and maxima because the real minimal and maxima almost always mathematically falls between pixels. Subpixel minima/maxima is done by getting the Taylor expansion of the image.
4. Remove Bad Keypoints
    * A lot of keypoints can be generated in the previous step and many of these are of low contrast or lie on an edge. In this case they are not much use so they can be discarded. 
5. Assigning Orientations to Keypoints
    * We now have keypoints and their scale (we know this from the scale of the image they were found in). We want to find the orientation for the keypoints. For this we look to the neightbour around the keypoints for gradients and magnitudes.
6. Generating the Features
    * We want to be able to identify features so we can create a fingerprint of keypoints for a feature. We create a window around the feature. We then split up that windows into even segments and generate a gradient angle for each window then normalise all the values.

This is a complex algorithm but diagrams make it far more manageable. The source for the quick explination is adapted from [http://aishack.in/tutorials/sift-scale-invariant-feature-transform-introduction/](http://aishack.in/tutorials/sift-scale-invariant-feature-transform-introduction/)

### TLSH - Trend Micro Locality Sensitive Hash

This locality sensitive hash function allows the keypoints to be hashed before being put into the database. This allows the result of our query to be a subset of the database rather than the entire database. We can search based on the hash to find close matches to the hash and return the values that are close to it.

### Database Search

For the database search we wanted to search based on how close the hash was. For this we used the Levenshtein distance between the hash in the query and the hash in the database. This mean that is can be a fast match rather than pulling back the whole database. This also means that we can tune the query to come back with more or less accurate results. The higher we set the threshold to the more sets of keypoints will come back. But if the Levenshtein distance is too low it may miss the keypoints.

It is important to remember that the Levenshtein distance works as a holistic to find matching key points but it is very often the case that non matching images with have very close hashes. This is due to the nature of the hash not being design specifically for this purpose. In future work I would love to design my own hashing function that would do this better and give more accurate results. The more accurate the hash function can be the faster this application will become. This will make a huge difference to the speed because every set of keypoints that come from the query are matched against the original image to find the image with the highest amount of keypoints matching. The less of these that there are, will dramatically increase the speed of this search.

To get the most of speed out of the query, we want to calculate the Levenshtein distance as close to the database as possible. If we were to query the database and then run the Lenvenshtein distance in python this would be an almost worthless task. Instead we can implement plsql. This is an extreme learning curve close to the deadline and one that was not accounted for in the gantt char at the planning phase of the project. It was therefore elected to use the function already built into the extra modules of PostgreSQL. This was a fast solution and one that worked very well. 


## Function Usage

#### data_management.py
```
class DataObject:
    '''
    Class to represent a keypoint to write to database

    self.pt: (Float, Float)
    self.size: Float
    self.angle: Float
    self.octave: Int
    self.class_id: Int
    self.desc: Numpy Array
    '''
    
    def __init__(self, pt, size, angle, response, octave, class_id, desc):
        '''
        Initalises variables for function
        '''
    
    def __str__(self):
        '''
        Returns string representation for output to database
        '''
        
def pack_keypoints(keypoints, desc):
    '''
    This will take a list of opencv keypoints and turn them into a list of 
    DataObjects definined above

    keypoints: List
    desc: Numpy Array

    Returns: List (of DataObjects)
    '''
    
def unpack_keypoints(kp_lst):
    '''
    Take list of DataObjects and converts back to list of opencv keypoints

    Returns: (List, Numpy Array)
    '''
    
def connect_postgres():
    '''
    Opens a connection to a postgres database

    Returns: Database connection object
    '''

def write_postgres(dhash, datapoint, url='Unknown'):
    '''
    Takes a hash of datapoint, datapoint and source url 
    and writes that to the database

    dhash: String (Hash of datapoints)
    datapoint: String (Keypoints of an image)
    url: String (Source of image)

    Returns None
    '''

def query_postgres(dhash):
    '''
    Reads in a hash and queries database for a similar hash

    dhash: String (Hash of keypoints)

    Returns: String (Results of query)
    '''
 ```
 
#### img_manipulation.py
```
def get_keypoints(img):
    '''
    Takes an image and returns its keypoints and descriptors
    
    img: cv2.imread object

    returns: (matrix of key points, matrix of descriptors) 
    '''

def get_match(desc1, desc2):
    '''
    Takes two matrixes of descriptors about and image 
    and uses a Flann based matcher to match these matrixes

    desc1: matrix of descriptors
    desc2: matrix of descriptors

    returns: list of matching descriptors
    '''

def rotate_img(image):
    '''
    Will rotate a matrix corresponding to an image

    image: Matrix corresponding to an image

    returns: Rotated matrix corresponding to an image
    '''

def load_img(img):
    '''
    Takes a file name and loads that image into an opencv matrix

    img: String

    returns: opencv matrix
    '''

def match_images(org_img, comp_img):
    ''' 
    Will attempt to match two images

    img1: string corresponding to filename of image
    img2: string corresponding to filename of image
 
    results: String, Percentage accuracy
    '''
```
