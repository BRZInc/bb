import requests
import urllib.parse
from downloader.repo import Repo

class BitBucketRequestor():
    __projects = "projects/"
    __repos = "repos/"

    def __init__(self, api_url):
        self.url = api_url

    def get_all_repos(self, project):
        try:
            print(self.__build_repos_url(project))
            response = requests.get(self.__build_repos_url(project), {})
            repos = []
            if response.OK:
                j = response.json()
                for r in j.get("values", None):
                    repos.append(Repo(r["slug"], r["id"], r["name"], r["state"], r["project"]["id"], r["forkable"]))
            return repos
        except Exception as e:
            # TODO: Add logging here later on
            print(e)
            return []

    def __build_repos_url(self, project):
        return urllib.parse.urljoin(self.url, "{0}{1}/{2}".format(self.__projects, project, self.__repos))


