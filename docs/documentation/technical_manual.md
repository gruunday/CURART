![CURART LOGO](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/raw/master/docs/blog/images/CURART_WIDE.png)

# Technical Manual

## Contents

1. Introduction
    - Overview
    - Glossary
2. System Architecture
    - 2.1 Language Choice
3. High-Level Design
    - 3.1 Inital vs Current Design
4. Problems and Resolution
5. Installation Guide
6. Configuration 
7. Testing
    - 7.1 Functional Testing
    - 7.2 Non Functional Testing 
8. Function Usage

## Introduction
### Overview
This project is written in python 3 to attempt to match images of artworks. The purpose of this is to attempt to find people who are using images of artworks that are in breach of copywright and modified from original or find the source of an artwork. This is implemented using the OpenCV version of the SIFT algorithm. Therefore it is not for comercial use and purely a research project.

While the domain of this project is restricted here to the domain of just artworks, this project can easily be used for other purposes of finding images that are made up of the exact same content. It will not use context at all for matcing, i.e a different angle of the same building. For this to match it is a goal of this project to only match if the images are the same.

The second aim of the project is to work at scale. If this tool is to be usable the user should not have to wait hours to find a result. This research project should be able to get matches in a reasonable amount of time.

#### Context Diagram
![Context Diagram](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-doylet9/raw/master/docs/documentation/images/Curart_context_diagram.png)

### Glossary
**TODO**
* OpenCV
* Docker: Any reference to containers, you can presume that these are docker containers unless otherwise stated.
* Container
* Traefic
* AWS
* Postgres


## System Architecture
![System Architecutre Diagram](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-doylet9/raw/master/docs/documentation/images/Curart_system_arch.png)

#### Language Choice
Python is an easy to develop language but has some speed impacts when it comes to heavy computation such as images. But after research into the SIFT algorithm I saw others that had successfully implemented SIFT with python with minimal impacts to speed. [Source](http://aishack.in/tutorials/implementing-sift-opencv/) It became apparent that implementing SIFT was not new and had been done many times before. So rather than reinventing the wheel I wanted to add to work that has been done before me.

This leads to the research into previous implementations of SIFT algorithm. The opencv library's implementation was one that came up again and again as the most optimised and accurate. This is the one chosen and is written in C with a python interface so this allows us to use it with python. 

Python has many packages for webframe works that many other low level languages do not. This also made it ideal that we could use it for many different uses throughout the architecture of the project. 

Python is also the language I am most comfortable in, and one of the non functional requirements of this project is to meet the project deadline. There for this is the language I can get all of the features I want to add into this project in time for the final deadline. 

Python2.7 was not concidered because of the end of it's life in 8 months at time of writing.

All these points align with me choosing python for this project. 


## High-Level Design

### Initial Design

The inital design of this project has changed a lot since it was first conseived. This was due to lack of experience in using the technologies and also unforseeable issues that were encountered. We will talk about the differences in this section and we will talk about the problems encountered and why the design has chaned in a later section.

The first major design change in the lack of aws lambda functions. These have been replaced by docker containers that are load balanced by a software defined load balancer called traefik. This will allow the same amount of scalability but does mean that the base server will have to have to be of sufficienct size to handle the traffic rather than a small server that can hand off the computation to another compute module. 

The datastore for this project as also changed from an amazon s3 bucket to a postgreSQL database hosted by aws. This pivot was due to the purpose of s3 buckets being an object store and unstructed data. This was a slow design that would invole searching the whole database if you were looking for a best match, like we are. A better solution was to hash object on the way into a postgreSQL database and create a structured form for them. Then on query we use the levenshtein distance on the hash to find the best match quickly. This still provides us with the reliability and availabilty of amazon services which was desirable at the begining of this project.

The webserver has also now been containerised per container rather than one for all. Each container handles its traffic internal. The traefik load balancer for the containers passes the traffic to the container in a round robin method.


### Current Design
**TODO**

## Problems and Resolution
**TODO**

## Installation Guide
**TODO**

## Configuration 
**TODO**

## Testing
**TODO**

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


