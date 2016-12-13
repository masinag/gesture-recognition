import cv2, math, sys, mygesture
import numpy as np
from argparse import ArgumentParser

if __name__ == '__main__':
    ap = ArgumentParser(description = 'This program allows you to analyze a video' +
                                      ' and recognize hand gestures')
    ap.add_argument('-b', '--blurring', default = 35, type = int,
                    help = 'Blurring value which represents the grade of blurring' +
                    'you want')
    ap.add_argument('-t', '--threshold', default = 127, type = int,
                    help = 'Thresholding value to recognize the colour of the hand')

    source = ap.add_mutually_exclusive_group(required = True)
    source.add_argument('-v', '--video',
                    help = 'Location of the video you want to analyze')
    source.add_argument('-w', '--webcam', type = int,
                    help = 'Use the webcam as video input. The value for the ' +
                           'default webcam is 0')
    source.add_argument('-i', '--image',
                    help = 'Location of the image you want to analyze')

    args = ap.parse_args()

    if args.video:
        mygesture.find_gestures_in_video(args.video)
    elif args.webcam:
        mygesture.find_gestures_in_video(args.webcam)
    elif args.image:
        print(mygesture.find_gestures_in_image(args.image))
