#!/usr/bin/python
"""
Run 
python setup.py build
to build this packages
setup.py
This Just Template Not Complete Setup.py
"""
import sys
from distutils.core import setup
setup(
    name='sharefs',
    version='1.0',
    description='Treat Social sites As a file system',
    author='Sanket Sudake, Sagar Rakshe',
    author_email='sanketsudake@gmail.com',
    license='GPLv3',
    py_modules = ['internet', 'main', 'notify','slog',
                'socialfs', 'social','stest','choose'],
    scripts = ['socialrun.sh'],
    )
#
# Final User will just run socialrun command to use application
# See socialrun.sh for more
# To be added
#
#url =
#packages =
