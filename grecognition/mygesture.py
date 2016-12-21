"""This module contains some useful function for the gesture recognition in an
image or in a video."""

import cv2, argparse
import numpy as np
import math, sys

class WrongSourceError(Exception):
    """Class used to handle exceptions raised during image or video loading."""
    pass

def odd(n):
    n = int(n)
    if n%2 == 0:
         raise argparse.ArgumentTypeError("%s is an invalid odd int value" % n)
    return n

def find_hand(img, threshold, blur):
    """
    Finds the contour of a hand in an image

    This function analyzes an image, search for a hand and in the case it
    finds it, the contour of the hand is returned. The function returns also
    the images produced during the analysis.

    Parameters
    ----------
    img : numpy.ndarray
        The image you want to analyze

    Returns
    -------
    numpy.ndarray
        Contour of the hand found
    numpy.ndarray
        Greyscaled version of the original image
    numpy.ndarray
        Blurred version of the greyscaled image
    numpy.ndarray
        Binary version of the blurred image, resulted after thresholding
    """
    # convert image in greyscale
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blurr the image
    value = (blur, blur)
    blurred = cv2.GaussianBlur(grey, value, 0)
    # threshold the image, returning a binary image
    _, thresholded = cv2.threshold(blurred, threshold, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # find the contours in the binary image
    # the returned values are:
    # * contours is a list of the contours detected. Each contour is
    #   represented as a list of points
    # * hierarchy is a list containing info abour the image topology.
    contours, hierarchy = cv2.findContours(thresholded.copy(),cv2.RETR_TREE, \
            cv2.CHAIN_APPROX_NONE)

    # find the contour delimiting the biggest area
    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    # find the rectangle delimiting the hand
    x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),0)
    return cnt, grey, blurred, thresholded

