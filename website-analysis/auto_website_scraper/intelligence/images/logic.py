import re

from lxml import html
from urlparse import urlparse

from ..utils.utils import url_validation


class ImageParser(object):
		"""
		Every response passes through this logic until get a required data
		"""

		def __init__(self, response):
				self.response = response

		def process_response(self, response, domain):
				"""
				Get image logic
				:param response, domain:
				:return: List
				"""
				doc = html.fromstring(response.body)
				image_urls = doc.xpath('.//img/@src') + doc.xpath('.//img/@data-src')
				self.domain_name = domain

				image_list = []
				for image_url in image_urls:
						if url_validation(image_url):
								image_url = self.make_up_url(image_url)
								image_list.append(image_url)
						else:
								# Remove the invalid urls
								image_urls.remove(image_url)

				if image_list:
						return len(list(set(image_list)))

		def make_up_url(self, url):
				"""
				Make up url in to format.
				:param url: String
				:return: String
				"""
				url_object = urlparse(url)
				if (not(url_object.scheme) or not(url_object.netloc)) and url_object.path:
						if re.search('(/.+?/)', url_object.path):
								return self.domain_name+url_object.path
				return url