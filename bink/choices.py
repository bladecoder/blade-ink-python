"""Choice collections returned by a story."""
import ctypes

from ._ffi import LIB, call, take_string
from .tags import Tags


class Choices:
    """An owned sequence of choice text, with access to each choice's tags."""
    def __init__(self, pointer, length):
        self._choices, self._len = pointer, length

    def __len__(self): return self._len
    def __bool__(self): return bool(self._len)
    def __iter__(self): return (self[index] for index in range(self._len))

    def _index(self, index):
        if not isinstance(index, int): raise TypeError("choice index must be an integer")
        if index < 0: index += self._len
        if not 0 <= index < self._len: raise IndexError("choice index out of range")
        return index

    def __getitem__(self, index):
        value = ctypes.c_char_p()
        call("bink_choices_get_text", self._choices, self._index(index), ctypes.byref(value))
        return take_string(value)

    def get_tags(self, index):
        pointer, length = ctypes.c_void_p(), ctypes.c_size_t()
        call("bink_choices_get_tags", self._choices, self._index(index), ctypes.byref(pointer), ctypes.byref(length))
        return Tags(pointer, length.value)

    def __del__(self):
        if getattr(self, "_choices", None):
            LIB.bink_choices_free(self._choices)
            self._choices = None
