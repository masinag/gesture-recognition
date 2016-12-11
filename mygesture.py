import cv2
import numpy as np
import math


def find_hand(img):
    # convert image in greyscale
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # blurr the image
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)

    # threshold the image, returning a binary image
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # find the contours in the binary image
    # the returned values are:
    # - contours is a list of the contours detected. Each contour is
    #   represented as a list of points
    # - hierarchy is a list containing info abour the image topology.
    contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
            cv2.CHAIN_APPROX_NONE)

    # find the contour delimiting the biggest area
    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    # find and draw the rectangle delimiting the hand
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),0)
    return cnt

def find_defects(img, contour):
    # find the convex hull of the contour
    hull = cv2.convexHull(contour)

    # this creates a new black images( all pixels value 0) with the size of
    # our image
    drawing = np.zeros(img.shape,np.uint8)
    # on the new image, draw the hand contour and its convex hull
    cv2.drawContours(drawing,[contour],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    # now we get the indices of the convex hull points, while before we got
    # the real points
    hull = cv2.convexHull(contour,returnPoints = False)
    # find the convexity defects of the contour.
    defects = cv2.convexityDefects(contour,hull)
    # (?)
    # cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    # (?)
    return defects

def count_defects(img, contour, defects):
    count_defects = 0
    # now we try to decide what defects we are interested in (?)
    for i in range(defects.shape[0]):
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
    return img, count_defects

def find_gestures(img):
    hand_contour = find_hand(img)
    defects      = find_defects(img, hand_contour)
    fingers_count = count_defects(img, contour, defects)
    return fingers_count
