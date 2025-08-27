import pytest
from bink.story import story_from_file


def test_choices_getitem_out_of_bounds():
    story = story_from_file("inkfiles/TheIntercept.ink.json")
    # Advance the story until at least one choice is available
    while story.can_continue() and len(story.choices) == 0:
        story.cont()
    choices = story.choices
    with pytest.raises(IndexError):
        _ = choices[len(choices)]
