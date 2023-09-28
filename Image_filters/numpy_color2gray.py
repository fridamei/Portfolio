import numpy as np
import cv2
import sys

def color_to_gray(image_file):
    
    """
    Function that uses Numpy to convert a color image to a grayscaled version
    Saves the grayscaled image locally
    
    Args:
        param1 (string): Filename of the image to be converted
    
    """
    
    # Read image file. Img is now a numpy array with dimensions (height, width, 3)
    img = cv2.imread(image_file)
    
    # Switch order of RGB-dimension from BGR (as outputted by cv2) to RBG for compatibility
    img = cv2. cvtColor (img , cv2 . COLOR_BGR2RGB)
    
    # Weights to apply the RGB layers respectively to convert to grayscale
    weights = [0.21, 0.72, 0.07]
    
    # img[...,:3] returns all three of the RGB values of all the pixels, so that each pixels RGB values are multiplied (dot-product) with the appropriate channel weight
    # Ie. ensures every RGB value of every pixel is multiplied by the appropriate weight
    print(f"Converting {image_file} to grayscale ...")
    img_grayscale = np.dot(img[...,:3], weights)
    
    # convert floating point numbers back to integers to ensure compatibility
    img_grayscale = img_grayscale.astype("uint8")

    # Perform rsplit (specified to split only ones) to strip the file name of the file type extension
    name_without_filetype =  image_file.rsplit(".", 1)[0]
    
    # Name of the grayscaled image
    new_file_name = f"{name_without_filetype}_grayscale.jpeg"
    
    # Save the image
    cv2.imwrite(new_file_name, img_grayscale)
    
    print(f"Saved image as {new_file_name}")
    
if __name__ == "__main__":
    color_to_gray(sys.argv[1])

