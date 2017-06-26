import re

from lxml import html
from ..utils.utils import make_up_url
import feedparser


class FeedParser(object):
        """
        Every response passes through this logic until get a required data
        """

        def __init__(self, response):
                self.response = response

        def process_response(self, response, domain):

                #  Get postal address logic
                #  :param response:
                #  :return: List
                total_feed=[]
                rss_url=[]
                doc = html.fromstring(response.body)
                feed_data=['rss','feed']
                total_link = doc.xpath('//@href')
                total_link=list(set(total_link))
                for link in total_link:
                  for rss_f in feed_data:
                    searchObj = re.search( rss_f,link, re.M|re.I)
                    if searchObj:
                      if "http" not in link:
                         link=make_up_url(link,domain)
                         rss_url.append(link)

                feed_data=[]
                rss_url=list(set(rss_url))
                for link in rss_url:
                   # feed=feedparser.parse(link)
                   # if feed["items"]:
                   #    for data in feed["items"]:
                   #       feed_data.append({"title":data['title'],'describtion':data['description']})
                   #    # print "TITLE:",feed["items"][0]["title"]
                   #    # print "DESCRIBITON",feed["items"][0]["description"]
                   total_feed.append({'url':link,'type':'undefined'})

                #to extract from rss


                return total_feed
