import re

from bs4 import BeautifulSoup
from ..phone_number.logic import PhoneParser
from ..email.logic import EmailParser
from ..utils.utils import get_text




class PersonalParser(object):
    """
    Every response passes through this logic until get a required data
    """

    def __init__(self, response):
        self.response = response

    def process_personal(self, response):
        """
        Get responsive logic
        :param response:
        :return: string(opening and closing)

        """
        visible_text =get_text(response.body)
        detail=self.detail(visible_text,response)
        return detail

    def detail(self,page,data):
        """
        Get Direct email and  Direct phone numbers
        :param page,data:
        :return: string(opening and closing)

        """

        key_words=['kontakt','ansprechpartner','Mitarbeiterinnen','mitarbeiterinnen']
        detail={}
        for key in key_words:
          present=re.findall(key,page,re.IGNORECASE)
          if present:
            phone_logic=PhoneParser(data)
            phone_number = phone_logic. parse_phone_numbers(page)

            email_logic=EmailParser(data)
            emails = email_logic.parse_email_address(page)


            detail={'direct_email':emails,'direct_phone_numbers':phone_number}

        if detail:
          return detail
        else:
          return  {'direct_email':[],'direct_phone_numbers':[]}
