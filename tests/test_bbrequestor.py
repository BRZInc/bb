import pytest
import unittest
import json
from unittest.mock import patch
from downloader.bbrequestor import BitBucketRequestor
from downloader.repo import Repo


class TestBitBucketRequestor(object):

	url = "https://somecorp.bitbucket.org/rest/api/latest/"
	project = "SomeProject"
	repo = "SomeRepo"

	@pytest.fixture(scope="class")
	def repos_json(self):
		with open("tests/repos-dummy-list.json", "r") as f:
			return json.load(f)

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
	def test_get_all_repos_status_200(self, mocked_request, repos_json):
		mocked_request.get.return_value.OK = True
		mocked_request.get.return_value.json.return_value = repos_json

		b = BitBucketRequestor(self.url)
		r = b.get_all_repos(self.project)
		assert type(r) == list
		assert len(r) == 3
		assert isinstance(r[0], Repo)

	@patch('downloader.bbrequestor.requests')
	def test_get_all_repos_none_repos(self, mocked_request):
		mocked_request.get.return_value.OK = True
		mocked_request.get.return_value.json.return_value = {"values": None}

		b = BitBucketRequestor(self.url)
		r = b.get_all_repos(self.project)
		assert r == []

	@patch('downloader.bbrequestor.requests')
	def test_get_all_repos_no_values_key(self, mocked_request):
		mocked_request.get.return_value.OK = True
		mocked_request.get.return_value.json.return_value = {}

		b = BitBucketRequestor(self.url)
		r = b.get_all_repos(self.project)
		assert r == []

	@patch('downloader.bbrequestor.requests')
	def test_get_all_repos_bad_response(self, mocked_request):
		mocked_request.get.return_value.OK = False

		b = BitBucketRequestor(self.url)
		r = b.get_all_repos(self.project)
		assert r == []
