# https://docs.python.org/3/distutils/apiref.html
from distutils.core import setup
from distutils.extension import Extension

polyhedron = Extension(
    'polyhedron',
    sources=['polyhedron.cpp', 'johnson.cpp'],
    libraries=['boost_python37-mt', 'boost_numpy37-mt'],
    extra_compile_args=['-std=c++17']  # lambda support required
)

setup(
    name='polyhedron',
    version='0.1',
    ext_modules=[polyhedron])

# call with: python3.7 setup.py build_ext --inplace
