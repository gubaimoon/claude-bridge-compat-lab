import copy
import unittest

from cache_adapter import adapt_request


class CacheAdapterTests(unittest.TestCase):
    def test_only_top_level_system_and_tool_markers_removed(self):
        marker = {"type": "ephemeral"}
        request = {
            "system": [{"type": "text", "text": "SYSTEM", "cache_control": marker}],
            "tools": [{"name": "read_file", "input_schema": {"properties": {"cache_control": {"type": "string"}}}, "cache_control": marker}],
            "messages": [{"role": "user", "content": [{"type": "text", "text": "hello", "cache_control": marker}]}],
        }
        original = copy.deepcopy(request)
        result = adapt_request(request)
        self.assertEqual(request, original)
        self.assertEqual(result["system"], [{"type": "text", "text": "SYSTEM"}])
        self.assertNotIn("cache_control", result["tools"][0])
        self.assertEqual(result["tools"][0]["input_schema"], original["tools"][0]["input_schema"])
        self.assertEqual(result["messages"], original["messages"])

    def test_string_system_and_missing_fields_remain_unchanged(self):
        for request in ({}, {"system": "SYSTEM"}, {"system": None, "tools": None}):
            with self.subTest(request=request):
                self.assertEqual(adapt_request(request), request)

    def test_multiple_markers_are_removed(self):
        request = {"system": [{"cache_control": {}}, {"cache_control": {}}], "tools": [{"cache_control": {}}, {"cache_control": {}}]}
        self.assertEqual(adapt_request(request), {"system": [{}, {}], "tools": [{}, {}]})


if __name__ == "__main__":
    unittest.main()
