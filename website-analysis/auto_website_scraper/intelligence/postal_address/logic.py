import re,unicodedata
from geopy import geocoders
from bs4 import BeautifulSoup
from..utils.utils import get_text

class AddressParser(object):
    """
    Every response passes through this logic until get a required data
    """

    def __init__(self, response):
        self.response = response

    def process_response(self, response):
        """
        Get postal address logic
        :param response:
        :return: List
        """
        visible_text = get_text(response.body)
        postal_address = []
        postal_address = self.parse_postal_address(visible_text)
        return postal_address


    def parse_postal_address(self, page):
        """
        parse postal address
        :param page:
        :return: dictonary containing postal details
        """
        final_postal_address=[]
        if re.findall(r'\d{5}\s?[\w]+',page,re.UNICODE): #check for combination of zip code and area name
            postal_addr = re.findall(r'\d{5}\s[\w]+',page,re.UNICODE)
            postal_addr=set(postal_addr)           #remove duplicates

            for entry in postal_addr:

                zip_code = re.findall(r'\d+',entry)[0]
                entry=entry.replace(zip_code,u'')
                place_name = re.findall(r'[\w]+',entry,re.UNICODE)[0]
                gn = geocoders.GoogleV3()

                try:
                  country, (lat, lng)= gn.geocode(place_name)

                  country=country.replace(',', " ")
                  country=country.replace("'", " ")
                except:
                  continue

                final_postal_address.append({'street':'undefined','country':country,'postal_code':zip_code,'place':place_name,'type': 'undefined'})

            return final_postal_address
        else:
          return []

