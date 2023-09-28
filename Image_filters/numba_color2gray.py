import numba
import cv2
import numpy as np
import sys # For command line support


def color_to_gray(image_file):
    
    """
    Function that uses pure Python and Numba (except using Numpy Array to save the image) to convert a color image to a grayscaled version
    Saves the grayscaled image locally
    
    Args:
        param1 (string): Filename of the image to be converted
    
    """
    
    # Read image file. Img is now a numpy array with dimensions (height, width, 3)
    img = cv2.imread(image_file)
    
    # Switch order of RGB-dimension from BGR (as outputted by cv2) to RBG for compatibility
    img = cv2. cvtColor (img , cv2 . COLOR_BGR2RGB)
    
    print(f"Converting {image_file} to grayscale ...")
    
    # Calling the Numba function
    img = numba_loop(img)

    # Convert the list to numpy array to be able to call imwrite and save the file
    img_grayscale = np.array(img)

    # Perform rsplit (specified to split only ones) to strip the file name of the file type extension
    name_without_filetype =  image_file.rsplit(".", 1)[0]
    
    # Name of the grayscaled image
    new_file_name = f"{name_without_filetype}_grayscale.jpeg"
    
    # Save the image
    cv2.imwrite(new_file_name, img_grayscale)
    
    print(f"Saved image as {new_file_name}")
    
    

@numba.jit 
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


if __name__ == "__main__":
    color_to_gray(sys.argv[1])
