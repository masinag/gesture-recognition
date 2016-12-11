import cv2, math, argparse
import numpy as np

# Source of images
cap = cv2.VideoCapture('../gesture3.avi')

#rect = {"top_left": (0,0), "bottom_right": (300,500)}
ap = argparse.ArgumentParser()
ap.add_argument('-t', '--threshold', default = 127, type = int,
                help = 'Threshold value')
ap.add_argument('-b', '--blurring', default = 35, type = int,
                help = 'Blurring value')
args = ap.parse_args()

while(cap.isOpened()):
    # Get the webcam image
    ret, img = cap.read()

    # cv2.rectangle(img,rect["top_left"], rect["bottom_right"],(0,255,0),0)
    # crop_img = img[rect["top_left"][0]:rect["bottom_right"][0],
    #                rect["top_left"][1]:rect["bottom_right"][1]]
    crop_img = img

    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (args.blurring, args.blurring)

    blurred = cv2.GaussianBlur(grey, value, 0)

    cv2.imshow('Blurred', blurred)

    _, thresh1 = cv2.threshold(blurred, args.threshold, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow('Thresholded', thresh1)

    #
    # contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
    #         cv2.CHAIN_APPROX_NONE)
    #
    # cnt = max(contours, key = lambda x: cv2.contourArea(x))
    #
    # x,y,w,h = cv2.boundingRect(cnt)
    # cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
    # hull = cv2.convexHull(cnt)
    # drawing = np.zeros(crop_img.shape,np.uint8)
    # cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    # cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    # hull = cv2.convexHull(cnt,returnPoints = False)
    # defects = cv2.convexityDefects(cnt,hull)
    # count_defects = 0
    # cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    # for i in range(defects.shape[0]):
    #     s,e,f,d = defects[i,0]
    #     start = tuple(cnt[s][0])
    #     end = tuple(cnt[e][0])
    #     far = tuple(cnt[f][0])
    #     a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    #     b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
    #     c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
    #     angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
    #     if angle <= 90:
    #         count_defects += 1
    #         cv2.circle(crop_img,far,1,[0,0,255],-1)
    #     #dist = cv2.pointPolygonTest(cnt,far,True)
    #     cv2.line(crop_img,start,end,[0,255,0],2)
    #     #cv2.circle(crop_img,far,5,[0,0,255],-1)
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
    # #cv2.imshow('drawing', drawing)
    # #cv2.imshow('end', crop_img)
    # cv2.imshow('Gesture', img)
    # all_img = np.hstack((drawing, crop_img))
    # cv2.imshow('Contours', all_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
