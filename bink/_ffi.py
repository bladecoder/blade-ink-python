"""Low-level ctypes declarations shared by the public wrappers."""

import ctypes
import ctypes.util
import os
import platform

(
    BINK_OK,
    BINK_FAIL,
    BINK_FAIL_NULL_POINTER,
    BINK_FAIL_INVALID_UTF8,
    BINK_FAIL_NUL_BYTE,
    BINK_FAIL_PANIC,
    BINK_FAIL_INVALID_ARGUMENT,
) = range(7)
BINK_ERROR_WARNING, BINK_ERROR_ERROR = range(2)
(
    BINK_VALUE_BOOL,
    BINK_VALUE_INT,
    BINK_VALUE_FLOAT,
    BINK_VALUE_STRING,
    BINK_VALUE_LIST,
    BINK_VALUE_DIVERT_TARGET,
    BINK_VALUE_VARIABLE_POINTER,
) = range(7)


def _load_library():
    names = {"Windows": "bink.dll", "Darwin": "libbink.dylib"}
    library_name = names.get(platform.system(), "libbink.so")
    arch = "arm64" if platform.machine() in ("arm64", "aarch64") else "x86_64"
    filename = os.path.join(os.path.dirname(__file__), "native", arch, library_name)
    if not os.path.exists(filename):
        filename = ctypes.util.find_library("bink") or library_name
    try:
        return ctypes.CDLL(filename)
    except (OSError, TypeError) as exc:
        raise RuntimeError("bink library not found") from exc


LIB = _load_library()
P = ctypes.c_void_p
CP = ctypes.POINTER(ctypes.c_char_p)
SZ = ctypes.c_size_t


def _declare(name, args, restype=ctypes.c_int):
    """Set ctypes argument and result types for an exported C function."""
    fn = getattr(LIB, name)
    fn.argtypes, fn.restype = args, restype


for _name, _args in {
    "bink_story_new": [ctypes.POINTER(P), ctypes.c_char_p, CP],
    "bink_story_can_continue": [P, ctypes.POINTER(ctypes.c_bool), CP],
    "bink_story_cont": [P, CP, CP],
    "bink_story_continue_maximally": [P, CP, CP],
    "bink_story_continue_async": [P, ctypes.c_float, ctypes.POINTER(ctypes.c_bool), CP],
    "bink_story_get_current_text": [P, CP, CP],
    "bink_story_get_current_choices": [P, ctypes.POINTER(P), ctypes.POINTER(SZ), CP],
    "bink_story_choose_choice_index": [P, SZ, CP],
    "bink_story_get_current_tags": [P, ctypes.POINTER(P), ctypes.POINTER(SZ), CP],
    "bink_story_get_global_tags": [P, ctypes.POINTER(P), ctypes.POINTER(SZ), CP],
    "bink_story_get_tags_for_content_at_path": [
        P,
        ctypes.c_char_p,
        ctypes.POINTER(P),
        ctypes.POINTER(SZ),
        CP,
    ],
    "bink_story_choose_path_string": [P, ctypes.c_char_p, CP],
    "bink_story_choose_path_string_with_args": [
        P,
        ctypes.c_char_p,
        ctypes.c_bool,
        P,
        CP,
    ],
    "bink_story_evaluate_function": [P, ctypes.c_char_p, P, ctypes.POINTER(P), CP, CP],
    "bink_story_load_state": [P, ctypes.c_char_p, CP],
    "bink_story_save_state": [P, CP, CP],
    "bink_story_reset_state": [P, CP],
    "bink_story_get_visit_count_at_path_string": [
        P,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_int32),
        CP,
    ],
    "bink_story_get_current_path": [P, CP, CP],
    "bink_story_build_string_of_hierarchy": [P, CP, CP],
    "bink_choices_get_text": [P, SZ, CP, CP],
    "bink_choices_get_tags": [P, SZ, ctypes.POINTER(P), ctypes.POINTER(SZ), CP],
    "bink_tags_get": [P, SZ, CP, CP],
    "bink_value_new_bool": [ctypes.c_bool, ctypes.POINTER(P), CP],
    "bink_value_new_int": [ctypes.c_int32, ctypes.POINTER(P), CP],
    "bink_value_new_float": [ctypes.c_float, ctypes.POINTER(P), CP],
    "bink_value_new_string": [ctypes.c_char_p, ctypes.POINTER(P), CP],
    "bink_value_get_bool": [P, ctypes.POINTER(ctypes.c_bool), CP],
    "bink_value_get_int": [P, ctypes.POINTER(ctypes.c_int32), CP],
    "bink_value_get_float": [P, ctypes.POINTER(ctypes.c_float), CP],
    "bink_value_get_string": [P, CP, CP],
    "bink_value_get_kind": [P, ctypes.POINTER(ctypes.c_int), CP],
    "bink_value_array_new": [ctypes.POINTER(P), CP],
    "bink_value_array_push": [P, P, CP],
    "bink_list_new": [ctypes.POINTER(P), CP],
    "bink_story_list_new_from_origin": [P, ctypes.c_char_p, ctypes.POINTER(P), CP],
    "bink_story_list_new_from_item": [P, ctypes.c_char_p, ctypes.POINTER(P), CP],
    "bink_list_add_item": [P, ctypes.c_char_p, ctypes.c_int32, CP],
    "bink_list_get_count": [P, ctypes.POINTER(SZ), CP],
    "bink_list_get_item": [P, SZ, CP, ctypes.POINTER(ctypes.c_int32), CP],
    "bink_list_get_origin_count": [P, ctypes.POINTER(SZ), CP],
    "bink_list_get_origin": [P, SZ, CP, CP],
    "bink_value_new_list": [P, ctypes.POINTER(P), CP],
    "bink_value_get_list": [P, ctypes.POINTER(P), CP],
    "bink_var_get": [P, ctypes.c_char_p, ctypes.POINTER(P), CP],
    "bink_var_set": [P, ctypes.c_char_p, P, CP],
    "bink_story_switch_flow": [P, ctypes.c_char_p, CP],
    "bink_story_remove_flow": [P, ctypes.c_char_p, CP],
    "bink_story_switch_to_default_flow": [P, CP],
    "bink_story_set_allow_external_function_fallbacks": [P, ctypes.c_bool, CP],
    "bink_unbind_external_function": [P, ctypes.c_char_p, CP],
    "bink_fun_args_count": [P, ctypes.POINTER(SZ), CP],
    "bink_fun_args_get": [P, SZ, ctypes.POINTER(P), CP],
}.items():
    _declare(_name, _args)

for _name, _args in {
    "bink_story_free": [P],
    "bink_choices_free": [P],
    "bink_tags_free": [P],
    "bink_value_free": [P],
    "bink_value_array_free": [P],
    "bink_list_free": [P],
    "bink_cstring_free": [ctypes.c_char_p],
}.items():
    _declare(_name, _args, None)


def check(result, error):
    """Raise the FFI error returned by a non-success status."""
    if result == BINK_OK:
        return
    message = error.value.decode("utf-8") if error.value else "Blade Ink FFI error"
    if error.value:
        LIB.bink_cstring_free(error)
    raise RuntimeError(message)


def call(name, *args):
    """Invoke an FFI function that receives a trailing error-message output."""
    error = ctypes.c_char_p()
    check(getattr(LIB, name)(*args, ctypes.byref(error)), error)


def take_string(value):
    """Decode and free an FFI-owned C string."""
    try:
        return value.value.decode("utf-8") if value.value else ""
    finally:
        if value.value:
            LIB.bink_cstring_free(value)
