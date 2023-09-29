import cv2
import numpy as np

import instapy.filters.gray_filters.python_color2gray as pcg
import instapy.filters.sepia_filters.python_color2sepia as pcs

import instapy.filters.gray_filters.numpy_color2gray as ncg
import instapy.filters.sepia_filters.numpy_color2sepia as ncs

import instapy.filters.gray_filters.numba_color2gray as nbcg
import instapy.filters.sepia_filters.numba_color2sepia as nbcs

import cython_color2gray as ccg
import cython_color2sepia as ccs

def grayscale_image(input_filename, output_filename=None, implementation='numpy'):
    """
    Function that takes in an image file and converts it to a grayscaled version
    Uses Numpy by default as it is fast and all functions demand Numpy support either way
    Args
        param1   The image file to be converted to grayscale
        param2   Saves a copy of the grayscaled image as the name supplied
        param3   Which implementation to use (python/numpy/numba/cython)
        
    Return
        Numpy Array representation of the image
    
    """
    # In case implementation is not specified as command line argument 
    if implementation == None:
        implementation="numpy"

    # Dictionary that links implementation with correct function
    implementations = {"python" : pcg.color_to_gray, "numpy" : ncg.color_to_gray, "numba" : nbcg.color_to_gray, "cython" : ccg.color_to_gray}
    
    "Runs the appropriate function based on argument (eg if python is specified, the pcg.color_to_gray() function is run)"
    image_gray = implementations[implementation](input_filename)
    
    # Save the image if output filename is supplied
    if output_filename != None:
        cv2.imwrite(output_filename, image_gray) 
    
    return image_gray


def sepia_image(input_filename, output_filename=None, implementation='python'):
    """
    Function that takes in an image file and converts it to a grayscaled version
    
    Args
        param1   The image file to be converted to sepia
        param2   Saves a copy of the sepia image as the name supplied
        param3   Which implementation to use (python/numpy/numba/cython)
        
    Return
        Numpy Array representation of the image
    
    """
    if implementation == None:
        implementation="numpy"

    implementations = {"python" : pcs.color_to_sepia, "numpy" : ncs.color_to_sepia, "numba" : nbcs.color_to_sepia, "cython" : ccs.color_to_sepia}
    
    image_sepia = implementations[implementation](input_filename)
    
    # Save the image if output filename is supplied
    if output_filename != None:
        cv2.imwrite(output_filename, image_sepia) 
    
    return image_sepia
