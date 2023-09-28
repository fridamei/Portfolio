## Assignment 4
I ran the code in Anaconda Spyder 4 with python 3.8, tested on VMWare Horizon remote from ifi workspace with python 3. Necessary packages: 
Numpy
timeit
time
cProfile
matplotlib

## Task 4.0

### Functionality
Times the functions of the supplied code test_slow_rectangle.py.
The times from my test runs are recorded in the report.txt files. 

### Usage
Save files in same directory for import of the test_slow_rectangle file to work.
In Spyder it is important to set the source directory to the directory where the files are located. 
Run the code in an IDE or from command line, it prints the results to screen (python3 filename.py)

## Task 4.1
I understood the Numba part of the task to use the pure Python loops.
### Functionality
Converts an image to a grayscale version using different implementations

The time tests are all executed on the supplied rain.jpg file, size 400 x 600 x 3 (H x W x C)

### Missing functionality
Cannot scale image
Requires manual compile of cython file before run

### Usage
For python_color2gray.py, numpy_color2gray.py and numba_color2gray.py:
Takes 1 argument containing the file name (with file type extension, eg .jpg) of the file to be converted.
Run from command line: python3 python_color2gray.py filename.filetype
(might be an other command for invoking the python interpreter depending on python version and terminal, my Anaconda prompt uses simply py)

For cython_color2gray.py:
The file containing the cython code needs to be compiled first. To do so, run the following command:
   python3 setup.py build_ext --inplace

Then run the cython_color2gray.py file from the command line, with the file name argument:
   python3 cython_color2gray.py filename.filetype
   
   (For cython code not using command line arguments the file can also be run without a separate run file by 
   invoking the python interpreter (running the command python3 + return) then >>> import filename (where the cython code is written, without filetype extension))

### Dependencies
OpenCV to process the image
Numpy
Numba 
Cython
Cython code also needs a C-compiler to run. Linux systems (like the IFI-machines) already have them installed, Windows do not.

The necessary packages are described in requirements.txt and is downloaded to a virtual environment\* using the command:
   pip install -r requirements.txt


\* To install a virtual environment called venv-in3110 do the following (as described in the assignment text):
   cd ~
   pip3 install --user virtualenv
   export PATH=$PATH:~/.local/bin
   virtualenv -p python3 venv-in3110

Then activate the environment by writing the command:
   source ~/venv-in3110/bin/activate


## Task 4.2

### Functionality
Converts an image to a sepia version using different implementations
The time tests are all executed on the supplied rain.jpg file, size 400 x 600 x 3 (H x W x C), as in task 4.1

### Missing functionality
Got best results using Numpy, might have overlooked some possibility for improvements in the cython code as 
I suspect a perfecly implemented cython algorithm should be even faster than numpy

### Usage
See Task 4.1, runs the exact same way except the names of the modules is to be changed from \_color2gray to \_color2sepia (eg python3 python_color2sepia.py filename.filetype)

### Dependencies
Dependencies as stated in task 4.1. All are found in the requirements.txt file. 


## Task 4.3

### Functionality
Package with the grayscale and sepia filters from earlier tasks.
Cython code is compiled from setup file and thus does not need manual compiling before running. 
Tests that assert all the implementations of both the grayscale and sepia functions, to check
that they return the expected value for a randomly generated pixel in a randomly generated image

### Usage
To run the filter functions from packages from terminal:
   cd to package location (~/Task_4.3/instapy) and enter pip3 install . + return in terminal
   Run python interpreter ($ python3)
   $ import instapy
   $ instapy.grayscale_image(input_name, output_name=None, implementation="numpy") (or instapy.sepia_image (...))
   
To run tests:
   pytest test_grayscale.py
   pytest test_sepia.py

### Dependencies
All of the above and pytest, which should also be in the requirements.txt file.
(if not: pip install -U pytest)


## Task 4.4

### Functionality
Command line interface for the package created in task 4.3
Takes arguments:
-h --help  for documentation
-f --file Input filename
-se --sepia choosing the sepia filter
-g --gray choosing the grayscale filter
-sc --scale scaling factor for resizing the image before conversion
-i --implement which implementation to use. numpy is default is none is chosen
-o --out where to save the output file, else the function will simply return an array without saving

## Missing functionality
Does not give errors if neither g or se is given. Tries to run the function regardless if the
necessary arguments are given or not. If rescaled then the scaled image is saved inplace overwriting the 
original file. 
Does not check if given file name actually exists before trying to run the functions

### Usage
To run the CLI:
   install the package as stated above if not done (navigate to ~/instapy file where the setup file is located)
   pip3 install .
   Run the CLI from any directory by entering instapy arg1 arg2 ...
  
