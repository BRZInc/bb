import pytest
import unittest
from unittest.mock import patch
from downloader.bit_bucket_downloader import BitBucketDownloader

@patch('downloader.bit_bucket_downloader.requests')
def test_get_all_repos(mocked_request):
	print(__name__)
	url = "https://somecorp.bitbucket.org/rest/api/latest/projects/SomeProject/repos/"
	b = BitBucketDownloader(url)
	result = b.get_all_repos()

	mocked_request.get.assert_called_with(url, unittest.mock.ANY)