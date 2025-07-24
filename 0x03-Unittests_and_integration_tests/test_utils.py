#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests the access_nested_map function from the utils module.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: any) -> None:
        """
        Tests that access_nested_map returns the expected result for various inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple, expected_message: str) -> None:
        """
        Tests that access_nested_map raises a KeyError with the expected message for invalid inputs.
        """
        with self.assertRaisesRegex(KeyError, expected_message):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Tests the get_json function from the utils module.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: dict, mock_requests_get: Mock) -> None:
        """
        Tests that get_json returns the expected result and calls requests.get once.
        """
        # Configure the mock object to return a Mock object with a json method
        mock_requests_get.return_value = Mock()
        mock_requests_get.return_value.json.return_value = test_payload

        # Call the function under test
        result = get_json(test_url)

        # Assert that requests.get was called exactly once with the test_url
        mock_requests_get.assert_called_once_with(test_url)

        # Assert that the output of get_json is equal to the test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Tests the memoize decorator from the utils module.
    """

    def test_memoize(self) -> None:
        """
        Tests that a method decorated with @memoize calls its wrapped method only once.
        """
        class TestClass:
            """
            A test class to demonstrate memoization.
            """
            def a_method(self) -> int:
                """
                A simple method that returns 42.
                """
                return 42

            @memoize
            def a_property(self) -> int:
                """
                A property that calls a_method and is memoized.
                """
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_a_method:
            test_instance = TestClass()
            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert that a_method was called only once
            mock_a_method.assert_called_once()

            # Assert that the correct result is returned
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
