import math

import numpy as np
import cv2


# Usage:
#     Change main function with ideal arguments
#     Then
#     from image_tranformer import ImageTransformer
#
# Parameters:
#     image_path: the path of image that you want rotated
#     shape     : the ideal shape of images image, None for original size.
#     theta     : rotation around the x axis
#     phi       : rotation around the y axis
#     gamma     : rotation around the z axis (basically a 2D rotation)
#     dx        : translation along the x axis
#     dy        : translation along the y axis
#     dz        : translation along the z axis (distance to the image)
#
# Output:
#     image     : the rotated image
#
# Reference:
#     1.        : http://stackoverflow.com/questions/17087446/how-to-calculate-perspective-transform-for-opencv-from-rotation-angles
#     2.        : http://jepsonsblog.blogspot.tw/2012/11/rotation-in-3d-using-opencvs.html


class ImageTransformer(object):
    """ Perspective transformation class for image
        with shape (height, width, #channels) """

    def __init__(self, image):
        self.image = image

        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.num_channels = self.image.shape[2]

    """ Wrapper of Rotating a Image """

    def rotate_along_axis(self, theta=0, phi=0, gamma=0, dx=0, dy=0, dz=0):
        # Get radius of rotation along 3 axes
        rtheta, rphi, rgamma = get_rad(theta, phi, gamma)

        # Get ideal focal length on z axis
        # NOTE: Change this section to other axis if needed
        d = np.sqrt(self.height ** 2 + self.width ** 2)
        self.focal = d / (2 * np.sin(rgamma) if np.sin(rgamma) != 0 else 1)

        dz = self.focal

        # Get projection matrix
        mat = self.get_m(rtheta, rphi, rgamma, dx, dy, dz)

        image = cv2.warpPerspective(self.image.copy(), mat, (self.width + (dx*2), self.height + (dy*2)), borderValue=(255, 0, 0))

        return image


    """ Get Perspective Projection Matrix """
    def get_m(self, theta, phi, gamma, dx, dy, dz, focal=None):
        w = self.width
        h = self.height
        if focal is None:
            f = self.focal
        else:
            f=focal

        # Projection 2D -> 3D matrix
        A1 = np.array([[1, 0, -w / 2],
                       [0, 1, -h / 2],
                       [0, 0, 1],
                       [0, 0, 1]])

        # Rotation matrices around the X, Y, and Z axis
        RX = np.array([[1, 0, 0, 0],
                       [0, np.cos(theta), -np.sin(theta), 0],
                       [0, np.sin(theta), np.cos(theta), 0],
                       [0, 0, 0, 1]])

        RY = np.array([[np.cos(phi), 0, -np.sin(phi), 0],
                       [0, 1, 0, 0],
                       [np.sin(phi), 0, np.cos(phi), 0],
                       [0, 0, 0, 1]])

        RZ = np.array([[np.cos(gamma), -np.sin(gamma), 0, 0],
                       [np.sin(gamma), np.cos(gamma), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

        # Composed rotation matrix with (RX, RY, RZ)
        R = np.dot(np.dot(RX, RY), RZ)

        # Translation matrix
        T = np.array([[1, 0, 0, dx],
                      [0, 1, 0, dy],
                      [0, 0, 1, dz],
                      [0, 0, 0, 1]])

        # Projection 3D -> 2D matrix
        A2 = np.array([[f, 0, w / 2, 0],
                       [0, f, h / 2, 0],
                       [0, 0, 1, 0]])

        # Final transformation matrix
        return np.dot(A2, np.dot(T, np.dot(R, A1)))

    @staticmethod
    def create_zoomed_in_image(image, zoom, posx, posy):

        # ALL IMAGES SHOULD BE THIS SIZE
        height = image.shape[0]
        width = image.shape[1]

        x_offset = int((width - image.shape[1]) / 2) + posx
        y_offset = int((height - image.shape[0]) / 2) + posy

        #  Resize image to zoom amount
        resizedImage = cv2.resize(image, (int(zoom*width), int(zoom*height)), interpolation=cv2.INTER_LINEAR)


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
        img = cv2.resize(image, (int(zoom*width), int(zoom*height)), interpolation=cv2.INTER_AREA)

        # Create black blank image
        blank_image = np.zeros((height, width, 3), np.uint8)

        blank_image[:] = (255, 255, 255)

        try:
            blank_image[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
            return blank_image

        except Exception as e:
            #print(e)
            f = ":("
            return None, [(-1,-1),(-1,-1),(-1,-1),(-1,-1)]
        # cv2.imshow("Blank image", blank_image)
        # cv2.waitKey(0)

    def update(self, image):
        self.image = image

    @staticmethod
    def load_image(img_path, shape=None):
        img = cv2.imread(img_path)
        if shape is not None:
            img = cv2.resize(img, shape)

        return img

    @staticmethod
    def save_image(img_path, img):
        try:
            success = cv2.imwrite(img_path, img)
            if not success:
                print(f"Failed to write image at {img_path}")
        except Exception as e:
            print(f"An error occurred when trying to write image at {img_path}. Error: {str(e)}")


def get_rad(theta, phi, gamma):
    return (deg_to_rad(theta),
            deg_to_rad(phi),
            deg_to_rad(gamma))


def get_deg(rtheta, rphi, rgamma):
    return (rad_to_deg(rtheta),
            rad_to_deg(rphi),
            rad_to_deg(rgamma))


def deg_to_rad(deg):
    return deg * math.pi / 180.0


def rad_to_deg(rad):
    return rad * 180.0 / math.pi
