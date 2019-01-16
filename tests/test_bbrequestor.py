from downloader.repo import Repo
from downloader.project import Project
from downloader.pull_request import PullRequest
import pytest
import unittest
import json
from unittest.mock import patch
from downloader.bbrequestor import BitBucketRequestor


@patch('downloader.bbrequestor.requests')
class TestBitBucketRequestor(object):

    __url = "https://somecorp.bitbucket.org/rest/api/latest/"
    __project = "SomeProject"
    __repo = "SomeRepo"

    @pytest.fixture(scope="function")
    def repos_json(self):
        with open("tests/repos-dummy-list.json", "r") as f:
            return json.load(f)

    @pytest.fixture(scope="function")
    def projects_json(self):
        with open("tests/projects-dummy-list.json", "r") as f:
            return json.load(f)

    @pytest.fixture(scope="function")
    def pull_requests_json(self):
        with open("tests/pull-requests-dummy-list.json", "r") as f:
            return json.load(f)

    def test_get_all_projects_proper_url(self, mocked_request):
        b = BitBucketRequestor(self.__url)
        b.get_all_projects()

        mocked_request.get.assert_called_with(
            "https://somecorp.bitbucket.org/rest/api/latest/projects/",
            unittest.mock.ANY)

    @pytest.mark.parametrize('exception', (ConnectionError(), TimeoutError()))
    def test_get_all_projects_connection_error(
            self, mocked_request, exception):
        mocked_request.get.side_effect = exception

        b = BitBucketRequestor(self.__url)
        r = b.get_all_projects()
        assert r == []

    def test_get_all_projects_status_200(self, mocked_request, projects_json):
        mocked_request.get.return_value.OK = True
        mocked_request.get.return_value.json.return_value = projects_json

        b = BitBucketRequestor(self.__url)
        r = b.get_all_projects()
        assert type(r) == list
        assert len(r) == 2
        assert isinstance(r[0], Project)

    def test_get_all_projects_none_projects(self, mocked_request):
        mocked_request.get.return_value.OK = True
        mocked_request.get.return_value.json.return_value = {"values": None}

        b = BitBucketRequestor(self.__url)
        r = b.get_all_projects()
        assert r == []

    def test_get_all_projects_no_values_key(self, mocked_request):
        mocked_request.get.return_value.OK = True
        mocked_request.get.return_value.json.return_value = {}

        b = BitBucketRequestor(self.__url)
        r = b.get_all_projects()
        assert r == []

    def test_get_all_projects_bad_request(self, mocked_request):
        mocked_request.get.return_value.OK = False

        b = BitBucketRequestor(self.__url)
        r = b.get_all_projects()
        assert r == []

    def test_get_all_repos_call_request_with_proper_url(self, mocked_request):
        b = BitBucketRequestor(self.__url)
        b.get_all_repos(self.__project)

        mocked_request.get.assert_called_with(
            "https://somecorp.bitbucket.org/rest/api/latest/" +
            "projects/SomeProject/repos/",
            unittest.mock.ANY)

    @pytest.mark.parametrize('exception', (ConnectionError(), TimeoutError()))
    def test_get_all_repos_connection_error(self, mocked_request, exception):
        mocked_request.get.side_effect = exception

        b = BitBucketRequestor(self.__url)
        r = b.get_all_repos(self.__project)
        assert r == []

    def test_get_all_repos_status_200(self, mocked_request, repos_json):
        mocked_request.get.return_value.OK = True
        mocked_request.get.return_value.json.return_value = repos_json

        b = BitBucketRequestor(self.__url)
        r = b.get_all_repos(self.__project)
        assert type(r) == list
        assert len(r) == 3
        assert isinstance(r[0], Repo)

    def test_get_all_repos_none_repos(self, mocked_request):
        mocked_request.get.return_value.OK = True
        mocked_request.get.return_value.json.return_value = {"values": None}

        b = BitBucketRequestor(self.__url)
        r = b.get_all_repos(self.__project)
        assert r == []

    def test_get_all_repos_no_values_key(self, mocked_request):
        mocked_request.get.return_value.OK = True
        mocked_request.get.return_value.json.return_value = {}

        b = BitBucketRequestor(self.__url)
        r = b.get_all_repos(self.__project)
        assert r == []

    def test_get_all_repos_bad_response(self, mocked_request):
        mocked_request.get.return_value.OK = False

        b = BitBucketRequestor(self.__url)
        r = b.get_all_repos(self.__project)
        assert r == []

    def test_get_all_pull_requests_proper_url(self, mocked_request):
        b = BitBucketRequestor(self.__url)
        b.get_all_pull_requests(self.__project, self.__repo)

        mocked_request.get.assert_called_with(
            "https://somecorp.bitbucket.org/rest/api/latest/" +
            "projects/SomeProject/repos/SomeRepo/pull-requests/",
            unittest.mock.ANY)

    @pytest.mark.parametrize('exception', (ConnectionError(), TimeoutError()))
    def test_get_all_pull_requests_connection_error(
            self, mocked_request, exception):
        mocked_request.get.side_effect = exception

        b = BitBucketRequestor(self.__url)
        r = b.get_all_pull_requests(self.__project, self.__repo)

        assert r == []

    def test_get_all_pull_requests_status_200(
            self, mocked_request, pull_requests_json):
        mocked_request.get.return_value.OK = True
        mocked_request.get.return_value.json.return_value = pull_requests_json

        b = BitBucketRequestor(self.__url)
        r = b.get_all_pull_requests(self.__project, self.__repo)

        assert type(r) == list
        assert len(r) == 2
        assert isinstance(r[0], PullRequest)

    def test_get_all_pull_requests_none_of_them(self, mocked_request):
        mocked_request.get.return_value.OK = True
        mocked_request.get.return_value.json.return_value = {"values": None}

        b = BitBucketRequestor(self.__url)
        r = b.get_all_pull_requests(self.__project, self.__repo)
        assert r == []

    def test_get_all_pull_requests_no_values_key(self, mocked_request):
        mocked_request.get.return_value.OK = True
        mocked_request.get.return_value.json.return_value = {}

        b = BitBucketRequestor(self.__url)
        r = b.get_all_pull_requests(self.__project, self.__repo)
        assert r == []

    def test_get_all_pull_requests_bad_response(self, mocked_request):
        mocked_request.get.return_value.OK = False

        b = BitBucketRequestor(self.__url)
        r = b.get_all_pull_requests(self.__project, self.__repo)
        assert r == []
