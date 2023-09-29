import cv2
import numpy as np
import sys

def color_to_sepia(image_file):
    
    """
    Function that uses pure Python (except using Numpy Array to save the image) to convert a color image to a sepia version
    Saves the sepia image locally
    
    Args:
        param1 (string): Filename of the image to be converted
    
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
    
    #img_sepia = np.matmul(img[...,:3], sepia_matrix.T)
    img_sepia = np.dot(img, sepia_matrix.T) # Tror denne fungerer like godt
    
    # Set pixel values greater than 255 to 255
    img_sepia[img_sepia > 255] = 255

    # convert floating point numbers back to integers to ensure compatibility and revert back to RGB
    img_sepia = cv2.cvtColor(img_sepia.astype("uint8"), cv2.COLOR_BGR2RGB)

    # Perform rsplit (specified to split only ones) to strip the file name of the file type extension
    name_without_filetype =  image_file.rsplit(".", 1)[0]
    
    # Name of the grayscaled image
    new_file_name = f"{name_without_filetype}_sepia.jpeg"
    
    # Save the image
    cv2.imwrite(new_file_name, img_sepia)

    """
    #For printing in editor
    cv2.imshow("Sepia",img_sepia)
    cv2.waitKey(0)
    """

    print(f"Saved image as {new_file_name}")

if __name__ == "__main__":
    color_to_sepia(sys.argv[1])
    