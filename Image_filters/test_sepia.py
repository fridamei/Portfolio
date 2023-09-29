import pytest
import numpy as np
import cv2
import instapy
from random import randint

def test_sepia():
    """
    Testing of the grayscale-functions from instapy using pytest
    """
    # Random 3D array 
    arr = (np.random.randint(255, size=(25,25, 3))).astype('uint8')
    
    # Array as an image
    cv2.imwrite("testing_image.jpg", arr)

    # save the same image to ensure encoding is the same
    img = cv2.imread("testing_image.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    sepia_matrix = [[0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]]

    # Random pixel for assertions
    row = randint(0,24)
    column = randint(0,24)
    r = img[row, column, 0]
    g = img[row][column][1] 
    b = img[row][column][2]

    img[row, column, 0] = int(r*sepia_matrix[0][0] + g*sepia_matrix[0][1] + b*sepia_matrix[0][2]) if int(r*sepia_matrix[0][0] + g*sepia_matrix[0][1] + b*sepia_matrix[0][2]) < 255 else 255
    
    img[row, column, 1] = int(r*sepia_matrix[1][0]+ g*sepia_matrix[1][1] + b*sepia_matrix[1][2]) if int(r*sepia_matrix[1][0]+ g*sepia_matrix[1][1] + b*sepia_matrix[1][2]) < 255 else 255

    img[row, column, 2] = int(r*sepia_matrix[2][0] + g*sepia_matrix[2][1] + b*sepia_matrix[2][2]) if int(r*sepia_matrix[2][0] + g*sepia_matrix[2][1] + b*sepia_matrix[2][2]) < 255 else 255

    "Testing python implementation"
    arr_python = instapy.grayscale_image("testing_image.jpg", implementation="python")
    python_pixel = arr_python[row, column]
    assert python_pixel.all() == img[row, column].all(), "Pixel from python not matching reference"


    "Testing numpy implementation"
    arr_numpy = instapy.grayscale_image("testing_image.jpg", implementation="numpy")
    numpy_pixel = arr_numpy[row, column]
    assert numpy_pixel.all() == img[row, column].all(), "Pixel from numpy not matching reference"

    "Testing numba implementation"
    arr_numba = instapy.grayscale_image("testing_image.jpg", implementation="numba")
    numba_pixel = arr_numba[row, column]
    assert numba_pixel.all() == img[row, column].all(), "Pixel from numba not matching reference"

    "Testing cython implementation"
    arr_cython = instapy.grayscale_image("testing_image.jpg", implementation="cython")
    cython_pixel = arr_cython[row, column]
    assert cython_pixel.all() == img[row, column].all(), "Pixel from cython not matching reference"


