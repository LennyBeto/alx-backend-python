0x03-Unittests_and_integration_tests
This repository delves into the foundational concepts of unit and integration testing within Python, leveraging the unittest framework, parameterized library, and unittest.mock module.

📚 Learning Outcomes
Upon successful completion of this project, you will be proficient in:
✅ Articulating the distinctions between unit tests and integration tests.
✅ Employing mocking techniques, test parameterization, and fixture management.
✅ Crafting and executing tests using Python's native unittest framework.
✅ Applying principles of test-driven development (TDD).
✅ Comprehending the purpose and internal workings of memoization.

🧪 Project Organization
The project is structured as follows:

utils.py: Contains essential utility functions, including access_nested_map, get_json, and memoize.

client.py: Defines the GithubOrgClient class, responsible for retrieving data from the GitHub API.

fixtures.py: Provides sample JSON responses from the GitHub API, utilized for test mocking.

test_utils.py: Houses the unit tests specifically designed for the utils.py module, incorporating parameterized and mock.

test_client.py: Contains both unit and integration tests for the client.py module, making use of provided fixtures and mocking.

🧪 Testing Paradigms
This project explores two primary testing methodologies:

✅ Unit Testing

Focuses on verifying individual functions or methods in isolation.

Concentrates solely on the internal logic of the tested component.

External dependencies (e.g., network calls, database interactions) are simulated or replaced with mocks.

Examples include testing access_nested_map and memoize.

✅ Integration Testing

Validates the seamless interaction and communication between multiple software components.

Involves executing end-to-end pathways through different parts of the system.

Only low-level external calls (e such as HTTP requests) are typically mocked.

An example is testing the GithubOrgClient's interaction with mocked API responses.

🧰 Essential Tools & Libraries
The core tools and libraries used in this project are:

unittest (Python's built-in testing framework)

unittest.mock (for creating mock objects)

parameterized (for data-driven tests)

To install the necessary dependencies, execute the following command:

pip install parameterized

🚀 Executing Tests
You can initiate tests by running specific test files:

python3 -m unittest 0x03-Unittests_and_integration_tests/test_utils.py
python3 -m unittest 0x03-Unittests_and_integration_tests/test_client.py

To run all tests residing in the directory, use the discovery command:

python3 -m unittest discover 0x03-Unittests_and_integration_tests

🧼 Code Style & Documentation Mandates
Adherence to the following standards is required:

All source code must conform to Pycodestyle guidelines (version 2.5).

Every Python file must possess executable permissions.

Each module, class, and function requires a descriptive docstring, expressed as a complete sentence.

All functions and coroutines must include explicit type annotations.

✅ Illustrative Example: Unit Test for access_nested_map

@parameterized.expand([
({"a": 1}, ("a",), 1),
({"a": {"b": 2}}, ("a",), {"b": 2}),
({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
self.assertEqual(access_nested_map(nested_map, path), expected)
