import cv2
import numpy as np


class MouseCoordinate:
    position = []

    def __init__(self):
        self.position = []

    def select_point(self, event, x, y, flags, param):  # int event, int x, int y, ...
        if len(self.position) > 2:
            self.position = []
            print("No selection. Please select a point on the image.")

        # if event == cv2.EVENT_LBUTTONDBLCLK:  # left mouse button DOUBLE click in this case
        if event == cv2.EVENT_LBUTTONDOWN:  # single click
            self.position.append([x, y])

    def getPointOne(self):
        return self.position[0]

    def getPointTwo(self):
        return self.position[1]


if __name__ == '__main__':

    image = cv2.imread('paint.jpg',
                       cv2.IMREAD_COLOR)
    # IMREAD_COLOR ... Load the image in BGR color format, ignore alpha channel
    cv2.namedWindow('image')

    height, width, depth = image.shape  # getting the image size and channel values

    MouseObject = MouseCoordinate()

    cv2.setMouseCallback('image', MouseObject.select_point)  # callback function for the image window

    while 1:
        cv2.imshow('image', image)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:  # ESC-key (27) system dependant
            break

        if k == ord('q'):
            mask = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            endframe = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # converting image from BGR to HSV with the opencv lib

            # coordinates of first click
            x1 = MouseObject.getPointOne()[0]
            y1 = MouseObject.getPointOne()[1]

            # coordinates of second click
            x2 = MouseObject.getPointTwo()[0]
            y2 = MouseObject.getPointTwo()[1]

            # mask[y1, x1]  returns HSV
            selectedHue1 = mask[y1, x1][0]
            selectedHue2 = mask[y2, x2][0]

            threshold = 30  # define the range of the first selected color

            print(selectedHue1)
            print(selectedHue2)

            for rows in range(0, width):  # iterating through the multidimensional array of the immage (in HSV)
                for cols in range(0, height):

                    if (mask[cols, rows, 0] > selectedHue1 - threshold) and (
                            mask[cols, rows, 0] < selectedHue1 + threshold):
                        # if the hue value of the image is in the range(first selection +/- threshold)

                        endframe[cols, rows, 0] = selectedHue2

                        # hue will be replaced with the hue value of the second selection

            endframeBGR = cv2.cvtColor(endframe, cv2.COLOR_HSV2BGR)
            # converting image back, from HSV to BGR

            cv2.imshow("endframe", endframeBGR)

    cv2.destroyAllWindows()
