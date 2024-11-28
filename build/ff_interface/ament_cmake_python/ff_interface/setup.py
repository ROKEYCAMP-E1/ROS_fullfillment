from setuptools import find_packages
from setuptools import setup

setup(
    name='ff_interface',
    version='0.0.0',
    packages=find_packages(
        include=('ff_interface', 'ff_interface.*')),
)
