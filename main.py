"""This program is an example of gesture recognition using Python and OpenCV. It
allows you to analyze a image, a video or to use your webcam as image source.
You can also decide the values used to process the image, such as the parameters
for the blurring and the thresholding.

Examples:
    $ python main.py --image media/img/one.jpg --blur 40

    $ python main.py --image media/img/two.jpg --show -t 150

    $ python main.py --video media/video/gesture.avi --show

"""
if __name__ == '__main__':
    import mygesture
    from argparse import ArgumentParser

    ap = ArgumentParser(description = 'This program allows you to analyze a video' +
                                      ' and recognize hand gestures')
    ap.add_argument('-b', '--blur', default = 35, type = int,
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
