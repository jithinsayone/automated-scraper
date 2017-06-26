import re

from bs4 import BeautifulSoup



class TimeParser(object):
    """
    Every response passes through this logic until get a required data
    """

    def __init__(self, response):
        self.response = response

    def process_time(self, response):
        """
        Get responsive logic
        :param response:
        :return: string(opening and closing)

        """
        soup = BeautifulSoup(response.body, 'html.parser')
        texts = soup.findAll(text=True)
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()

        time = self.parse_time(visible_text)
        return time
    def parse_time(self,data):
        """

        :param response:
        :return:string
        """

        days=['montag','dientag','mittwoch','donnerstag','freitag','samtag','monday','tuesday','wednesday','thursday','friday','saturday','sunday','zeit']

        total_time=[]

        for day in days:

          details=re.findall(day,data,re.IGNORECASE)
          if details:
            pos=data.index(details[0])

            total_time.append(re.sub('\s+', '', data[pos:pos+80]))

        if total_time:
          return total_time
        else:
          return []
