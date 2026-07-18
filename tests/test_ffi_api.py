"""Integration coverage for the complete public blade-ink-ffi binding surface."""
import unittest

from bink.story import story_from_file
from bink.value import InkList, Value, ValueArray


class FfiApiTestCase(unittest.TestCase):
    def test_values_lists_and_function_evaluation(self):
        self.assertEqual(Value(True).to_python(), True)
        self.assertEqual(Value(7).to_python(), 7)
        self.assertAlmostEqual(Value(1.25).to_python(), 1.25)
        self.assertEqual(Value("hello").to_python(), "hello")
        values = ValueArray([2, 8, 0.4])
        story = story_from_file("inkfiles/function/func-basic.ink.json")
        result, output = story.evaluate_function("lerp", values)
        self.assertAlmostEqual(result, 4.4, places=6)
        self.assertEqual(output, "")
        ink_list = InkList([("letters.a", 1), ("letters.b", 2)])
        self.assertEqual(ink_list.items, [("letters.a", 1), ("letters.b", 2)])
        self.assertEqual(ink_list.origins, ["letters", "letters"])
        self.assertEqual(Value(ink_list).to_python().items, ink_list.items)
        list_story = story_from_file("inkfiles/lists/basic-operations.ink.json")
        self.assertEqual(list_story.list_from_origin("list").origins, ["list"])
        self.assertEqual(list_story.list_from_item("list.a").items, [("list.a", 1)])

    def test_runtime_state_variables_observers_and_external_functions(self):
        story = story_from_file("inkfiles/runtime/variable-observers.ink.json")
        observed = []
        handle = story.observe_variable("x", lambda name, value: observed.append((name, value)), removable=True)
        story.continue_maximally()
        self.assertEqual(observed, [("x", 5)])
        self.assertEqual(story.get_variable("x"), 5)
        story.set_variable("x", 9)
        self.assertEqual(story.get_variable("x"), 9)
        story.remove_variable_observer(handle)

        story = story_from_file("inkfiles/runtime/external-function-2-arg.ink.json")
        story.set_allow_external_function_fallbacks(True)
        story.bind_external_function("externalFunction", lambda name, x, y: x - y)
        self.assertEqual(story.continue_maximally(), "The value is -1.\n")
        story.unbind_external_function("externalFunction")

    def test_story_navigation_async_flows_and_introspection(self):
        story = story_from_file("inkfiles/runtime/multiflow-basics.ink.json")
        story.switch_flow("secondary")
        self.assertEqual(story.continue_maximally(), "")
        story.choose_path_string("knot1")
        self.assertTrue(story.continue_async(1000))
        self.assertEqual(story.current_text, "knot 1 line 1\n")
        self.assertIn("knot1", story.current_path)
        self.assertIn("knot1", story.build_string_of_hierarchy())
        self.assertEqual(story.get_visit_count_at_path_string("knot1"), 0)
        story.switch_to_default_flow()
        story.remove_flow("secondary")
        story.reset_state()
        self.assertTrue(story.can_continue())

    def test_tags_choices_paths_and_error_handler(self):
        story = story_from_file("inkfiles/tags.ink.json")
        story.set_error_handler(lambda message, is_error: None)
        self.assertEqual(list(story.get_global_tags()), ["author: Joe", "title: My Great Story"])
        story.cont()
        self.assertEqual(list(story.tags), ["author: Joe", "title: My Great Story"])
        story.choose_path_string_with_args("knot", (), reset_call_stack=True)
        self.assertEqual(story.cont(), "Knot content\n")
        self.assertEqual(list(story.get_tags_for_content_at_path("knot")), ["knot tag"])
        choice_story = story_from_file("inkfiles/tagsInChoice.ink.json")
        choice_story.continue_maximally()
        self.assertEqual(list(choice_story.choices.get_tags(0)), ["one", "two"])
