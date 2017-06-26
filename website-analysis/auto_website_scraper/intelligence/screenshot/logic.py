from selenium import webdriver
import os
import boto
import boto.s3
import sys,os
from boto.s3.key import Key


class ScreenshotParser(object):
    """
    Every response passes through this logic until get a required data
    """
    def __init__(self, response):
        self.response = response

    def process_response(self,domain):
        """
        Get screen shot logic
        :param response, domain,:
        :return: List
        """
        return self.get_screen_shot(domain)

    def get_screen_shot(self, domain):
        """
        Get screen shot with unique site variable name
        :param domain, site_variable:
        :return: List
        """

        try :
            cmd="wkhtmltopdf "+domain+" /home/sme-scraper-website/screenshot.pdf"
            os.system(cmd)

            # AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
            # AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
            #
            #
            #
            # REGION_HOST = 's3.eu-central-1.amazonaws.com'
            # bucket_name = 'sme-website-scraper-screenshot'
            # conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,host=REGION_HOST)
            #
            #
            # bucket = conn.get_bucket(bucket_name)
            # testfile = '/home/sme-scraper-website/screenshot.png'
            # file_title=domain
            # k = Key(bucket)
            # k.key = file_title.replace('/', '')
            # k.set_contents_from_filename(testfile)
            # screenshot_url = k.generate_url(60000, query_auth=True)
            #return screenshot_url
            return  True
        except IOError:
               return "ERROR IN RETREIVING SCREENSHOT"