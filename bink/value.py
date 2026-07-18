"""Typed Ink values, value arrays, and Ink lists."""
import ctypes

from ._ffi import (BINK_VALUE_BOOL, BINK_VALUE_FLOAT, BINK_VALUE_INT,
                   BINK_VALUE_LIST, BINK_VALUE_STRING, LIB, call, take_string)


class Value:
    """An owned FFI value. Construct it from bool, int, float, str, or InkList."""
    def __init__(self, value=None, _pointer=None, _owned=True):
        self._owned = _owned
        if _pointer is not None:
            self._value = _pointer
            return
        self._value = ctypes.c_void_p()
        if isinstance(value, InkList): call("bink_value_new_list", value._list, ctypes.byref(self._value))
        elif isinstance(value, bool): call("bink_value_new_bool", value, ctypes.byref(self._value))
        elif isinstance(value, int): call("bink_value_new_int", value, ctypes.byref(self._value))
        elif isinstance(value, float): call("bink_value_new_float", value, ctypes.byref(self._value))
        elif isinstance(value, str): call("bink_value_new_string", value.encode(), ctypes.byref(self._value))
        else: raise TypeError("Value must be bool, int, float, str, or InkList")

    @property
    def kind(self):
        kind = ctypes.c_int(); call("bink_value_get_kind", self._value, ctypes.byref(kind)); return kind.value

    def to_python(self):
        if self.kind == BINK_VALUE_BOOL:
            out = ctypes.c_bool(); call("bink_value_get_bool", self._value, ctypes.byref(out)); return out.value
        if self.kind == BINK_VALUE_INT:
            out = ctypes.c_int32(); call("bink_value_get_int", self._value, ctypes.byref(out)); return out.value
        if self.kind == BINK_VALUE_FLOAT:
            out = ctypes.c_float(); call("bink_value_get_float", self._value, ctypes.byref(out)); return out.value
        if self.kind == BINK_VALUE_STRING:
            out = ctypes.c_char_p(); call("bink_value_get_string", self._value, ctypes.byref(out)); return take_string(out)
        if self.kind == BINK_VALUE_LIST:
            out = ctypes.c_void_p(); call("bink_value_get_list", self._value, ctypes.byref(out)); return InkList(_pointer=out)
        raise TypeError("this Ink value has no Python representation")

    def __del__(self):
        if getattr(self, "_value", None) and self._owned: LIB.bink_value_free(self._value)
        self._value = None


class ValueArray:
    """Owned argument array for function evaluation and path selection."""
    def __init__(self, values=()):
        self._values = ctypes.c_void_p(); call("bink_value_array_new", ctypes.byref(self._values))
        for value in values: self.append(value)
    def append(self, value):
        owned = value if isinstance(value, Value) else Value(value)
        call("bink_value_array_push", self._values, owned._value)
    def __del__(self):
        if getattr(self, "_values", None): LIB.bink_value_array_free(self._values); self._values = None


class InkList:
    """An owned Ink list of ``(origin.item, value)`` entries."""
    def __init__(self, items=(), _pointer=None):
        self._list = _pointer or ctypes.c_void_p()
        if _pointer is None:
            call("bink_list_new", ctypes.byref(self._list))
            for name, value in items: self.add(name, value)
    def add(self, full_name, value): call("bink_list_add_item", self._list, full_name.encode(), value)
    def __len__(self):
        count = ctypes.c_size_t(); call("bink_list_get_count", self._list, ctypes.byref(count)); return count.value
    @property
    def items(self):
        result = []
        for index in range(len(self)):
            name, value = ctypes.c_char_p(), ctypes.c_int32()
            call("bink_list_get_item", self._list, index, ctypes.byref(name), ctypes.byref(value))
            result.append((take_string(name), value.value))
        return result
    @property
    def origins(self):
        count = ctypes.c_size_t(); call("bink_list_get_origin_count", self._list, ctypes.byref(count))
        result = []
        for index in range(count.value):
            origin = ctypes.c_char_p(); call("bink_list_get_origin", self._list, index, ctypes.byref(origin)); result.append(take_string(origin))
        return result
    def __del__(self):
        if getattr(self, "_list", None): LIB.bink_list_free(self._list); self._list = None
