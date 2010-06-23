from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='apvy',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Zeomega',
      author_email='jbaker@zeomega.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'txamqp',
      ],
      entry_points={
          'console_scripts' : ['apvyd = apvy.apvyd:main'],
      }
      )
