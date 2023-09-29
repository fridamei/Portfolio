import cv2
import numpy as np
import sys
import numba

def color_to_sepia(image_file):
    
    """
    Function that uses a numpy Array and a Python loop with Numba to convert a color image to a sepia version
        
    Args:
        param1 (string): Filename of the image to be converted
    
    Return 
        Numpy array of the sepia image
    """
    # Read image file. Img is now a numpy array with dimensions (height, width, 3)
    img = cv2.imread(image_file)
    
    # Switch order of RGB-dimension from BGR (as outputted by cv2) to RBG for compatibility
    img = cv2.cvtColor (img, cv2.COLOR_BGR2RGB)
    
    sepia_matrix = np.array([[0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]])

    # Loop through the rows and columns (height and width) of the image
    print(f"Converting {image_file} to sepia ...")


    img_sepia = numba_loop(img, sepia_matrix)
    
    # Convert list to array, revert back to RGB-order and return
    return cv2.cvtColor(np.array(img_sepia), cv2.COLOR_BGR2RGB)

#Numba loop
@numba.njit
def numba_loop(image_list, filter_matrix):
    
    """
    Performs the loop. Numba does not perform well in tandem with cv2, therefore we only decorate the
    time consuming loop with numba
    
    Args:
        param1: numpy array to loop through and convert sepia
        param2: numpy array containing the matrix to use as image filter
        
    Returns:
        Converted image as numpy array
    
    """
    
    for i in range(len(image_list)):
        for j in range(len(image_list[i])):
            # Save the pixels before scaling
            r = image_list[i][j][0]
            g = image_list[i][j][1] 
            b = image_list[i][j][2]
    
           # Convert the red pixels:
            # (r*0.393 + g*0.769 + b*0.189)
            image_list[i][j][0] = int(r*filter_matrix[0][0] + g*filter_matrix[0][1] + b*filter_matrix[0][2]) if int(r*filter_matrix[0][0] + g*filter_matrix[0][1] + b*filter_matrix[0][2]) < 255 else 255
            
            # Convert the green pixels:
            #(r*0.349 + g*0.686 + b*0.168) 
            image_list[i][j][1] = int(r*filter_matrix[1][0]+ g*filter_matrix[1][1] + b*filter_matrix[1][2]) if int(r*filter_matrix[1][0]+ g*filter_matrix[1][1] + b*filter_matrix[1][2]) < 255 else 255
            
            # Convert the blue pixels:
            #(r*0.272 + g*0.534 + b*0.131)
            image_list[i][j][2] = int(r*filter_matrix[2][0] + g*filter_matrix[2][1] + b*filter_matrix[2][2]) if int(r*filter_matrix[2][0] + g*filter_matrix[2][1] + b*filter_matrix[2][2]) < 255 else 25

    return image_list

if __name__ == "__main__":
    color_to_sepia(sys.argv[1])
