#!/usr/bin/env python

from distutils.core import setup

setup(name='PyKaka',
      version='0.1',
      description='Python API for Kaka',
      author='Helge Dzierzon',
      author_email='helge.dzierzon@plantandfood.co.nz',
      url='',
      packages=['PyKaka'],
     )


install_requires=[
   'numpy',
   'pql',
   'pymongo',
   'pyyaml',
   'xlrd',
   'pandas',
]


