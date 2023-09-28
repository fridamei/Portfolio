import timeit

#setup_python="""
#import python_color2gray as pcg

#"""
#print(timeit.repeat(stmt="pcg.color_to_gray('rain.jpg')", setup=setup_python, repeat=3, number=1))


setup_numpy="""
import numpy_color2gray as ncg
"""
print(timeit.repeat(stmt="ncg.color_to_gray('rain.jpg')", setup=setup_numpy, repeat=3, number=1))


setup_numba="""
import numba_color2gray as nbcg
"""
print(timeit.repeat(stmt="nbcg.color_to_gray('rain.jpg')", setup=setup_numba, repeat=3, number=1))


setup_cython="""
import cython_grayscale_code as ccg
"""
print(timeit.repeat(stmt="ccg.color_to_gray('rain.jpg')", setup=setup_cython, repeat=3, number=1))
