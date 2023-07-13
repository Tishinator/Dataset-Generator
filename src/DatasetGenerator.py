import os
import sys
import argparse
import cv2
from tqdm import tqdm
from src.image.Image import Image
from src.modifications import utils


def prompt_boolean_input(message):
    return input(message).lower() == "y"


def calculate_number_of_images(rotation_angle, do_rotation_on_x, do_rotation_on_y, do_rotation_on_z):
    rotations = [do_rotation_on_x, do_rotation_on_y, do_rotation_on_z]
    number_of_rotations = sum(rotations)

    # Total number of images
    total_images = number_of_rotations * rotation_angle

    return total_images


def validate_user_confirmation(message):
    if input(message).lower() != "yes":
        sys.exit()


def main():
    # Initialize the ArgumentParser object
    parser = argparse.ArgumentParser(description="Image Transformer")

    # Add an argument for the image path
    parser.add_argument("img_path", help="The path of the image to be transformed")

    # Parse the arguments
    args = parser.parse_args()

    # Input image path
    img_path = args.img_path
    print(f"Image path: {img_path}")

    image = Image(img_path)

    if prompt_boolean_input("Would you like the image rotated? Y/N: "):
        rotation_config = {
            "do_rotation_on_x": prompt_boolean_input("X-axis? Y/N: "),
            "do_rotation_on_y": prompt_boolean_input("Y-axis? Y/N: "),
            "do_rotation_on_z": prompt_boolean_input("Z-axis? Y/N: "),
        }

        # Prompt user for rotation range
        rotation_angle = int(input("Enter the rotation range (default 360): ") or 360)
    else:
        rotation_config = {
            "do_rotation_on_x": False,
            "do_rotation_on_y": False,
            "do_rotation_on_z": False,
        }
        rotation_angle = 0

    # Calculate the number of generated images and required disk space
    num_images = calculate_number_of_images(rotation_angle=rotation_angle, **rotation_config)
    disk_space = num_images * os.path.getsize(img_path)

    # Display the number of images and disk space
    print(f"Number of generated images: {num_images}")
    print(f"Disk space required (GB): {disk_space / (1024 * 1024 * 1024):.2f}")

    validate_user_confirmation("Continue? (yes/no): ")

    # cv2.imshow("image", image.image_data)
    # cv2.waitKey(0)

    dx, dy = int(image.image_data.shape[0] / 10), int(image.image_data.shape[1] / 10)

    output_dirs = ['output', 'output/X', 'output/Y', 'output/Z']
    for dir_name in output_dirs:
        os.makedirs(dir_name, exist_ok=True)

    progress_bar = tqdm(total=num_images, unit="images")

    for angle in range(rotation_angle):
        # Iterate over the axes dynamically based on the configurations
        for axis_name, axis, do_rotation in [('X', [angle, 0, 0], rotation_config["do_rotation_on_x"]),
                                             ('Y', [0, angle, 0], rotation_config["do_rotation_on_y"]),
                                             ('Z', [0, 0, angle], rotation_config["do_rotation_on_z"])]:
            if do_rotation:
                # Rotate the image using the current axis and offset
                rotated_image = image.rotate(axis=axis, position_offset=[dx, dy])

                # Construct the filename based on the axis name and angle
                filename = f'output/{axis_name}/{angle}{axis_name}_{str(angle).zfill(3)}.jpg'

                # Save the rotated image with the constructed filename
                utils.save_image(filename, rotated_image.image_data)

            # Update the progress bar
            progress_bar.update()


    progress_bar.close()


if __name__ == "__main__":
    main()
