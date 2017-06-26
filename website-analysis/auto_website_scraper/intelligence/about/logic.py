from lxml import html


class AboutParser(object):
		"""
		Every response passes through this logic until get a required data
		"""

		def __init__(self, response):
				self.response = response

		def process_response(self, response):
				"""
				Get technologies logic
				:param response:
				:return: List
				"""
				doc = html.fromstring(response.body)
				about_us = doc.xpath('.//meta[@name="description"]/@content')
				if not about_us:
						about_us = doc.xpath('.//META[@NAME="description"]/@CONTENT')

				return about_us