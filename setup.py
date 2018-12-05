from setuptools import setup, find_packages
import sys
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = True
except ImportError:
    bdist_wheel = None

version = '0.9.1'

setup(name='djenga',
      version=version,
      description="Useful building blocks for Django.",
      long_description="""\
Useful building blocks for Django.""",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Framework :: Django',
          'Framework :: Django :: 1.11',
          'Framework :: Django :: 1.10',
          'Framework :: Django :: 1.9',
          'License :: OSI Approved :: BSD License',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      cmdclass={'bdist_wheel': bdist_wheel},
      keywords='django python',
      author='Preetam Shingavi',
      author_email='p.shingavi@yahoo.com',
      url='https://github.com/2ps/djenga',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'six>=1.10.0',
          'Django>=1.9',
          'cssutils>=1.0',
          'beautifulsoup4>=4.3.2',
          'pynliner>=0.8.0',
          'pycryptodome>=3.6.6',
          'pytz',
          'python-dateutil',
          'pyyaml',
          'django-redis-cache',
          'celery>=4.1.0',
          'boto3',
          'requests>=2.19',
      ] + ([ 'psutil' ] if 'cygwin' in sys.platform else []),
      entry_points={
          'console_scripts': [
              'kms_wrap=djenga.encryption.kms_wrap:main',
          ],
      })
