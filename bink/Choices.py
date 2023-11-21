from bink.loadlib import lib, BINK_OK
import ctypes

class Choices:  
    def __init__(self, choices, c_len: int):    
        self._choices = choices
        self._len = c_len

    def len(self) -> int:
        return self._len
    
    def get_text(self, idx) -> str:
        text = ctypes.c_char_p()
        ret = lib.bink_choices_get_text(self._choices, idx, ctypes.byref(text))

        if ret != BINK_OK:
            raise RuntimeError("Error getting choice text, index out of bounds?")

        result = text.value.decode('utf-8')
        lib.bink_cstring_free(text)

        return result
    
    def __del__(self):
        lib.bink_choices_free(self._choices)
