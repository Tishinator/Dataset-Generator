import cv2
import numpy as np


@staticmethod
def create_zoomed_in_image(image, zoom, posx, posy):
    # ALL IMAGES SHOULD BE THIS SIZE
    height = image.shape[0]
    width = image.shape[1]

    x_offset = int((width - image.shape[1]) / 2) + posx
    y_offset = int((height - image.shape[0]) / 2) + posy

    #  Resize image to zoom amount
    resizedImage = cv2.resize(image, (int(zoom * width), int(zoom * height)), interpolation=cv2.INTER_LINEAR)

    #  crop image to original height & width
    startPosX = posx
    endPosX = width + posx

    startPosY = posy
    endPosY = height + posy

    croppedImage = resizedImage[startPosY:endPosY, startPosX:endPosX]

    return croppedImage


@staticmethod
def create_zoomed_out_image(image, zoom, posx, posy):
    # ALL IMAGES SHOULD BE THIS SIZE
    height = image.shape[0]
    width = image.shape[1]

    x_offset = int((width - image.shape[1]) / 2) + posx
    y_offset = int((height - image.shape[0]) / 2) + posy

    #  Resize the image (Zoom out / shrink image )
    img = cv2.resize(image.image_data, (int(zoom * width), int(zoom * height)), interpolation=cv2.INTER_AREA)

    # Create black blank image
    blank_image = np.zeros((height, width, 3), np.uint8)

    blank_image[:] = (255, 255, 255)

    try:
        blank_image[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img
        return blank_image

    except Exception as e:
        # print(e)
        f = ":("
        return None, [(-1, -1), (-1, -1), (-1, -1), (-1, -1)]
    # cv2.imshow("Blank image", blank_image)
    # cv2.waitKey(0)