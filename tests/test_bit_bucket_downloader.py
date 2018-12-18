import pytest
import unittest
from unittest.mock import patch
from downloader.bit_bucket_downloader import BitBucketDownloader
from requests import Response
import json

class TestBitBucketDownloader(object):

	url = "https://somecorp.bitbucket.org/rest/api/latest/projects/SomeProject/repos/"

	@pytest.fixture(scope="class")
	def simple_json(self):
		return "{'a key': 'a value'}"

	@patch('downloader.bit_bucket_downloader.requests')
	def test_get_all_repos(self, mocked_request):		
		b = BitBucketDownloader(self.url)
		result = b.get_all_repos()

		mocked_request.get.assert_called_with(self.url, unittest.mock.ANY)

	@pytest.mark.parametrize('exception', (ConnectionError(), TimeoutError()))
	@patch('downloader.bit_bucket_downloader.requests')
	def test_get_all_repos_connection_error(self, mocked_request, exception):
		mocked_request.get.side_effect = exception
		b = BitBucketDownloader(self.url)
		r = b.get_all_repos()
		assert r == None

	@patch('downloader.bit_bucket_downloader.requests')
	def test_get_all_repos_status_200(self, mocked_request, simple_json):
		mocked_request.get.return_value.OK = True
		mocked_request.get.return_value.json.return_value = simple_json

		b = BitBucketDownloader(self.url)
		r = b.get_all_repos()
		assert r == simple_json

	@patch('downloader.bit_bucket_downloader.requests')
	def test_get_all_repos_status_404(self, mocked_request):
		mocked_request.get.return_value.OK = False

		b = BitBucketDownloader(self.url)
		r = b.get_all_repos()
		assert r == None