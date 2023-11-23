from bink.story import Story, story_from_file
import unittest


class StoryTestCase(unittest.TestCase):
    def test_oneline(self):
        story = story_from_file("inkfiles/oneline.ink.json")
        self.assertTrue(story.can_continue())
        self.assertEqual(story.cont(), "Line.\n")

    def test_the_intercept(self):
        story = story_from_file("inkfiles/TheIntercept.ink.json")
        self.assertTrue(story.can_continue())

        end = False

        while not end:
            while story.can_continue():
                line = story.cont()
                print(line)  # Assuming 'line' is a byte-like object

            # Obtain and print choices
            choices = story.get_current_choices()

            print(f"Num. choices: {len(choices)}\n")

            if len(choices) != 0:
                for i in range(len(choices)):
                    text = choices.get_text(i)
                    print(f"{i + 1}. {text}")

                # Always choose the first option
                ret = story.choose_choice_index(0)
            else:
                end = True

        print("Story ended ok.")


if __name__ == '__main__':
    unittest.main()
