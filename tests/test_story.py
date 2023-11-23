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
            for line in story:
                print(line)  # Assuming 'line' is a byte-like object

            # Obtain and print choices
            choices = story.choices
            print(f"Num. choices: {len(choices)}\n")

            if choices:
                for i, text in enumerate(choices):
                    print(f"{i + 1}. {text}")
                    
                # Always choose the first option
                story.choose_choice_index(0)
            else:
                end = True

        print("Story ended ok.")


if __name__ == '__main__':
    unittest.main()
