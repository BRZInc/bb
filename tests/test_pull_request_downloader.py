import pytest

@pytest.fixture(scope=module)
def repos_json_response():
	with open("tests/repos-dummy-list.json") as f:
		return f.read().replace("\n", "")

def test_get_all_repos(repos_json_response):
	p = PullRequestDownloader(BitBucketDownloader)
	repos = p.get_all_repos()
	assert len(repos) == 3

@pytest.mark.skip(reason="will implement a bit later")
def test_get_all_repos_empty():
	assert 0

@pytest.mark.skip(reason="will implement a bit later")
def test_get_all_repos_service_unavailable():
	assert 0

@pytest.mark.skip(reason="will implement a bit later")
def test_get_all_repos_unauthorized():
	assert 0

@pytest.mark.skip(reason="will implement a bit later")
def test_get_all_pull_requests():
	assert 0

@pytest.mark.skip(reason="will implement a bit later")
def test_get_all_pull_requests_empty():
	assert 0

@pytest.mark.skip(reason="will implement a bit later")
def test_get_all_pull_requests_service_unavailable():
	assert 0