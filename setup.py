"""Package definition."""


import sys
from setuptools import setup, Distribution
from wheel.bdist_wheel import bdist_wheel


class BinaryDistribution (Distribution):
    def has_ext_modules(self):
        return True


class BdistWheel(bdist_wheel):
    def get_tag(self):
        return ('py3', 'none') + super().get_tag()[2:]


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


setup(
    package_data={'bink': get_package_data()},
    distclass = BinaryDistribution,
    cmdclass = {
        'bdist_wheel': BdistWheel,
    },
)
