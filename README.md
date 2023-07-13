# Dataset Generator

## Description
The DatasetGenerator.py script is a Python program designed to apply transformations on an image, specifically rotations. The script prompts the user for input on whether they would like to rotate the image and along which axis (x, y, z). It also allows the user to specify the rotation range (default is 360 degrees). The program provides an estimate of the number of generated images and the required disk space before proceeding with the operation.

## Prerequisites
- Python 3.6 or higher
- OpenCV
- numpy
- tqdm

## How to Use
To use the script, you need to provide the path to the image as an argument when running the script. Here's an example of how to use it:

```shell
python DatasetGenerator.py /path/to/image.jpg
