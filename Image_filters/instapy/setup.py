from distutils.core import setup
import setuptools
from setuptools.extension import Extension
from Cython.Build import cythonize 
import numpy as np

"For compiling the cython files"
extensions=[
    Extension("cython_color2gray", ["instapy/filters/gray_filters/cython_color2gray.pyx"],
    include_dirs=[np.get_include()],),
    Extension("cython_color2sepia", ["instapy/filters/sepia_filters/cython_color2sepia.pyx"],
    include_dirs=[np.get_include()])
]

# Setup specifications
setuptools.setup(
    name="instapy",
    version="1.0",
    author="fridamei",
    author_email="fridamei@uio.no",
    description="Instagram filters for Python",    
url="https://github.uio.no/IN3110/IN3110-fridamei/"
    packages=setuptools.find_packages(),
    scripts=["bin/instapy"],
    ext_modules=cythonize(extensions),
    setup_requires=["cython", "numpy", "setuptools"],
    install_requires=["numpy", "numba", "opencv-python", "pytest"]
    )
