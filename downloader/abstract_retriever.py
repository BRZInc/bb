class AbstractRetriever():
	def get_all_projects(self):
		raise NotImplemented()

	def get_all_repos(self, project):
		raise NotImplemented()

	def get_all_pull_requests(self, project, repo):
		raise NotImplemented()