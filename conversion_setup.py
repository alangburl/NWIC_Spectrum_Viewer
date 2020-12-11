from distutils.core import setup
from Cython.Build import cythonize
import setuptools
setup(ext_modules=cythonize("Conversion.pyx", build_dir="build"),
                                           script_args=['build'], 
                                           options={'build':{'build_lib':'.'}}