"""This program is an example of gesture recognition using Python and OpenCV. It
allows you to analyze a image, a video or to use your webcam as image source.
You can also decide the values used to process the image, such as the parameters
for the blurring and the thresholding.

Examples:
    $ python gesture-recognition --image media/images/one.jpg --blur 40

    $ python gesture-recognition --image media/images/two.jpg --show -t 150

    $ python gesture-recognition --video media/videos/gesture.avi --show

"""
if __name__ == '__main__':
    import mygesture, logging
    from argparse import ArgumentParser

    #configure logger options, set the default level at info
    logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    ap = ArgumentParser(description = 'This program allows you to analyze a video' +
                                      ' and recognize hand gestures')
    ap.add_argument('-b', '--blur', default = 35, type = mygesture.odd,
                    help = 'Blurring value which represents the grade of blurring' +
                    'you want. This value must be odd.')
    ap.add_argument('-t', '--threshold', default = 127, type = int,
                    help = 'Thresholding value to recognize the colour of the hand')
    ap.add_argument('-s', '--show', default = True, action = 'store_true',
                    help = 'Show windows the steps of the image processing')

    source = ap.add_mutually_exclusive_group(required = True)
    source.add_argument('-v', '--video',
                    help = 'Location of the video you want to analyze')
    source.add_argument('-w', '--webcam', type = int,
                    help = 'Use the webcam as video input. The value for the ' +
                           'default webcam is 0')
    source.add_argument('-i', '--image',
                    help = 'Location of the image you want to analyze')
    # source.add_argument('-d', '--debug', action = 'store_true',
    #                 help = 'Show debugging informations')

    args = ap.parse_args()

    logging.debug('%s' % args)

    try:
        if args.video:
            logger.info('Counted %d fingers in the video' %
                         mygesture.count_fingers_in_video(args.video,
                                                          args.threshold,
                                                          args.blur,
                                                          args.show))
        elif not args.webcam is None:
            logger.info('Counted %d fingers in the webcam input' %
                         mygesture.count_fingers_in_video(args.webcam,
                                                          args.threshold,
                                                          args.blur,
                                                          args.show))
        elif args.image:
            logger.info('Counted %d fingers in the image' %
                         mygesture.count_fingers_in_image(args.image,
                                                          args.threshold,
                                                          args.blur,
                                                          args.show))
    except mygesture.WrongSourceError:
        logger.error('Error while trying to open %s' % (args.image or
                                                        args.video or
                                                        args.webcam))
