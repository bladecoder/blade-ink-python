# pylint: disable=E1101
"""Handle Ink Choices."""
import ctypes
from bink import LIB, BINK_OK

class Choices:
    """List of story choices."""
    def __init__(self, choices, c_len: int):
        self._choices = choices
        self._len = c_len

    def len(self) -> int:
        """Returns the number of choices."""
        return self._len

    def get_text(self, idx) -> str:
        """Returns the choice text."""
        text = ctypes.c_char_p()
        ret = LIB.bink_choices_get_text(self._choices, idx, ctypes.byref(text))

        if ret != BINK_OK:
            raise RuntimeError(
                "Error getting choice text, index out of bounds?")

        result = text.value.decode('utf-8')
        LIB.bink_cstring_free(text)

        return result

    def __del__(self):
        LIB.bink_choices_free(self._choices)
