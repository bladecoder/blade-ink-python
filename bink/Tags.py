# pylint: disable=E1101

"""Handle Ink tags."""
import ctypes
from bink.loadlib import LIB, BINK_OK

class Tags:
    """Contains a list of tags."""
    def __init__(self, tags, c_len):
        self._tags = tags
        self._len = c_len

    def len(self) -> int:
        """Returns the number of choices."""
        return self._len

    def get(self, idx) -> str:
        """Returns the tag text."""
        tag = ctypes.c_char_p()
        ret = LIB.bink_choices_get_text(self._tags, idx, ctypes.byref(tag))

        if ret != BINK_OK:
            raise RuntimeError("Error getting tag, index out of bounds?")

        result = tag.value.decode('utf-8')
        LIB.bink_cstring_free(tag)

        return result

    def __del__(self):
        LIB.bink_choices_free(self._tags)
