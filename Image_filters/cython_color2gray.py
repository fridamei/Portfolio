import sys
import cython_grayscale_code

"""
File that runs the compiled Cython code. 

Takes command line argument with file name

"""

if __name__ == "__main__":
    cython_grayscale_code.color_to_gray(sys.argv[1])