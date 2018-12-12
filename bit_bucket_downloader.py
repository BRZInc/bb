import requests
import json

class BitBucketDownloader():
	def __init__(url=None):
		self.url = url

	def get_all_repos(self):
		response = requests.get(url, {})
		return response