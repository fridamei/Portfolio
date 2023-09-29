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

    sepia_matrix = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
    

    print(f"Converting {image_file} to sepia ...")
    
    # Matrix multiplication so that
    # sepia_red = (r*0.393 + g*0.769 + b*0.189)
    # sepia_green = (r*0.349 + g*0.686 + b*0.168)
    # sepia_blue = (r*0.272 + g*0.534 + b*0.131)
    img_sepia = np.matmul(img[...,:3], sepia_matrix.T) # Gir den rød, overeksponerte hunden
    
    # Set pixel values greater than 255 to 255
    img_sepia[img_sepia > 255] = 255

    # convert floating point numbers back to integers to ensure compatibility and revert back to RGB
    return cv2.cvtColor(img_sepia.astype("uint8"), cv2.COLOR_BGR2RGB)