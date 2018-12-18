import requests
import json

class BitBucketDownloader():
	def __init__(self, url=None):
		self.url = url

	def get_all_repos(self):
		try:
			response = requests.get(self.url, {})
			if response.OK:
				return response.json()
			else:
				return None
		except:
			# TODO: Add logging here later on
			return None