import numba
import cv2
import numpy as np
import sys # For command line support


def color_to_gray(image_file):
    
    """
    Function that uses a numpy Array and a Python loop with Numba to convert a color image to a grayscaled version

    Args:
        param1 (string): Filename of the image to be converted
    
    Return 
        Numpy array of the grayscaled image
    """
    
    # Read image file. Img is now a numpy array with dimensions (height, width, 3)
    img = cv2.imread(image_file)
    
    # Switch order of RGB-dimension from BGR (as outputted by cv2) to RBG for compatibility
    img = cv2. cvtColor (img , cv2 . COLOR_BGR2RGB)

    print(f"Converting {image_file} to grayscale ...")


    # Calling the Numba function
    img = numba_loop(img)

    # Convert the list to numpy array and return 
    return np.array(img)

@numba.njit
def numba_loop(image_list):
    
    """
    Performs the loop. Numba does not perform well in tandem with cv2, therefore we only decorate the
    time consuming loop with numba
    
    Args:
        param1  list to loop through and convert to grayscale
        
        
    Returns:
        Converted image
    
    """
    for i in range(len(image_list)):
        for j in range(len(image_list[i])):
            # Replace the innermost list representing the RGB values of the pixle with a scalar (sum of the weighted RGB-values)
            # For every pixle multiple by appropriate weight and add (equivalent of taking dot product)
            image_list[i][j] = int(image_list[i][j][0]*0.21 + image_list[i][j][1]*0.72 + image_list[i][j][2]*0.07)
    return image_list
