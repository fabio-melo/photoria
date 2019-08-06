from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

setup(
  name = 'Meu Programa',
  ext_modules = [
    Extension('ops',
              sources=['ops.pyx'],
              extra_compile_args=['-g0'])
    ],
    cmdclass = {'build_ext': build_ext},
    include_dirs=[numpy.get_include()]
)