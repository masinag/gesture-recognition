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
    ap.add_argument('-s', '--show', default = 127, action = 'store_true',
                    help = 'Show windows the steps of the image processing')

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
        print(mygesture.count_fingers_in_video(args.video, args.show))
    elif args.webcam>=0:
        print(mygesture.count_fingers_in_video(args.webcam, args.show))
    elif args.image:
        print(mygesture.count_fingers_in_image(args.image, args.show))
