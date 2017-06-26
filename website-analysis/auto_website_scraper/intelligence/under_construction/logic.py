import requests,json,re
from bs4 import BeautifulSoup
from..utils.utils import get_text
class ConstructionParser(object):
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
        key_words=['lauching',"under construction",'banned',"coming soon","grand openning",'starten',"bauarbeiten im ganage","keine daten",'verboten']
        visible_text = get_text(response.body) #convert response.body only to  text
        for word in key_words:
          searchObj = re.search( word,visible_text, re.M|re.I)
          if searchObj:
            return True

        return False