import pytest
import unittest
import json
from unittest.mock import patch
from downloader.bbretriever import BitBucketRetriever
from requests import Response

class TestBitBucketRetriever(object):

	url = "https://somecorp.bitbucket.org/rest/api/latest/"
	project = "SomeProject"
	repo = "SomeRepo"

	@pytest.fixture(scope="class")
	def simple_json(self):
		return "{'a key': 'a value'}"

	@pytest.mark.parametrize('exception', (ConnectionError(), TimeoutError()))
	@patch('downloader.bbretriever.requests')
	def test_get_all_repos_connection_error(self, mocked_request, exception):
		mocked_request.get.side_effect = exception
		b = BitBucketRetriever(self.url)
		result = b.get_all_repos(self.project)
		assert result == []

	@patch('downloader.bbretriever.requests')
	def test_get_all_repos(self, mocked_request, simple_json):
		b = BitBucketRetriever(self.url)
		r = b.get_all_repos(self.project)

		mocked_request.get.assert_called_with("https://somecorp.bitbucket.org/rest/api/latest/projects/SomeProject/repos/", unittest.mock.ANY)

	@patch('downloader.bbretriever.requests')
	def test_get_all_repos_status_200_response_type(self, mocked_request, simple_json):
		mocked_request.get.return_value.OK = True
		mocked_request.get.return_value.json.return_value = simple_json

		b = BitBucketRetriever(self.url)
		r = b.get_all_repos(self.project)
		assert r == simple_json

		mocked_request.get.return_value.json.assert_called()

	@patch('downloader.bbretriever.requests')
	def test_get_all_repos_status_404(self, mocked_request):
		mocked_request.get.return_value.OK = False

		b = BitBucketRetriever(self.url)
		r = b.get_all_repos(self.project)
		assert r == []

		mocked_request.get.return_value.json.assert_not_called()