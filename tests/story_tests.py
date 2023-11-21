from bink import Story
import unittest

class StoryTestCase(unittest.TestCase):
    def test_oneline(self):
        story = Story.from_file("inkfiles/oneline.ink.json")
        self.assertTrue(story.can_continue())
        self.assertEqual(story.cont(), "Line.\n")

    def test_the_intercept(self):
        story = Story.from_file("inkfiles/TheIntercept.ink.json")
        self.assertTrue(story.can_continue())

        end = False

        while not end:
            while story.can_continue():
                line = story.cont()
                print(line)  # Assuming 'line' is a byte-like object

            # Obtain and print choices
            choices = story.get_current_choices()

            print(f"Num. choices: {choices.len()}\n")

            if choices.len() != 0:
                for i in range(choices.len()):
                    text = choices.get_text(i)
                    print(f"{i + 1}. {text}")

                # Always choose the first option
                ret = story.choose_choice_index(0)
            else:
                end = True

        print("Story ended ok.")

if __name__ == '__main__':
    unittest.main()
