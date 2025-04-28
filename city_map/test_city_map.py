import json
import unittest

from city_map import CityMap


class TestGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('map_expected_paths.json') as f:
            cls.expected_paths = json.load(f)
        with open('map_entities.json') as f:
            entities = json.load(f)
            cls.city_map = CityMap(entities)

    def _validate_path(self, expected_path, actual_path):
        self.assertEqual(expected_path, actual_path,
                         f"Expected path {expected_path} but got {actual_path}")

    def test_1(self):
        # Source to destination in a different neighborhood
        src, dst = 'house-a', 'house-d'
        expected_path = self.expected_paths["test1"]
        actual_path = self.city_map.get_path(src, dst)
        self._validate_path(expected_path, actual_path)
    #
    # def test_2(self):
    #     # Source to airport
    #     src, dst = 'house-a', 'airport-bengurion'
    #     expected_path = self.expected_paths["test2"]
    #     actual_path = self.city_map.get_path(src, dst)
    #     self._validate_path(expected_path, actual_path)
    #
    # def test_3(self):
    #     # Source to destination in a different neighborhood - Broken path by exit rule
    #     src, dst = 'house-e', 'house-a'
    #     expected_path = self.expected_paths["test3"]
    #     actual_path = self.city_map.get_path(src, dst)
    #     self._validate_path(expected_path, actual_path)
    #
    # def test_4(self):
    #     # Source to destination in a different neighborhood - Broken path by entrance rule
    #     src, dst = 'house-d', 'house-c'
    #     expected_path = self.expected_paths["test4"]
    #     actual_path = self.city_map.get_path(src, dst)
    #     self._validate_path(expected_path, actual_path)
    #
    # def test_5(self):
    #     # Source to destination in the same neighborhood - valid path
    #     src, dst = 'house-e', 'house-d'
    #     expected_path = self.expected_paths["test5"]
    #     actual_path = self.city_map.get_path(src, dst)
    #     self._validate_path(expected_path, actual_path)
    #

if __name__ == "__main__":
    unittest.main()