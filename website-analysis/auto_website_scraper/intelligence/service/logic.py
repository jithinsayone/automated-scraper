import requests,json,os,re
from lxml import html
from ..utils.utils import apply_schema_to_url
from ..utils.utils import remove_urls
from ..utils.utils import make_up_url
from ..utils.utils import get_text
from bs4 import BeautifulSoup
from pkg_resources import resource_stream
include_package_data = True
f = open('./sme_website_scraper/resource/services-offered-keys.txt','r')
service_key=[l.strip() for l in f.readlines()]
class ServiceParser(object):
    """
    Every response passes through this logic until get a required data
    """

    def __init__(self, response):
        self.response = response

    def process_response(self, response, domain):
        """
        Get technologies logic
        :param response, domain:
        :return: List
        """
        final_service_offered=[]
        service_offered=[]
        service_seen_links=[]
        service_links=[]
        service_text=[]
        doc = html.fromstring(response.body)
        for link in doc.xpath('//a')+doc.xpath('//A'):
           service_text.append(link.text)
           service_links.append(link.get('href'))
        key_word=['Bedienung','service','leistungen']
        # service_link=response.xpath(".//a/@href").extract()
        # service_text=response.xpath(".//a/text()").extract()

        for word in key_word:
          for text in service_text:
            if text:
              searchObj = re.search( word,text, re.M|re.I)
              if searchObj:
                index=service_text.index(text)
                service_seen_links.append(service_links[index])

        final_link=self.convert(service_seen_links,domain)
        for link in final_link:
          data=self.get_data(link)
          service_offered.append(data)
        for service in service_offered:
          if len(service)>1:
            for service_data in service:
               final_service_offered.append(service_data)
          else:
            final_service_offered.append(service)

        return final_service_offered

    def convert(self,links,domain):
        final_link=[]
        if links:
              urls = remove_urls(links)
              urls=list(set(urls))
              for url in urls:
                  url = make_up_url(url, domain)
                  if not url:
                      continue
                  next_url = apply_schema_to_url(url)

                  if domain in  next_url and  domain != next_url:
                        # print "LINK:",next_url
                        final_link.append(next_url)
                         # yield Request(url=next_url, meta ={'domain': domain})

        if final_link:
          return final_link
        else:
          return []


    def get_data(self,link):
        service_offered=[]
        r = requests.get(link)
        if r.status_code==200:
          visible_text=get_text(r.text)
          for key in service_key:
            if re.search( key,visible_text, re.M|re.I):
              service_offered.append(key)

        return service_offered
