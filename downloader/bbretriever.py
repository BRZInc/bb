import requests
import json
import urllib.parse

class BitBucketRetriever():
	project_url = "projects/"
	repo_url = "repos/"

	def __init__(self, api_url):
		self.url = api_url

	def get_all_repos(self, project):
		try:
			print(self.__build_repos_url(project))
			response = requests.get(self.__build_repos_url(project), {})
			if response.OK:
				return response.json()
			else:
				raise ConnectionError()
		except Exception as e:
			# TODO: Add logging here later on
			print(e)
			return []

	def __build_project_url(self, project):
		return urllib.parse.urljoin(self.url, self.project_url+project+"/")

	def __build_repos_url(self, project):
		return urllib.parse.urljoin(self.url, self.project_url+project+"/"+self.repo_url)