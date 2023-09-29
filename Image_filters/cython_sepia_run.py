import sys
import cython_color2sepia

"""
File that runs the compiled Cython code. 

Takes command line argument with file name

"""

if __name__ == "__main__":
    cython_color2sepia.color_to_sepia(sys.argv[1])
