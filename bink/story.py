# pylint: disable=E1101, C0116

"""Handle Ink Story."""
import ctypes
from bink.choices import Choices
from bink.tags import Tags
from bink import LIB, BINK_OK


class Story:
    """Story is the entry point of the Blade Ink lib."""
    def __init__(self, story_string: str):
        err_msg = ctypes.c_char_p()
        story = ctypes.c_void_p()
        ret = LIB.bink_story_new(
            ctypes.byref(story),
            story_string.encode('utf-8'),
            ctypes.byref(err_msg))
        if ret != BINK_OK:
            err = err_msg.value.decode('utf-8')
            LIB.bink_cstring_free(err_msg)
            raise RuntimeError(err)

        self._story = story

    def __next__(self):
        if not self.can_continue():
            raise StopIteration

        return self.cont()

    def __iter__(self):
        return self

    @property
    def choices(self):
        return self.get_current_choices()

    @property
    def tags(self):
        return self.get_current_tags()

    def can_continue(self):
        can_continue = ctypes.c_bool()
        ret = LIB.bink_story_can_continue(
            self._story, ctypes.byref(can_continue))

        if ret != BINK_OK:
            raise RuntimeError("Error in can_continue")

        return can_continue.value

    def cont(self) -> str:
        err_msg = ctypes.c_char_p()
        line = ctypes.c_char_p()
        ret = LIB.bink_story_cont(
            self._story,
            ctypes.byref(line),
            ctypes.byref(err_msg))

        if ret != BINK_OK:
            err = err_msg.value.decode('utf-8')
            LIB.bink_cstring_free(err_msg)
            raise RuntimeError(err)

        result = line.value.decode('utf-8')
        LIB.bink_cstring_free(line)

        return result

    def continue_maximally(self) -> str:
        err_msg = ctypes.c_char_p()
        line = ctypes.c_char_p()
        ret = LIB.bink_story_continue_maximally(
            self._story, ctypes.byref(line), ctypes.byref(err_msg))

        if ret != BINK_OK:
            err = err_msg.value.decode('utf-8')
            LIB.bink_cstring_free(err_msg)
            raise RuntimeError(err)

        result = line.value.decode('utf-8')
        LIB.bink_cstring_free(line)

        return result

    def get_current_choices(self) -> Choices:
        choices = ctypes.c_void_p()
        choice_count = ctypes.c_int()
        ret = LIB.bink_story_get_current_choices(
            self._story, ctypes.byref(choices), ctypes.byref(choice_count))

        if ret != BINK_OK:
            raise RuntimeError("Error getting current choices")

        choices = Choices(choices, choice_count.value)

        return choices

    def choose_choice_index(self, choice_index: int):
        """Chooses the `Choice` from the
        `currentChoices` list with the given index. Internally, this
        sets the current content path to what the
        `Choice` points to, ready to continue story evaluation."""
        err_msg = ctypes.c_char_p()
        cidx = ctypes.c_int(choice_index)
        ret = LIB.bink_story_choose_choice_index(
            self._story, cidx, ctypes.byref(err_msg))

        if ret != BINK_OK:
            err = err_msg.value.decode('utf-8')
            LIB.bink_cstring_free(err_msg)
            raise RuntimeError(err)

    def get_current_tags(self) -> Tags:
        tags = ctypes.c_void_p()
        tag_count = ctypes.c_int()
        ret = LIB.bink_story_get_current_tags(
            self._story, ctypes.byref(tags), ctypes.byref(tag_count))

        if ret != BINK_OK:
            raise RuntimeError("Error getting current tags")

        tags = Tags(tags, tag_count.value)

        return tags

    def choose_path_string(self, path: str):
        err_msg = ctypes.c_char_p()
        story = ctypes.c_void_p()
        ret = LIB.bink_story_new(
            ctypes.byref(story),
            path.encode('utf-8'),
            ctypes.byref(err_msg))
        if ret != BINK_OK:
            err = err_msg.value.decode('utf-8')
            LIB.bink_cstring_free(err_msg)
            raise RuntimeError(err)

    def __del__(self):
        LIB.bink_story_free(self._story)


def story_from_file(story_file: str):
    with open(story_file, 'r', encoding='utf-8') as file:
        content = file.read()
        return Story(content)
