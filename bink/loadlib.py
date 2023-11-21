import os
import platform
import ctypes.util

# First, look for a bundled FreeType shared object on the top-level of the
# installed freetype-py module.
system = platform.system()
if system == 'Windows':
    library_name = 'bink.dll'
elif system == 'Darwin':
    library_name = 'libbink.dylib'
else:
    library_name = 'libbink.so'

_filename = os.path.join(os.path.dirname(__file__), 'lib/' + library_name)

# If no bundled shared object is found, look for a system-wide installed one.
if not os.path.exists(_filename):
    # on windows all ctypes does when checking for the library
    # is to append .dll to the end and look for an exact match
    # within any entry in PATH.
    _filename = ctypes.util.find_library('bink')

    if _filename is None:
        if platform.system() == 'Windows':
            # Check current working directory for dll as ctypes fails to do so
            _filename = os.path.join(os.path.realpath('.'), "bink.dll")
        else:
            _filename = library_name

try:
    print("lib filename: ", _filename)
    lib = ctypes.CDLL(_filename)
except (OSError, TypeError):
    lib = None
    raise RuntimeError('bink library not found')

lib.bink_story_new.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
lib.bink_story_new.restype = ctypes.c_int

lib.bink_story_can_continue.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_bool)]
lib.bink_story_can_continue.restype = ctypes.c_int

BINK_OK = 0
BINK_FAIL = 1
BINK_FAIL_NULL_POINTER = 2