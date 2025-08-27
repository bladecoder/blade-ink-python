from bink.story import story_from_file
import unittest

class TagsInkTestCase(unittest.TestCase):
    def test_tags(self):
        story = story_from_file("inkfiles/tags.ink.json")
        self.assertTrue(story.can_continue())
        
        self.assertEqual("This is the content\n", story.cont())

        current_tags = story.get_current_tags()
        self.assertEqual(2, len(current_tags))
        self.assertEqual("author: Joe", current_tags[0])
        self.assertEqual("title: My Great Story", current_tags[1])

        story.choose_path_string("knot")
        self.assertEqual("Knot content\n", story.cont())
        current_tags = story.get_current_tags()
        self.assertEqual(1, len(current_tags))
        self.assertEqual("knot tag", current_tags[0])

        self.assertEqual("", story.cont())
        current_tags = story.get_current_tags()
        self.assertEqual("end of knot tag", current_tags[0])

if __name__ == '__main__':
    unittest.main()
