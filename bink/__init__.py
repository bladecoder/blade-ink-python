"""Python bindings for the Blade Ink C API."""

from ._ffi import (
    BINK_ERROR_ERROR,
    BINK_ERROR_WARNING,
    BINK_FAIL,
    BINK_FAIL_INVALID_ARGUMENT,
    BINK_FAIL_INVALID_UTF8,
    BINK_FAIL_NUL_BYTE,
    BINK_FAIL_NULL_POINTER,
    BINK_FAIL_PANIC,
    BINK_OK,
    BINK_VALUE_BOOL,
    BINK_VALUE_DIVERT_TARGET,
    BINK_VALUE_FLOAT,
    BINK_VALUE_INT,
    BINK_VALUE_LIST,
    BINK_VALUE_STRING,
    BINK_VALUE_VARIABLE_POINTER,
    LIB,
)

__all__ = [name for name in globals() if name.startswith("BINK_")] + ["LIB"]
