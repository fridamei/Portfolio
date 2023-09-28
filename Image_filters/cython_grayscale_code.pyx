import cv2
import numpy as np
import sys # For command line support
cimport numpy as np

def color_to_gray(image_file):
    
    """
    Function that uses Cython (numpy array passed to a Cython function for traversing, then using Numpy Array to save the image) to convert a color image to a grayscaled version
    Saves the grayscaled image locally
    
    Args:
        param1 (string): Filename of the image to be converted
    
    """
    
    # Read image file. Img is now a numpy array with dimensions (height, width, 3)
    img = cv2.imread(image_file)
    
    # Switch order of RGB-dimension from BGR (as outputted by cv2) to RBG for compatibility
    img = cv2. cvtColor (img , cv2 . COLOR_BGR2RGB)

    # Convert img to a python list for computations    
    #img = list(img)
    
    print(f"Converting {image_file} to grayscale ...")
    
    # Calling the Cython function
    img_grayscale = cython_loop(img)

    # Convert the list to numpy array to be able to call imwrite and save the file
    #img_grayscale = np.array(img)

    # Perform rsplit (specified to split only ones) to strip the file name of the file type extension
    name_without_filetype =  image_file.rsplit(".", 1)[0]
    
    # Name of the grayscaled image
    new_file_name = f"{name_without_filetype}_grayscale.jpeg"
    
    # Save the image
    cv2.imwrite(new_file_name, img_grayscale)
    
    print(f"Saved image as {new_file_name}")

# Cython loop with typed arguments
cdef cython_loop(np.ndarray[np.uint8_t, ndim=3] img):
    
    """
    Performs the loop using Cython
    
    Args:
        param1  list to loop through and convert to grayscale
        
        
    Returns:
        Grayscaled image
    
    """
    # Define variables as C-types
    cdef int rows = len(img)
    cdef int columns = len(img[0])
    
    cdef int i, j = 0
    for i in range(rows):
        for j in range(columns):
            # Replace the innermost list representing the RGB values of the pixle with a scalar (sum of the weighted RGB-values)
            # For every pixle multiple by appropriate weight and add (equivalent of taking dot product)
            img[i][j] = int(img[i][j][0]*0.21 + img[i][j][1]*0.72 + img[i][j][2]*0.07)
    
    return img