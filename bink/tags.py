"""Tag collections returned by a story or choice."""

import ctypes

from ._ffi import LIB, call, take_string


class Tags:
    """An owned, immutable sequence of Ink tags."""

    def __init__(self, pointer, length):
        self._tags, self._len = pointer, length

    def __len__(self):
        return self._len

    def __bool__(self):
        return bool(self._len)

    def __iter__(self):
        return (self[index] for index in range(self._len))

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("tag index must be an integer")
        if index < 0:
            index += self._len
        if not 0 <= index < self._len:
            raise IndexError("tag index out of range")
        value = ctypes.c_char_p()
        call("bink_tags_get", self._tags, index, ctypes.byref(value))
        return take_string(value)

    def __del__(self):
        if getattr(self, "_tags", None):
            LIB.bink_tags_free(self._tags)
            self._tags = None
