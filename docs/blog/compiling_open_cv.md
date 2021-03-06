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


