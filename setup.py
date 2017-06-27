from setuptools import setup, find_packages
import sys

version = '0.4.1'

setup(name='djenga',
      version=version,
      description="Useful building blocks for Django.",
      long_description="""\
Useful building blocks for Django.""",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Framework :: Django',
          'Framework :: Django :: 1.11',
          'Framework :: Django :: 1.10',
          'Framework :: Django :: 1.9',
          'License :: OSI Approved :: BSD License',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django python',
      author='Preetam Shingavi',
      author_email='p.shingavi@yahoo.com',
      url='https://github.com/2ps/djenga',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'Django>=1.9',
          'cssutils==1.0',
          'beautifulsoup4==4.3.2',
          'pycrypto>=2.6.1',
          'pytz',
          'python-dateutil',
          'pyyaml',
      ] + ([ 'psutil' ] if 'cygwin' in sys.platform else []),
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
