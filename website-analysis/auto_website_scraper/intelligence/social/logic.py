import re

from lxml import html
from ..utils.utils import url_validation


class SocialParser(object):
        """
        Every response passes through this logic until get a required data
        """

        def __init__(self, response):
                self.response = response

        def process_response(self, response, domain):
                #  Get postal address logic
                #  :param response:
                #  :return: List
                removal_social_media=['http://www.twitter.com','http://www.youtube.com','http://www.youtube.com/','https://www.facebook.com/','https://www.facebook.com']
                social_media=['facebook','facebook.com','plus.google','fb.com','myspace.com','bebo.com','reddit.com','twitter.com','youtube.com','xing.com','linkedin.com']   #list of social media to define type
                removal_key_words=['policy','settings','privacy']
                combined_url=[]
                doc = html.fromstring(response.body)
                total_link = doc.xpath('//a/@href')
                self.domain_name = domain
                total_link=list(set(total_link))
                temp_total_link=[]

                #Remove unwanted social_media link
                for link in total_link:
                  if link not in removal_social_media:
                    temp_total_link.append(link)
                total_link=temp_total_link

                #remove unwanted key_words
                temp_total_link=[]
                for link in total_link:
                  flag=0
                  for key in removal_key_words:
                    if re.search( key,link, re.M|re.I):
                      flag=1
                      break

                  if flag==0:
                    temp_total_link.append(link)
                total_link=temp_total_link


                for link in total_link:
                    for media in social_media:
                       searchObj = re.search( media,link, re.M|re.I)
                       if searchObj:
                          if re.sub('\.com$', '', media):
                            real_media=re.sub('\.com$', '', media)
                            combined_url.append({'url':link,'type':real_media})
                          else:
                            combined_url.append({'url':link,'type':media})


                return combined_url

