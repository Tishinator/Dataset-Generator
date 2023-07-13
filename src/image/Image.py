import cv2
from src.modifications import rotate, zoom


class Image:
    def __init__(self, img_path):
        self.path = img_path
        if self.path:
            self.image_data = cv2.imread(img_path)
            self.height = self.image_data.shape[0]
            self.width = self.image_data.shape[1]
            self.num_channels = self.image_data.shape[2]
            self.shape = [self.image_data.shape[0], self.image_data.shape[1]]
        else:
            self.image_data = None
            self.height = 0
            self.width = 0
            self.num_channels = 0
            self.shape = []

    @classmethod
    def from_image_data(cls, image_data):
        obj = cls("")
        obj.path = None
        obj.image_data = image_data
        obj.height = image_data.shape[0]
        obj.width = image_data.shape[1]
        obj.num_channels = image_data.shape[2]
        obj.shape = [image_data.shape[0], image_data.shape[1]]
        return obj

    # returns an rotated image.
    def rotate(self, axis=(0, 0, 0), position_offset=(0, 0)):
        return self.from_image_data(rotate.rotate_along_axis(self,
                                                             axis[0], axis[1], axis[2],
                                                             position_offset[0], position_offset[1]))

    def zoom(self, zoom_level, position_offset=(0, 0)):
        ret_image = None
        if zoom_level < 1.0:
            ret_image = zoom.create_zoomed_out_image(self, zoom_level,
                                                     position_offset[0], position_offset[1])
        elif zoom_level > 1.0:
            ret_image = zoom.create_zoomed_in_image(self, zoom_level,
                                                    position_offset[0], position_offset[1])

        return self.from_image_data(ret_image)
