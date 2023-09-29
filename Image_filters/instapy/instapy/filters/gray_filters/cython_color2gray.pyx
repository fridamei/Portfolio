import cv2
import numpy as np
import cython
cimport numpy as np

cpdef color_to_gray(image_file):
    
    """
    Function that uses Cython (numpy array passed to a Cython function for traversing, then using Numpy Array to save the image) to convert a color image to a grayscaled version
    
    Args:
        param1 (string): Filename of the image to be converted
    
    Return 
        Numpy array of grayscaled image
    """
    
    # Read image file. Img is now a numpy array with dimensions (height, width, 3)
    img = cv2.imread(image_file)
    
    # Switch order of RGB-dimension from BGR (as outputted by cv2) to RBG for compatibility
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    print(f"Converting {image_file} to grayscale ...")
    
    # Calling the Cython function
    cdef np.ndarray[np.uint8_t, ndim=3] img_grayscale

    img_grayscale = cython_loop(img)

    return img_grayscale

# Cython loop with typed arguments
cdef np.ndarray[np.uint8_t, ndim=3] cython_loop(np.ndarray[np.uint8_t, ndim=3] img):  
    """
    Performs the loop using Cython
    
    Args:
        param1  list to loop through and convert to grayscale
        
        
    Returns:
        Grayscaled image
    
    """
    # Define variables as C-types
    cdef int i, j, rows, columns
    rows = len(img)
    columns = len(img[0])
    for i in range(rows):
        for j in range(columns):
            # Replace the innermost list representing the RGB values of the pixle with a scalar (sum of the weighted RGB-values)
            # For every pixle multiple by appropriate weight and add (equivalent of taking dot product)
            img[i, j] = int(img[i, j, 0]*0.21 + img[i, j, 1]*0.72 + img[i, j, 2]*0.07)

    return img
