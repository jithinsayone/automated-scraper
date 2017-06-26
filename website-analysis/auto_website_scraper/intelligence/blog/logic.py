from lxml import html
import urllib





class BlogParser(object):
    """
    Every response passes through this logic until get a required data
    """

    def __init__(self, response):
        self.response = response

    def process_response(self, response,domain):
        """
        Get technologies logic
        :param domain:
        :param response:
        :return: List
        """
        blog_data=[]
        blog_link=response.xpath("//a[re:match(text(),'Blog')]/@href").extract()
        blog_text=response.xpath("//a[re:match(text(),'Blog')]/text()").extract()

        if blog_link and blog_text:
            for temp in range(0,len(blog_link)):
                if 'http' not in blog_link[temp]:
                     blog_link[temp]=domain+blog_link[temp]


                blog_data.append({'url':blog_link[temp],'Title':blog_text[temp],'describtion':'undefined','data':'undefined'})

        return blog_data