def find_defects(img, contour):
    """
    Finds the convexity defects of a contour.

    This function, given in input an image and a contour delimiting an object
    in the image (such as a hand), finds the convexity defects of this contour.
    A convexity defect is like a 'cavity' in the object, an area that does not
    belong to the object but that is located inside its convex hull.

    Parameters
    ----------
    img : numpy.ndarray
        The image containing the contour
    contour: numpy.ndarray
        The contour of which you want to find the convexity defects

    Returns
    -------
    numpy.ndarray
        Convexity defects found
    numpy.ndarray
        Image showing the contour and its convex hull
    """
    # find the convex hull of the contour
    hull = cv2.convexHull(contour)

    # this creates a new black images( all pixels value 0) with the size of
    # our image. We will use thei
    drawing = np.zeros(img.shape,np.uint8)
    # on the new image, draw the hand contour and its convex hull
    cv2.drawContours(drawing,[contour],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    # now we get the indices of the convex hull points, while before we got
    # the real points
    hull = cv2.convexHull(contour,returnPoints = False)
    # find the convexity defects of the contour.
    defects = cv2.convexityDefects(contour,hull)
    return defects, drawing

def count_fingers(img, contour, defects):

    count_defects = 0
    # now we try to decide what defects we are interested in
    for i in range(defects.shape[0]):
        # for every defect point we calculate the angle and then we decide if
        # we have found a finger.
        s,e,f,d = defects[i,0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
    return count_defects

def detect_num_fingers(img, contours, defects):
    """Counts the fingers in a contour.

    This function, given a contour representing a hand and its convexity defects,
    understands which of them are relevant for the fingers count.

    Parameters
    ----------
    img : numpy.ndarray
        The image containing the contour
    contour : numpy.ndarray
        The contour delimiting the hand
    defects : numpy.ndarray
        The convexity defects of the contour

    Returns
    -------
    int
        Number of fingers counted
    """

    # if there are no convexity defects, possibly no hull found or no
    # fingers extended
    if defects is None:
        return 0

    # we assume the wrist will generate two convexity defects (one on each
    # side), so if there are no additional defect points, there are no
    # fingers extended
    if len(defects) <= 2:
        return 0

    # if there is a sufficient amount of convexity defects, we will find a
    # defect point between two fingers so to get the number of fingers,
    # start counting at 1
    num_fingers = 1
    for i in range(defects.shape[0]):
        # each defect point is a 4-tuple
        start_idx, end_idx, farthest_idx, _ = defects[i, 0]
        start = tuple(contours[start_idx][0])
        end = tuple(contours[end_idx][0])
        far = tuple(contours[farthest_idx][0])

        # if angle is below a threshold, defect point belongs to two
        # extended fingers
        if angle_rad(np.subtract(start, far),
                     np.subtract(end, far)) < deg2rad(80.0):
            # increment number of fingers
            num_fingers = num_fingers + 1
    return min(5, num_fingers)

def angle_rad(v1, v2):
    """Angle in radians between two vectors

    This method returns the angle (in radians) between two array-like
    vectors using the cross-product method, which is more accurate for
    small angles than the dot-product-acos method.

    Parameters
    ----------
    v1 : numpy.ndarray
        The first vector
    v2 : numpy.ndarray
        The second vector

    Returns
    -------
    numpy.float64
        Angle in radians between the two vectors
    """
    return np.arctan2(np.linalg.norm(np.cross(v1, v2)), np.dot(v1, v2))

def deg2rad(angle_deg):
    """Convert degrees to radians

    This method converts an angle in radians e[0,2*np.pi) into degrees
    e[0,360)

    Parameters
    ----------
    angle_deg : numpy.float64
        The angle in degrees

    Returns
    -------
    numpy.float64
        Angle expressed in radians
    """
    return angle_deg/180.0*np.pi

def find_gestures(img, threshold, blur):
    """
    Finds the gestures in an image.

    This function tries to understand the hand gestures in an image. This means
    that it looks for an hand and counts the fingers shown.

    Parameters
    ----------
    img : numpy.ndarray
        The image you want to analyze

    Returns
    -------
    int
        Number of fingers counted
    numpy.ndarray
        Greyscaled version of the original image
    numpy.ndarray
        Blurred version of the greyscaled image
    numpy.ndarray
        Binary version of the blurred image, resulted after thresholding
    numpy.ndarray
        Image showing the contour of the hand and its convex hull
    """
    hand_contour, grey, blurred, thresholded = find_hand(img, threshold, blur)
    defects, drawing = find_defects(img, hand_contour)
    # fingers_count = count_fingers(img, hand_contour, defects)
    fingers_count = detect_num_fingers(img, hand_contour, defects)

    return fingers_count, grey, blurred, thresholded, drawing

def count_fingers_in_image(source, show = False):
    """
    Counts the fingers in an image.

    This function analyzes an image and returns the number of fingers seen. If
    required it also shows the step images resulted from the image processing.

    Parameters
    ----------
    source : string
        The location of the image you want to analyze.
    show: bool
        It should be true if you want to show the step images. Default value is
        false.

    Returns
    -------
    int
        Number of fingers counted
    """
    image = cv2.imread(source)
    if image is None:
        raise WrongSourceError, "Error: unable to open %s" % source
    fingers_count, grey, blurred, thresholded, drawing = find_gestures(image,
                                threshold, blur)
    if show:
        images = {"Original": image, "Thresholded": thresholded, "Contour": drawing}
        show_images(images)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return fingers_count

def count_fingers_in_video(source, threshold, blur, show):
    """
    Counts the fingers in a video.

    This function analyzes a video and returns the number of fingers seen. If
    required it also shows the step images resulted from the image processing
    and prints the number of fingers counted on the standard error.

    Parameters
    ----------
    source : string or int
        If it is a string, it is interpreted as the location of the video you
        want to analyze. If it is an integer, it is interpreted as the number of
        the webcam you want to use. The default webcam is the number 0.
    show: bool
        It should be true if you want to show the step images and read the
        number of fingers counted at the moment. Default value is false.

    Returns
    -------
    int
        Sum of the fingers counted during the whole video.
    """
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise WrongSourceError, "Error: unable to open %s" % source
    total_count = fingers_count = 0
    try:
        while(cap.isOpened()):
            ret, image = cap.read()

            if image is None:
                break
            else:
                previous_count = fingers_count
                fingers_count, grey, blurred, thresholded, drawing = find_gestures(image,
                                            threshold, blur)
                if fingers_count != previous_count:
                    total_count += fingers_count
                    if show:
                        # write the fingers count on the standard error
                        sys.stderr.write("%d\n" % fingers_count)
                if show:
                    images = {"Original": image, "Thresholded": thresholded, "Contour": drawing}
                    show_images(images)
                # if the 'q' key is pressed, the windows will be closed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
    finally:
        # release the cam that we locked before
        cap.release()
        cv2.destroyAllWindows()
    return total_count


def show_images(images):
    """
    Shows the given images.

    This function takes a dictionary in which every key is a string representing
    the name of a window and its value is the image we want to display in that
    window.

    Parameters
    ----------
    images: dict
        This dictionary should containg the name of the windows (str) as keys and the
        images you want to display as values (numpy.ndarray).

    Returns
    -------
    """
    for name, image in images.items():
        cv2.imshow(name, image)
