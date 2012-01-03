#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Setuptools setup file for `python_toolbox`.'''

import os
import setuptools
import sys


def get_python_toolbox_packages():
    '''
    Get all the packages in `python_toolbox`.
    
    Returns something like:
    
        ['python_toolbox', 'python_toolbox.caching',
        'python_toolbox.nifty_collections', ... ]
        
    '''
    return ['python_toolbox.' + p for p in
            setuptools.find_packages('./python_toolbox')] + \
           ['python_toolbox']


def get_test_python_toolbox_packages():
    '''
    Get all the packages in `test_python_toolbox`.
    
    Returns something like:
    
        ['test_python_toolbox', 'test_python_toolbox.test_caching',
        'test_python_toolbox.test_nifty_collections', ... ]
        
    '''
    return ['test_python_toolbox.' + p for p in
            setuptools.find_packages('./test_python_toolbox')] + \
           ['test_python_toolbox']


def get_packages():
    '''
    Get all the packages in `python_toolbox` and `test_python_toolbox`.
    
    Returns something like:
    
        ['test_python_toolbox', 'python_toolbox', 'python_toolbox.caching',
        'test_python_toolbox.test_nifty_collections', ... ]
        
    '''
    return get_python_toolbox_packages() + get_test_python_toolbox_packages()


my_long_description = \
'''\

The Python Toolbox is a collection of Python tools for various tasks. It
contains:

 - `python_toolbox.caching`: Tools for caching functions, class instances and
    properties.
 
 - `python_toolbox.cute_iter_tools`: Tools for manipulating iterables. Adds
    useful functions not found in Python's built-in `itertools`.
 
 - `python_toolbox.context_managers`: Pimping up your context managers.
 
 - `python_toolbox.emitters`: A publisher-subscriber framework that doesn't
    abuse strings.
   
 - And many, *many* more! The Python Toolbox contains **hundreds** of useful
   little tools.

Visit http://pythontoolbox.org for more info.

Documentation is at http://docs.pythontoolbox.org .
'''

my_classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    ('License :: OSI Approved :: GNU Library or Lesser General '
     'Public License (LGPL)'),
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering',
]


setuptools.setup(
    name='python_toolbox',
    version='0.1',
    requires=['distribute'],
    test_suite='nose.collector',
    install_requires=['distribute'],
    tests_require=['nose>=1.0.0',
                   'docutils>=0.8'],
    description='A collection of Python tools for various tasks',
    author='Ram Rachum',
    author_email='ram@rachum.com',
    url='http://python_toolbox.org',
    packages=get_packages(),
    scripts=['test_python_toolbox/scripts/_test_python_toolbox.py'],
    license='LGPL v2.1',
    long_description=my_long_description,
    classifiers=my_classifiers,
    include_package_data=True,
    zip_safe=False,
)

