import re
from bs4 import BeautifulSoup
from..utils.utils import get_text
class EmailParser(object):
    """
    Every response passes through this logic until get a required data
    """

    def __init__(self, response):
        self.response = response

    def process_response(self, response):
        """
        Get email logic
        :param response:
        :return: List
        """
        visible_text = get_text(response.body)
        email = self.parse_email_address(visible_text)
        return email

    def parse_email_address(self, page):
        """
        Parse email address
        :param page:
        :return:
        """
        emails = list(set(re.findall(r'([a-zA-Z0-9_.+-]+\s*(?:@|\(at\))\s*[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', page)))
        if emails:
            emails.sort()
        final_emails=[]
        for email in emails:
            final_emails.append({'email':email})
        return final_emails

