import cv2
import numpy as np
import sys

def color_to_sepia(image_file):
    
    """
    Function that uses pure Python (except using Numpy Array to save the image) to convert a color image to a sepia version

    Args:
        param1 (string): Filename of the image to be converted
        
    Return
        Numpy array of the grayscaled image
    """
    # Read image file. Img is now a numpy array with dimensions (height, width, 3)
    img = cv2.imread(image_file)
    
    # Switch order of RGB-dimension from BGR (as outputted by cv2) to RBG for compatibility
    img = cv2.cvtColor (img, cv2.COLOR_BGR2RGB)

    # Convert img to a python list for pure python computations    
    img = list(img)
    
    sepia_matrix = [[0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]]

    # Loop through the rows and columns (height and width) of the image
    print(f"Converting {image_file} to sepia ...")

    for i in range(len(img)):
        for j in range(len(img[i])):
            # Save the pixels before scaling
            r = img[i][j][0]
            g = img[i][j][1] 
            b = img[i][j][2]

            # Convert the red pixels:
            # (r*0.393 + g*0.769 + b*0.189)
            img[i][j][0] = int(r*sepia_matrix[0][0] + g*sepia_matrix[0][1] + b*sepia_matrix[0][2]) if int(r*sepia_matrix[0][0] + g*sepia_matrix[0][1] + b*sepia_matrix[0][2]) < 255 else 255
            
            # Convert the green pixels:
            #(r*0.349 + g*0.686 + b*0.168) 
            img[i][j][1] = int(r*sepia_matrix[1][0]+ g*sepia_matrix[1][1] + b*sepia_matrix[1][2]) if int(r*sepia_matrix[1][0]+ g*sepia_matrix[1][1] + b*sepia_matrix[1][2]) < 255 else 255
            
            # Convert the blue pixels:
            #(r*0.272 + g*0.534 + b*0.131)
            img[i][j][2] = int(r*sepia_matrix[2][0] + g*sepia_matrix[2][1] + b*sepia_matrix[2][2]) if int(r*sepia_matrix[2][0] + g*sepia_matrix[2][1] + b*sepia_matrix[2][2]) < 255 else 255


    # Convert list to array and revert back to RGB-order
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
