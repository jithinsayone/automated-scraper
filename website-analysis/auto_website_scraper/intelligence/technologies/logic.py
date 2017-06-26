import re
import yaml
from lxml import html
from ..utils.utils import url_validation
from pkg_resources import resource_stream
include_package_data = True


class TechnologyParser(object):
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
        remove_list_tech=[]
        whitelist_data=[]
        final_whitelist_data=[]
        blacklist_data=None
        white = open('./sme_website_scraper/resource/technologies-whitelist.yaml','r')
        black = open('./sme_website_scraper/resource/technologies-blacklist.yaml','r')


        with white as stream:
          try:
           whitelist=yaml.load(stream)
          except yaml.YAMLError as exc:
           print(exc)
        with black as stream:
          try:
           blacklist=yaml.load(stream)
          except yaml.YAMLError as exc:
           print(exc)

        blacklist_data=blacklist["blacklist"]





        doc = html.fromstring(response.body)
        script_urls = doc.xpath('.//script/@src') + doc.xpath('.//link/@href')
        self.domain_name = domain

        total_technology=[]
        technology_list = []
        technology = []
        matched_technology=[]
        for script_url in script_urls:
            if url_validation(script_url):
                if self.check_all_regexp(script_url):
                    technology_list.append(script_url)

        for technologies in list(set(technology_list)):
            if type(technologies) is list:
                for technology in technologies:
                    technology.append(technology)
            else:
                technology.append(technologies)
            if domain in technology:
                technology.remove(domain)


        #remove whitelist

        for tech in technology:
          for data in whitelist:

               patterns=data["patterns"]
               name=data["name"]

               for pattern in patterns:
                 searchObj = re.search(pattern,tech, re.M|re.I)
                 if searchObj:
                   matched_technology.append({'name':name,'version':'undefined'})
                   try:
                     remove_list_tech.append(tech)
                   except:
                     pass
        technology=list(set(technology)-set(remove_list_tech))
        if not matched_technology:
          matched_technology.append([])
        #remove blacklist

        for tech in technology:
          for black in blacklist_data:
               searchObj = re.search(black,tech, re.M|re.I)
               if searchObj:
                   try:
                    remove_list_tech.append(tech)
                   except:
                    pass
        technology=list(set(technology)-set(remove_list_tech))
        for tech in technology:
          total_technology.append(tech)
        if not total_technology:
          total_technology.append([])

        return {"tech":total_technology,"matched_tech":matched_technology}


    def check_all_regexp(self, script_url):
        """
        Check string with all case of regex
        :param url: String
        :return: String
        """
        regexp = ['jquery','.ico','.png','.jpg','.rss','.xml','feed']
        combinedRegex = re.compile('|'.join('(?:{0})'.format(x) for x in regexp))
        technologies = combinedRegex.findall(script_url)
        if not technologies:
            replace_pattern1 = re.compile('./')
            if replace_pattern1.match(script_url):
                script_url = script_url.replace('./','')
            replace_pattern2 = re.compile('../')
            if replace_pattern2.match(script_url):
                script_url = script_url.replace('../','')
            return script_url
