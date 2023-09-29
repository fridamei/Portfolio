import cv2
import numpy as np
import cython
cimport numpy as np

cpdef color_to_sepia(image_file):
    
    """
    Function that uses Cython (numpy array passed to a Cython function for traversing) to convert a color image to a sepia version
    Saves the sepia image locally
    
    Args:
        param1 (string): Filename of the image to be converted
    
    """
    
    # Read image file. Img is now a numpy array with dimensions (height, width, 3)
    img = cv2.imread(image_file)
    
    # Switch order of RGB-dimension from BGR (as outputted by cv2) to RBG for compatibility
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    sepia_matrix = np.array([[0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]])
    
    
    print(f"Converting {image_file} to sepia ...")
    
    # Calling the Cython function
    cdef np.ndarray[np.uint8_t, ndim=3] img_sepia
    img_sepia = cython_loop(img, sepia_matrix)

    # Convert list to array and revert back to RGB-order
    img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_BGR2RGB)

    # Perform rsplit (specified to split only ones) to strip the file name of the file type extension
    name_without_filetype =  image_file.rsplit(".", 1)[0]
    
    # Name of the sepia image
    new_file_name = f"{name_without_filetype}_sepia.jpeg"
    
    # Save the image
    cv2.imwrite(new_file_name, img_sepia)
    
    print(f"Saved image as {new_file_name}")


# Cython loop with typed arguments
cdef np.ndarray[np.uint8_t, ndim=3] cython_loop(np.ndarray[np.uint8_t, ndim=3] image_list, np.ndarray[double, ndim=2] filter_matrix):
    """
    Performs the loop using Cython
    
    Args:
        param1  numpy array to loop through and convert to sepia
        param2  numpy array to use as filter
        
    Returns:
        Numpy array containig sepia image
    
    """
    cdef int i, j, rows, columns
    rows = len(image_list)
    columns = len(image_list[0])
    
    for i in range(rows):
        for j in range(columns):
            # Save the pixels before scaling
            # As each entry to the image_list is typed in the argument section, the types of r,g,b is implied
            r = image_list[i, j, 0]
            g = image_list[i, j, 1] 
            b = image_list[i, j, 2]
    
           # Convert the red pixels:
            # (r*0.393 + g*0.769 + b*0.189)
            image_list[i, j, 0] = int(r*filter_matrix[0, 0] + g*filter_matrix[0, 1] + b*filter_matrix[0, 2]) if int(r*filter_matrix[0, 0] + g*filter_matrix[0, 1] + b*filter_matrix[0,2]) < 255 else 255
            
            # Convert the green pixels:
            #(r*0.349 + g*0.686 + b*0.168) 
            image_list[i, j, 1] = int(r*filter_matrix[1, 0]+ g*filter_matrix[1,1] + b*filter_matrix[1, 2]) if int(r*filter_matrix[1, 0]+ g*filter_matrix[1, 1] + b*filter_matrix[1, 2]) < 255 else 255
            
            # Convert the blue pixels:
            #(r*0.272 + g*0.534 + b*0.131)
            image_list[i, j,2] = int(r*filter_matrix[2,0] + g*filter_matrix[2,1] + b*filter_matrix[2, 2]) if int(r*filter_matrix[2, 0] + g*filter_matrix[2][1] + b*filter_matrix[2, 2]) < 255 else 255

    return image_list
