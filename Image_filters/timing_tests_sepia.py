import timeit

"Setup strings"
setup_python="""
import python_color2sepia as pcs
"""

setup_numpy="""
import numpy_color2sepia as ncs
"""

setup_numba="""
import numba_color2sepia as nbcs
"""

setup_cython="""
import cython_color2sepia as ccs
"""


#Printing to file
fp = open("timing_tests_sepia.txt", "w")

fp.write("Timing of the sepia functions using timeit.repeat() with 3 runs:\n")

"Python"
print("Timing the pure python function:\n")
fp = open("timing_tests_sepia.txt", "a")
python_timing = str(timeit.repeat(stmt="pcs.color_to_sepia('rain.jpg')", setup=setup_python, repeat=3, number=1))

python_string = f"\nPure python: {python_timing}"
fp.write(python_string)


"Numpy"
print("\n\nTiming the numpy function:\n")

numpy_timing = str(timeit.repeat(stmt="ncs.color_to_sepia('rain.jpg')", setup=setup_numpy, repeat=3, number=1))
fp = open("timing_tests_sepia.txt", "a")

numpy_string = f"\nNumpy: {numpy_timing}"
fp.write(numpy_string)


"Numba"
print("\n\nTiming the numba function:\n")

numba_timing = str(timeit.repeat(stmt="nbcs.color_to_sepia('rain.jpg')", setup=setup_numba, repeat=3, number=1))

fp = open("timing_tests_sepia.txt", "a")

numba_string = f"\nNumba: {numba_timing}"
fp.write(numba_string)


"Cython"
print("\n\nTiming the cython function:\n")

cython_timing = str(timeit.repeat(stmt="ccs.color_to_sepia('rain.jpg')", setup=setup_cython, repeat=3, number=1))

fp = open("timing_tests_sepia.txt", "a")

cython_string = f"\nCython: {cython_timing}"
fp.write(cython_string)


fp.close()
print("\nTiming file saved as timing_tests_sepia.txt")
