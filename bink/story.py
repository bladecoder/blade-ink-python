"""High-level Story API over blade-ink-ffi."""

import ctypes

from ._ffi import BINK_ERROR_ERROR, LIB, P, call, take_string
from .choices import Choices
from .tags import Tags
from .value import InkList, Value, ValueArray

_ERROR_HANDLER = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, P)
_EXTERNAL_FUNCTION = ctypes.CFUNCTYPE(P, ctypes.c_char_p, P, P)
_VARIABLE_OBSERVER = ctypes.CFUNCTYPE(None, ctypes.c_char_p, P, P)
LIB.bink_story_set_error_handler.argtypes = [
    P,
    _ERROR_HANDLER,
    P,
    ctypes.POINTER(ctypes.c_char_p),
]
LIB.bink_bind_external_function.argtypes = [
    P,
    ctypes.c_char_p,
    _EXTERNAL_FUNCTION,
    P,
    ctypes.POINTER(ctypes.c_char_p),
]
LIB.bink_bind_external_function_with_options.argtypes = [
    P,
    ctypes.c_char_p,
    _EXTERNAL_FUNCTION,
    P,
    ctypes.c_bool,
    ctypes.POINTER(ctypes.c_char_p),
]
LIB.bink_observe_variable.argtypes = [
    P,
    ctypes.c_char_p,
    _VARIABLE_OBSERVER,
    P,
    ctypes.POINTER(ctypes.c_char_p),
]
LIB.bink_observe_variable_with_handle.argtypes = [
    P,
    ctypes.c_char_p,
    _VARIABLE_OBSERVER,
    P,
    ctypes.POINTER(P),
    ctypes.POINTER(ctypes.c_char_p),
]
LIB.bink_variable_observer_remove.argtypes = [P, P, ctypes.POINTER(ctypes.c_char_p)]


