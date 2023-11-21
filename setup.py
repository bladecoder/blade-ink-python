"""Package definition."""
from setuptools import find_packages, setup

setup(
    name='bink',
    packages=find_packages(exclude=['tests']),
    version='0.1.0',
    description='Runtime for Ink, a scripting language for writing interactive narrative',
    author='Rafael Garcia',
    license='Apache 2.0',
)
