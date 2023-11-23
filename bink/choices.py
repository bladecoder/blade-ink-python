# pylint: disable=E1101, R0903
"""Handle Ink Choices."""
import ctypes
from bink import LIB, BINK_OK


class ChoicesIterator:
    """Iterator for choices."""
    def __init__(self, choices):
        self._choices = choices
        self._index = 0

    def __next__(self):
        if self._index >= len(self._choices):
            raise StopIteration

        self._index += 1
        return self._choices[self._index - 1]


class Choices:
    """List of story choices."""
    def __init__(self, choices, c_len: int):
        self._choices = choices
        self._len = c_len

    def __len__(self) -> int:
        """Returns the number of choices."""
        return self._len

    def __bool__(self) -> bool:
        return self._len != 0

    def __iter__(self):
        return ChoicesIterator(self)

    def __getitem__(self, idx: int) -> str:
        """Returns the choice text"""

        if not isinstance(idx, int):
            raise TypeError

        if idx < 0 or idx > self._len:
            raise IndexError

        return self.get_text(idx)

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
