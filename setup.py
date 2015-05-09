from setuptools import setup, find_packages
import sys, os

version = '0.0.5'

setup(name='djenga',
      version=version,
      description="Useful building blocks for Django.",
      long_description="""\
Useful building blocks for Django.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django python',
      author='Preetam Shingavi',
      author_email='p.shingavi@yahoo.com',
      url='https://github.com/2ps/djenga',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'Django==1.7.3',
          'cssutils==1.0',
          'beautifulsoup4==4.3.2',
          'pycrypto==2.6.1',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
