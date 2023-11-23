# pylint: disable=E1101, R0903

"""Handle Ink tags."""
import ctypes
from bink import LIB, BINK_OK


class TagsIterator:
    """Iterator for tags."""
    def __init__(self, tags):
        self._tags = tags
        self._index = 0

    def __next__(self):
        if self._index >= len(self._tags):
            raise StopIteration

        self._index += 1
        return self._tags[self._index - 1]


class Tags:
    """Contains a list of tags."""
    def __init__(self, tags, c_len):
        self._tags = tags
        self._len = c_len

    def __len__(self) -> int:
        """Returns the number of tags."""
        return self._len

    def __bool__(self) -> bool:
        return self._len != 0

    def __iter__(self):
        return TagsIterator(self)

    def __getitem__(self, idx: int) -> str:
        """Returns the tag text"""

        if not isinstance(idx, int):
            raise TypeError

        if idx < 0 or idx > self._len:
            raise IndexError

        return self.get(idx)

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
