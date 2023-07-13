import cv2
from src.image.Image import Image
import unittest


class ImageModificationTest(unittest.TestCase):
    def setUp(self):
        # Set up any necessary objects or variables
        self.img_path = r"C:\Users\miket\Pictures\Leftovers.png"

    def tearDown(self):
        # Clean up after each test
        pass

    def test_Image_Class(self):
        apple = Image(self.img_path)
        dx, dy = int(apple.image_data.shape[0] / 10), int(apple.image_data.shape[1] / 10)
        # dx, dy = 0, 0
        cv2.imshow("image", apple.image_data)
        cv2.waitKey(0)

        # try a modification
        newImg = apple.rotate([45, 45, 0], [dx, dy])
        cv2.imshow("image", newImg.image_data)
        # cv2.waitKey(0)
        newImg2 = apple.rotate([45, 45, 0])
        cv2.imshow("image2", newImg2.image_data)
        cv2.waitKey(0)

        # zoom
        newImg3 = apple.zoom(zoom_level=0.5)
        cv2.imshow("image3", newImg3.image_data)
        cv2.waitKey(0)

if __name__ == '__main__':
    unittest.main()