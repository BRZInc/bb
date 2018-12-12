import pytest
import unittest
from unittest.mock import patch

@patch('requests')
def test_get_all_repos(mocked_request):
	print(__name__)
	url = "https://somecorp.bitbucket.org/rest/api/latest/projects/SomeProject/repos/"
	b = BitBucketDownloader(url)
	result = b.get_all_repos()

	mocked_request.get.assert_called_with(url, mock.ANY)