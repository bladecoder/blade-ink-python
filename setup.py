"""Package definition."""
import setuptools, sys
from setuptools import find_packages, setup
from wheel.bdist_wheel import bdist_wheel
from os import path
from io import open

class BinaryDistribution (setuptools.Distribution):
    def has_ext_modules(self):
        return True

class BdistWheel(bdist_wheel):
    def get_tag(self):
        return ('py3', 'none') + bdist_wheel.get_tag(self)[2:]

def get_package_data():
    plat_name_idx = None
    # find --plat-name argument idx and get the next argument
    for i, arg in enumerate(sys.argv):
        if arg == '--plat-name':
            plat_name_idx = i + 1
            break

    # if --plat-name argument is present, return ['native/lib_name']
    if plat_name_idx:
        plat_name = sys.argv[plat_name_idx]
        if plat_name.startswith('macosx'):
            lib = 'libbink.dylib'
        elif plat_name.startswith('linux') or plat_name.startswith('manylinux'):
            lib = 'libbink.so'
        elif plat_name.startswith('win'):
            lib = 'bink.dll'
        else:
            raise RuntimeError('Unsupported platform: ' + plat_name)
        
        arch = "x86_64/"
        if "arm64" in plat_name or "aarch64" in plat_name:
            arch = "arm64/"

        lib = arch + lib
        
        return ['native/' + lib]

    # if it is not present, return ['native/*']
    return ['native/*']

description = open(
    path.join(path.abspath(path.dirname(__file__)), 'README.rst'),
    encoding='utf-8').read()

setup(
    name='bink',
    packages=find_packages(exclude=['tests']),
    version='0.3.1',
    description='Runtime for Ink, a scripting language for writing interactive narrative',
    long_description_content_type='text/x-rst',
    long_description=description,
    author='Rafael Garcia',
    license='Apache 2.0',
    package_data={'bink': get_package_data()},
    distclass = BinaryDistribution,
    cmdclass = {
        'bdist_wheel': BdistWheel,
    },
    zip_safe=False # native libraries are included in the package
)
