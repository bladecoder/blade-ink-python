from bink.story import Story, story_from_file
import unittest


class StoryTestCase(unittest.TestCase):
    def test_oneline(self):
        story = story_from_file("inkfiles/oneline.ink.json")
        self.assertTrue(story.can_continue())
        self.assertEqual(story.cont(), "Line.\n")

    def test_load_save(self):
        """Test save_state and load_state functionality."""
        # Create a story and get initial text
        story = story_from_file("inkfiles/runtime/load-save.ink.json")

        # Continue to get all initial text
        lines = story.continue_maximally()

        # Check first line
        self.assertEqual(lines, "We arrived into London at 9.45pm exactly.\n")

        # Save the game state
        save_string = story.save_state()

        print(f"Save state: {save_string}")

        # Free the current story and create a new one
        del story

        story = story_from_file("inkfiles/runtime/load-save.ink.json")

        # Load the saved state
        story.load_state(save_string)

        # Choose first choice
        story.choose_choice_index(0)

        # Continue to get the next text
        lines = story.continue_maximally()

        # The text should contain both lines we expect
        self.assertIn("\"There is not a moment to lose!\" I declared.", lines)
        self.assertIn("We hurried home to Savile Row as fast as we could.", lines)

        # Check that we are at the end
        self.assertFalse(story.can_continue())

        # Check that there are no more choices
        choices = story.get_current_choices()
        self.assertEqual(len(choices), 0)

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
