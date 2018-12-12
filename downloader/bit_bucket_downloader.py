import requests
import json

class BitBucketDownloader():
	def __init__(self, url=None):
		self.url = url

	def get_all_repos(self):
		response = requests.get(self.url, {})
		return response