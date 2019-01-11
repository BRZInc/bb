import pytest
import unittest
from unittest.mock import patch
from downloader.bbrequestor import BitBucketRequestor


class TestBitBucketRequestor(object):

	url = "https://somecorp.bitbucket.org/rest/api/latest/"
	project = "SomeProject"
	repo = "SomeRepo"

	@pytest.fixture(scope="class")
	def simple_json(self):
		return "{'a key': 'a value'}"

	@patch('downloader.bbrequestor.requests')
	def test_get_all_repos(self, mocked_request):
		b = BitBucketRequestor(self.url)
		b.get_all_repos(self.project)

		mocked_request.get.assert_called_with("https://somecorp.bitbucket.org/rest/api/latest/projects/SomeProject/repos/", unittest.mock.ANY)

	@pytest.mark.parametrize('exception', (ConnectionError(), TimeoutError()))
	@patch('downloader.bbrequestor.requests')
	def test_get_all_repos_connection_error(self, mocked_request, exception):
		mocked_request.get.side_effect = exception
		b = BitBucketRequestor(self.url)
		r = b.get_all_repos(self.project)
		assert r == []

	@patch('downloader.bbrequestor.requests')
	def test_get_all_repos_status_200(self, mocked_request, simple_json):
		mocked_request.get.return_value.OK = True
		mocked_request.get.return_value.json.return_value = simple_json

		b = BitBucketRequestor(self.url)
		r = b.get_all_repos(self.project)
		assert r == simple_json

	@patch('downloader.bbrequestor.requests')
	def test_get_all_repos_bad_response(self, mocked_request):
		mocked_request.get.return_value.OK = False

		b = BitBucketRequestor(self.url)
		r = b.get_all_repos(self.project)
		assert r == []
