"""
Created on Mon Jun 26 13:12:10 2023
@author: cai
"""

# Import necessary libraries
import numpy as np
import os
import argparse
import re
import sys

# Set the maximum number of pixels to be loaded by OpenCV
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()

# Import OpenCV library
import cv2

# Function to join images either vertically or horizontally
def join_images(img_name_format, img_order, axis):
    # Read the first image
    img = cv2.imread(img_name_format.format(img_order[0]))
    
    # Iterate through the rest of the images and join them with the first one
    for img_name in img_order[1:]:
        next_img = cv2.imread(img_name_format.format(img_name))
        img = cv2.vconcat([img, next_img]) if axis == 0 else cv2.hconcat([img, next_img])
        
    return img

# Main function
def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser()
    
    # Add argument for image name
    parser.add_argument("img_name", help="The name of the image", nargs='?')
    args = parser.parse_args()

    # Check if an image name is provided
    if args.img_name is None:
        print("Please provide an image name.")
        sys.exit(1)

    # Generate image name format
    img_name_format = re.sub('\.[A-Z]\d\.png$', '.{}.png', args.img_name)
    output_file_name = img_name_format.replace('.{}', '')

    # Define the order of the images to be joined
    img_order_1 = ['A1', 'B1', 'C1', 'D1']
    img_order_2 = ['A2', 'B2', 'C2', 'D2']

    # Join the first set of images horizontally
    img1 = join_images(img_name_format, img_order_1, 1)  
    cv2.imwrite("temp1.png", img1)

    # Join the second set of images horizontally
    img2 = join_images(img_name_format, img_order_2, 1)  
    cv2.imwrite("temp2.png", img2)

    # Join the two sets of images vertically
    final_img = cv2.vconcat([img1, img2])

    # Save the final image
    cv2.imwrite(output_file_name, final_img)

# Run the main function
if __name__ == "__main__":
    main()
