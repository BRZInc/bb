import requests
import urllib.parse
from downloader.repo import Repo
from downloader.project import Project
from downloader.pull_request import PullRequest

class BitBucketRequestor():
    __projects = "projects/"
    __repos = "repos/"
    __pull_requests = "pull-requests/"

    def __init__(self, api_url):
        self.url = api_url

    def get_all_projects(self):
        try:
            response = requests.get(self.__build_projects_url(), {})
            projects = []

            if response.OK:
                j = response.json()
                for p in j.get("values",[]):
                    projects.append(Project(p["key"], p["id"], p["name"], p["description"], p["public"], p["type"]))

            return projects
        except Exception as e:
            # TODO: Add proper logging over here
            print(e)
            return []

    def get_all_repos(self, project):
        try:
            #print(self.__build_repos_url(project))
            response = requests.get(self.__build_repos_url(project), {})
            repos = []
            if response.OK:
                j = response.json()
                for r in j.get("values", []):
                    repos.append(Repo(r["slug"], r["id"], r["name"], r["state"], r["project"]["id"], r["forkable"]))
            return repos
        except Exception as e:
            # TODO: Add logging here later on
            print(e)
            return []

    def get_all_pull_requests(self, project, repo):
        try:
            response = requests.get(self.__build_pull_requests_url(project, repo), {})
            pull_requests = []
            if response.OK:
                j = response.json()
                for p in j.get("values", []):
                    reviewers_ids = [revs["user"]["id"] for revs in p["reviewers"]]
                    participant_ids = [pars["user"]["id"] for pars in p["participants"]]

                    pull_requests.append(
                        PullRequest(
                            p["id"], 
                            p["version"], 
                            p["title"], 
                            p["description"], 
                            p["state"], 
                            p["createdDate"], 
                            p["updatedDate"], 
                            p["fromRef"]["id"], 
                            p["toRef"]["id"], 
                            p["author"]["user"]["id"], 
                            reviewers_ids, 
                            participant_ids, 
                            p["links"]["self"][0]["href"]))
            
            return pull_requests
        except Exception as e:
            # TODO: Add proper logging over here
            print(e)
            return []

    def __build_projects_url(self):
        return urllib.parse.urljoin(self.url, "{0}".format(self.__projects))

    def __build_repos_url(self, project):
        return urllib.parse.urljoin(self.url, "{0}{1}/{2}".format(self.__projects, project, self.__repos))

    def __build_pull_requests_url(self, project, repo):
        return urllib.parse.urljoin(self.url, "{0}{1}/{2}{3}/{4}".format(self.__projects, project, self.__repos, repo, self.__pull_requests))


