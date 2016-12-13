import cv2
import numpy as np
import math, sys


def find_hand(img):
    # convert image in greyscale
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # blurr the image
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)

    # threshold the image, returning a binary image
    _, thresholded = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # find the contours in the binary image
    # the returned values are:
    # - contours is a list of the contours detected. Each contour is
    #   represented as a list of points
    # - hierarchy is a list containing info abour the image topology.
    contours, hierarchy = cv2.findContours(thresholded.copy(),cv2.RETR_TREE, \
            cv2.CHAIN_APPROX_NONE)

    # find the contour delimiting the biggest area
    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    # find and draw the rectangle delimiting the hand
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),0)
    return cnt, grey, blurred, thresholded

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
    return defects, drawing

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
    return count_defects

def find_gestures(img):
    hand_contour, grey, blurred, thresholded = find_hand(img)
    defects, drawing = find_defects(img, hand_contour)
    fingers_count = count_defects(img, hand_contour, defects)
    return fingers_count, grey, blurred, thresholded, drawing

def find_gestures_in_image(source, show):
    image = cv2.imread(source)
    fingers_count, grey, blurred, thresholded, drawing = find_gestures(image)
    if show:
        show_images((image, thresholded, drawing))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return fingers_count

def find_gestures_in_video(source, show):
    cap = cv2.VideoCapture(source)
    total_count = fingers_count = 0
    try:
        while(cap.isOpened()):
            ret, image = cap.read()
            previous_count = fingers_count
            fingers_count, grey, blurred, thresholded, drawing = find_gestures(image)
            if fingers_count != previous_count:
                total_count += fingers_count
                sys.stderr.write(str(fingers_count))
            if show:
                show_images((image, thresholded, drawing))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # release the cam that we locked before
        cap.release()
        cv2.destroyAllWindows()
    return total_count


def show_images(images):
    for i, image in enumerate(images):
        cv2.imshow("%d"%i, image)