# The class intentionally mirrors the complete public blade-ink-ffi Story API.
class Story:  # pylint: disable=too-many-public-methods
    """An Ink story. Every feature in the blade-ink-ffi C API is exposed here."""

    def __init__(self, story_string):
        """Create a story from compiled Ink JSON."""
        self._story = ctypes.c_void_p(None)
        self._callbacks, self._observer_handles = [], []
        call("bink_story_new", ctypes.byref(self._story), story_string.encode())

    def __iter__(self):
        return self

    def __next__(self):
        if not self.can_continue():
            raise StopIteration
        return self.cont()

    @property
    def choices(self):
        """Return the current choice collection."""
        return self.get_current_choices()

    @property
    def tags(self):
        """Return the tags emitted by the latest continuation."""
        return self.get_current_tags()

    @property
    def current_text(self):
        """Return text accumulated by the latest continuation."""
        return self.get_current_text()

    @property
    def current_path(self):
        """Return the current Ink content path."""
        return self.get_current_path()

    def can_continue(self):
        """Return whether normal continuation can produce more content."""
        result = ctypes.c_bool(False)
        call("bink_story_can_continue", self._story, ctypes.byref(result))
        return result.value

    def cont(self):
        """Continue the story by one line."""
        return self._string("bink_story_cont")

    def continue_maximally(self):
        """Continue until the next choice or end of story."""
        return self._string("bink_story_continue_maximally")

    def get_current_text(self):
        """Return text accumulated by the latest continuation."""
        return self._string("bink_story_get_current_text")

    def get_current_path(self):
        """Return the current Ink content path."""
        return self._string("bink_story_get_current_path")

    def build_string_of_hierarchy(self):
        """Return a diagnostic representation of the story hierarchy."""
        return self._string("bink_story_build_string_of_hierarchy")

    def save_state(self):
        """Serialize the current story state."""
        return self._string("bink_story_save_state")

    def _string(self, function):
        result = ctypes.c_char_p()
        call(function, self._story, ctypes.byref(result))
        return take_string(result)

    def continue_async(self, millisecs_limit_async):
        """Continue within a time budget and return whether that pass completed."""
        complete = ctypes.c_bool(False)
        call(
            "bink_story_continue_async",
            self._story,
            millisecs_limit_async,
            ctypes.byref(complete),
        )
        return complete.value

    def get_current_choices(self):
        """Return the choices currently available to the reader."""
        return self._collection("bink_story_get_current_choices", Choices)

    def get_current_tags(self):
        """Return the tags emitted by the latest continuation."""
        return self._collection("bink_story_get_current_tags", Tags)

    def get_global_tags(self):
        """Return tags declared at story scope."""
        return self._collection("bink_story_get_global_tags", Tags)

    def _collection(self, function, cls, *args):
        pointer, length = ctypes.c_void_p(None), ctypes.c_size_t(0)
        call(function, self._story, *args, ctypes.byref(pointer), ctypes.byref(length))
        return cls(pointer, length.value)

    def get_tags_for_content_at_path(self, path):
        """Return tags declared at an Ink content path."""
        return self._collection(
            "bink_story_get_tags_for_content_at_path", Tags, path.encode()
        )

    def choose_choice_index(self, index):
        """Select the current choice at ``index``."""
        call("bink_story_choose_choice_index", self._story, index)

    def choose_path_string(self, path):
        """Jump to an Ink content path."""
        call("bink_story_choose_path_string", self._story, path.encode())

    def choose_path_string_with_args(self, path, args=(), reset_call_stack=True):
        """Jump to a path while providing function-style arguments."""
        values = args if isinstance(args, ValueArray) else ValueArray(args)
        call(
            "bink_story_choose_path_string_with_args",
            self._story,
            path.encode(),
            reset_call_stack,
            values.pointer,
        )

    def evaluate_function(self, name, args=()):
        """Evaluate an Ink function and return its value and text output."""
        values = args if isinstance(args, ValueArray) else ValueArray(args)
        result, text = ctypes.c_void_p(), ctypes.c_char_p()
        call(
            "bink_story_evaluate_function",
            self._story,
            name.encode(),
            values.pointer,
            ctypes.byref(result),
            ctypes.byref(text),
        )
        return Value(_pointer=result).to_python(), take_string(text)

    def load_state(self, state):
        """Restore a state previously produced by :meth:`save_state`."""
        call("bink_story_load_state", self._story, state.encode())

    def reset_state(self):
        """Reset the story to its initial state."""
        call("bink_story_reset_state", self._story)

    def get_visit_count_at_path_string(self, path):
        """Return the visit count recorded for ``path``."""
        count = ctypes.c_int32(0)
        call(
            "bink_story_get_visit_count_at_path_string",
            self._story,
            path.encode(),
            ctypes.byref(count),
        )
        return count.value

    def get_variable(self, name):
        """Return a global Ink variable as a Python value."""
        value = ctypes.c_void_p(None)
        call("bink_var_get", self._story, name.encode(), ctypes.byref(value))
        return Value(_pointer=value).to_python()

    def set_variable(self, name, value):
        """Set a global Ink variable from a Python value."""
        value = value if isinstance(value, Value) else Value(value)
        call("bink_var_set", self._story, name.encode(), value.pointer)

    def list_from_origin(self, origin):
        """Create an Ink list containing all items from ``origin``."""
        return self._story_list("bink_story_list_new_from_origin", origin)

    def list_from_item(self, item):
        """Create an Ink list containing ``item``."""
        return self._story_list("bink_story_list_new_from_item", item)

    def _story_list(self, function, name):
        result = ctypes.c_void_p(None)
        call(function, self._story, name.encode(), ctypes.byref(result))
        return InkList(_pointer=result)

    def switch_flow(self, name):
        """Switch to, or create, the named flow."""
        call("bink_story_switch_flow", self._story, name.encode())

    def remove_flow(self, name):
        """Remove the named flow."""
        call("bink_story_remove_flow", self._story, name.encode())

    def switch_to_default_flow(self):
        """Switch back to the default flow."""
        call("bink_story_switch_to_default_flow", self._story)

    def set_allow_external_function_fallbacks(self, allow):
        """Enable or disable Ink's fallback for unbound external functions."""
        call("bink_story_set_allow_external_function_fallbacks", self._story, allow)

    def bind_external_function(self, name, function, lookahead_safe=False):
        """Bind a Python callable as an Ink external function."""

        def callback(c_name, c_args, _):
            try:
                count = ctypes.c_size_t(0)
                call("bink_fun_args_count", c_args, ctypes.byref(count))
                args = []
                for index in range(count.value):
                    value = ctypes.c_void_p(None)
                    call("bink_fun_args_get", c_args, index, ctypes.byref(value))
                    args.append(Value(_pointer=value).to_python())
                result = function(c_name.decode(), *args)
                if result is None:
                    return None
                return Value(result).detach()
            # A Python exception must never cross a C callback boundary.
            except Exception:  # pylint: disable=broad-exception-caught
                return None

        callback = _EXTERNAL_FUNCTION(callback)
        self._callbacks.append(callback)
        function_name = (
            "bink_bind_external_function_with_options"
            if lookahead_safe
            else "bink_bind_external_function"
        )
        if lookahead_safe:
            call(function_name, self._story, name.encode(), callback, None, True)
        else:
            call(function_name, self._story, name.encode(), callback, None)

    def unbind_external_function(self, name):
        """Remove an external function binding."""
        call("bink_unbind_external_function", self._story, name.encode())

    def set_error_handler(self, handler):
        """Set a callable receiving ``(message, is_error)`` diagnostics."""
        callback = _ERROR_HANDLER(
            lambda message, kind, _: handler(message.decode(), kind == BINK_ERROR_ERROR)
        )
        self._callbacks.append(callback)
        call("bink_story_set_error_handler", self._story, callback, None)

    def observe_variable(self, name, observer, removable=False):
        """Observe changes to a variable and optionally return a removal handle."""

        def callback(c_name, c_value, _):
            try:
                observer(
                    c_name.decode(), Value(_pointer=c_value, _owned=False).to_python()
                )
            # A Python exception must never cross a C callback boundary.
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        callback = _VARIABLE_OBSERVER(callback)
        self._callbacks.append(callback)
        if not removable:
            call("bink_observe_variable", self._story, name.encode(), callback, None)
            return None
        handle = ctypes.c_void_p(None)
        call(
            "bink_observe_variable_with_handle",
            self._story,
            name.encode(),
            callback,
            None,
            ctypes.byref(handle),
        )
        self._observer_handles.append(handle)
        return handle

    def remove_variable_observer(self, handle):
        """Remove an observer returned by :meth:`observe_variable`."""
        call("bink_variable_observer_remove", self._story, handle)
        if handle in self._observer_handles:
            self._observer_handles.remove(handle)

    def __del__(self):
        if getattr(self, "_story", None):
            LIB.bink_story_free(self._story)
            self._story = None


def story_from_file(story_file):
    """Create a story from a compiled Ink JSON file."""
    with open(story_file, encoding="utf-8") as file:
        return Story(file.read())
