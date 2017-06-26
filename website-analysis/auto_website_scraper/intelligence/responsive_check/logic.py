from lxml import html
from ..utils.utils import url_validation


class ResponsiveParser(object):
    """
    Every response passes through this logic until get a required data
    """

    def __init__(self, response):
        self.response = response

    def process_response(self, response):
        """
        Get responsive logic
        :param response:
        :return: List
        """
        header_data  = []
        doc = html.fromstring(response.body)
        script_urls = doc.xpath('.//script/@src') + doc.xpath('.//link/@href')
        frameworks = ['bootstrap','foundicons','skeleton','yaml','tuktuk','gumby','kube','groundwork','responsiveaeon']
        if "viewport" in response.body:
            header_data = doc.xpath('.//meta[@name="viewport"]/@content')

        responsive_list = []
        for script_url in script_urls:
            if url_validation(script_url):
                for framework in frameworks:
                    if framework in script_url or header_data :
                        responsive_list.append(script_url)

        return list(set(responsive_list))

