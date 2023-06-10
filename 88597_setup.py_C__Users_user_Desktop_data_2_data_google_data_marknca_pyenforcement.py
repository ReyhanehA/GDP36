import os
from setuptools import setup

# pulled right from the python docs at https://pythonhosted.org/an_example_pypi_project/setuptools.html
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'PyEnforcement',
    version = '0.9.0',
    author = 'Mark Nunnikhoven',
    author_email = 'me@markn.ca',
    description = ('PyEnforcement is a python module for accessing the OpenDNS Security Platform API.'),
    license = 'MIT',
    keywords = 'opendns api enforcement security',
    url = 'https://github.com/marknca/pyenforcement',
    packages=['pyenforcement'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)