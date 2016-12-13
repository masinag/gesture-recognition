# gesture-recognition

This program is an example of gesture recognition using Python and OpenCV. It
allows you to analyze a image, a video or to use your webcam as image source.
You can also decide the values used to process the image, such as the parameters
for the blurring and the thresholding.

# Project structure

In the gesture-recognition/ directory you will find the code of the project.
This includes a __main__.py file which is the one you can run, and a mygesture.py
file which is a library with useful function for this project. The __init__.py
file marks this directory as a python package directory.

In the media/ directory you will find two sub-directories: images/ and videos/,
which contain some file that you can use as examples.

## Installation

Below is described the installation process on Ubuntu 16.10:

* Python version ‘2.7.12’:
 	  installed by default.
* OpenCV python library version ‘2.4.9.1’:
 	  $ sudo apt-get install python-opencv
* Numpy python library version ‘1.11.0’:
    $ sudo apt-get install python-numpy
* Math python library:
 	  $ installed by default.
* Argparse python library version ‘1.1’:
    $ installed by default.

## Usage
Below there are some examples of usage:

    $ python gesture-recognition --image media/images/one.jpg --blur 40

    $ python gesture-recognition --image media/images/two.jpg --show -t 150

    $ python gesture-recognition --video media/videos/gesture.avi --show

You can read more details running the command:

    $ python gesture-recognition --help


## Video

link: [http://goo.gl/fui2MH ](http://goo.gl/fui2MH)

[![IMAGE ALT TEXT](https://img.youtube.com/vi/QYiypuWZPU0/0.jpg)](https://www.youtube.com/watch?v=QYiypuWZPU0)

## Credits

link: [https://github.com/vipul-sharma20/gesture-opencv](https://github.com/vipul-sharma20/gesture-opencv)
