import cv2
import numpy as np
import math
import sys
from argparse import ArgumentParser


ap = ArgumentParser(description = 'This program allows you to analyze a video' +
                                  ' and recognize hand gestures')
ap.add_argument('-b', '--blurring', default = 35, type = int,
                help = 'Blurring value which represents the grade of blurring' +
                'you want')
ap.add_argument('-t', '--threshold', default = 127, type = int,
                help = 'Thresholding value to recognize the colour of the hand')

source = ap.add_mutually_exclusive_group()
source.add_argument('-v', '--video', default = '../gesture.avi',
                help = 'Source of the video you want to analyze')
source.add_argument('-w', '--webcam', action = 'store_true',
                help = 'Include this option if you want to use your default' +
                        'webcam as image source')

args = ap.parse_args()
#rect = {"top_left": (0,0), "bottom_right": (300,500)}

# Source of images
if not args.webcam:
    cap = cv2.VideoCapture(args.video)
else:
    cap = cv2.VideoCapture(0)

while(cap.isOpened()):
#while False:
    # Get the webcam image
    ret, img = cap.read()

    # cv2.rectangle(img,rect["top_left"], rect["bottom_right"],(0,255,0),0)
    # crop_img = img[rect["top_left"][0]:rect["bottom_right"][0],
    #                rect["top_left"][1]:rect["bottom_right"][1]]
    crop_img = img

    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)

    blurred = cv2.GaussianBlur(grey, value, 0)

    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #cv2.imshow('Thresholded', thresh1)

    contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
            cv2.CHAIN_APPROX_NONE)

    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img,far,1,[0,0,255],-1)
        #dist = cv2.pointPolygonTest(cnt,far,True)
        cv2.line(crop_img,start,end,[0,255,0],2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)
    # if count_defects == 1:
    #     cv2.putText(img,"I can see 1 finger", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    # elif count_defects == 2:
    #     cv2.putText(img,"I can see 2 fingers", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    # elif count_defects == 3:
    #     cv2.putText(img,"I can see 3 fingers", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    # elif count_defects == 4:
    #     cv2.putText(img,"I can see 4 fingers", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    # else:
    #     cv2.putText(img,"I can see 5 fingers", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

    cv2.imshow('drawing', drawing)
    cv2.imshow('end', crop_img)
    cv2.imshow('threshold', thresh1)
    #cv2.imshow('Gesture', img)

    sys.stderr.write("%d\n" % count_defects)
    #all_img = np.hstack((drawing, crop_img))
    #cv2.imshow('Contours', all_img)
    k = cv2.waitKey(10)
    if cv2.waitKey(1) & 0xFF == ord('q')  or k == 27:
        break
