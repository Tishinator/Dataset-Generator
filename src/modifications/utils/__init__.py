import math
import cv2


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


def load_image(img_path, shape=None):
    img = cv2.imread(img_path)
    if shape is not None:
        img = cv2.resize(img, shape)

    return img


def save_image(img_path, img):
    try:
        success = cv2.imwrite(img_path, img)
        if not success:
            print(f"Failed to write image at {img_path}")
    except Exception as e:
        print(f"An error occurred when trying to write image at {img_path}. Error: {str(e)}")