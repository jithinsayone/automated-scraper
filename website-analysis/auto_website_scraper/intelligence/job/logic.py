import requests,json

class JobParser(object):
    """
    Every response passes through this logic until get a required data
    """

    def __init__(self, response):
        self.response = response

    def process_response(self, response):
        """
        Get technologies logic
        :param response, domain:
        :return: List
        """

        # date_data=requests.get("http://timetravel.mementoweb.org/api/json/2013/"+domain)
        # data=date_data.text
        #
        # try:
        #   date = json.loads(data)
        #   return date["mementos"]["last"]["datetime"]
        # except:
        #   return False
        print"HII"