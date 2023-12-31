# blade-ink-python

Blade Ink Python provides bindings for the Inkle's [Ink](https://github.com/inkle/ink), a scripting language for writing interactive narratives.

`bladeink` is fully compatible with the reference version and supports all its language features.

To learn more about the Ink language, you can check [the official documentation](https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md).

## Installation
From PyPI: `pip install bink`. This will install the library with a bundled Blade Ink binary, so you're ready to go on Windows, macOS and Linux.

## Using the Blade Ink library

Here is a quick example that uses basic features to play an Ink story using the Blade Ink.

```python
from bink.story import Story, story_from_file

# Story is the entry point of the Blade Ink lib.
story = story_from_file("inkfiles/TheIntercept.ink.json")
self.assertTrue(story.can_continue())

end = False

while not end:
    while story.can_continue():
        line = story.cont()
        print(line)

    # Obtain and print choices
    choices = story.get_current_choices()

    print(f"Num. choices: {len(choices)}\n")

    if choices:
        for i, text in enumerate(choices):
            print(f"{i + 1}. {text}")

        # read_input() is a method that you should implement
        # to get the choice selected by the user.
        choice_idx = read_input()
        # set the option selected by the user
        story.choose_choice_index(choice_idx)
    else:
        end = True

print("Story ended ok.")
```

## Executing tests

We can execute Python tests in the `tests` folder using the next command:

```bash
$  python -m unittest discover
```

