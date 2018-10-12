__author__ = 'gidobot'
import numpy as np
import PIL.Image
import argparse
import glob
import os
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser(description='Options for Bayer pattern png image analyzer')
    parser.add_argument('--input_folder', required=True, type=str, help='path to folder containing png images to anaylze')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
	args = parse_args()
	for file in glob.glob(os.path.join(args.input_folder, "*.png")):
		image = PIL.Image.open(file)
		pixel = np.array(image)
		mean_pixel = np.mean(pixel)*(2**4)
		print("Mean bayer pixel value for {}: {}".format(file, mean_pixel))