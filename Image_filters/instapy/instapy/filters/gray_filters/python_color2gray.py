import cv2
import numpy as np
import sys

def color_to_gray(image_file):
    
    """
    Function that uses pure Python (except using Numpy Array to save the image) to convert a color image to a grayscaled version

    Args:
        param1 (string): Filename of the image to be converted
    
    Return
        Numpy array of the grayscaled image
       
    """
    
    # Read image file. Img is now a numpy array with dimensions (height, width, 3)
    img = cv2.imread(image_file)
    
    # Switch order of RGB-dimension from BGR (as outputted by cv2) to RBG for compatibility
    img = cv2.cvtColor (img, cv2.COLOR_BGR2RGB)

    # Convert img to a python list for computations    
    img = list(img)
    
    # Loop through the rows and columns (height and width) of the image
    
    print(f"Converting {image_file} to grayscale ...")
    for i in range(len(img)):
        for j in range(len(img[i])):
            # Replace the innermost list representing the RGB values of the pixle with a scalar (sum of the weighted RGB-values)
            # For every pixle multiple by appropriate weight and add (equivalent of taking dot product)
            img[i][j] = int(img[i][j][0]*0.21 + img[i][j][1]*0.72 + img[i][j][2]*0.07)
    
    # Convert the list to numpy array to be able to call imwrite and save the file
    return np.array(img)

