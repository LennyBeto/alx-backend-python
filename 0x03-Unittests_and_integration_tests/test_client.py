#!/usr/bin/env python3
"""
Unit and integration tests for the client module.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient

# Assuming fixtures.py exists and contains these payloads
# For the purpose of this example, we'll define minimal placeholders
# If you have a real fixtures.py, ensure these match its content.
org_payload = {"login": "google", "repos_url": "https://api.github.com/orgs/google/repos"}
repos_payload = [
    {"name": "repo1", "license": {"key": "mit"}},
    {"name": "repo2", "license": {"key": "apache-2.0"}},
    {"name": "repo3", "license": None},
]
expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo2"]


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: patch) -> None:
        """
        Tests that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument.
        """
        # Define the expected payload for the mocked get_json
        expected_payload = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected_payload

        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the method under test
        result = client.org()

        # Construct the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Assert that get_json was called exactly once with the expected URL
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the output of org() is equal to the expected payload
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self) -> None:
        """
        Tests that _public_repos_url returns the expected URL based on a mocked payload.
        """
        # Define the payload that the mocked org method will return
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

        # Use patch as a context manager to mock GithubOrgClient.org
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            # Configure the mocked org to return the test_payload
            mock_org.return_value = test_payload

            # Create an instance of GithubOrgClient (org_name doesn't matter here
            # since org is mocked)
            client = GithubOrgClient("testorg")

            # Access the _public_repos_url property
            result = client._public_repos_url

            # Assert that the mocked org property was called once
            mock_org.assert_called_once()

            # Assert that the result is the expected URL from the payload
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: patch) -> None:
        """
        Tests that public_repos returns the expected list of repositories
        and that mocked methods are called once.
        """
        # Define the payload that get_json will return
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": None},
            {"name": "repo3", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = repos_payload

        # Define the URL that _public_repos_url will return
        public_repos_url_value = "https://api.github.com/orgs/testorg/repos"

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = public_repos_url_value

            # Create an instance of GithubOrgClient
            client = GithubOrgClient("testorg")

            # Call the method under test
            result = client.public_repos()

            # Assert that _public_repos_url was called once
            mock_public_repos_url.assert_called_once()

            # Assert that get_json was called once with the correct URL
            mock_get_json.assert_called_once_with(public_repos_url_value)

            # Assert that the list of repos is as expected (only names)
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient.public_repos method.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up the class-level mock for requests.get to simulate API calls.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Define the side_effect for the mocked requests.get
        # This function will return a Mock object with a json() method
        # that returns the appropriate fixture based on the URL.
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return Mock(json=lambda: cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: {}) # Default for unexpected URLs

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Stops the patcher after all tests in the class have run.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Tests that public_repos returns the expected list of repositories
        from the fixtures.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Tests that public_repos with a license argument returns the
        expected list of repositories with that license from the fixtures.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"),
                         self.apache2_repos)
