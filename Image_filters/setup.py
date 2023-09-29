from distutils.core import setup
from Cython.Build import cythonize
import numpy

"""
File to compile the cython (.pyx) file(s)

"""

setup(name='Cython modules', 
      ext_modules=cythonize('*.pyx'), 
      include_dirs=[numpy.get_include()])

