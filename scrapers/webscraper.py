import requests
from bs4 import BeautifulSoup
from datetime import datetime


class WebScraper:
    def __init__(self):
        self.visited_urls = set()

    def get_soup(self, link):
        """
        Return the BeautifulSoup object for input link
        """
        request_object = requests.get(link, auth=('user', 'pass'))
        soup = BeautifulSoup(request_object.content, 'html.parser')
        return soup

    def get_status_code(self, link):
        """
        Return the error code for any url
        param: link
        """
        try:
            error_code = requests.get(link).status_code
        except requests.exceptions.ConnectionError:
            error_code = None
        return error_code

    def find_internal_urls(self, lufthansa_url, depth=0, max_depth=2):
        all_urls_info = []
        status_dict = {}
        soup = self.get_soup(lufthansa_url)
        a_tags = soup.findAll("a", href=True)

        if depth > max_depth:
            return {}
        else:
            for a_tag in a_tags:
                if "http" not in a_tag["href"] and "/" in a_tag["href"]:
                    url = "http://www.lufthansa.com" + a_tag['href']
                elif "http" in a_tag["href"]:
                    url = a_tag["href"]
                else:
                    continue

                if url not in self.visited_urls:
                    self.visited_urls.add(url)
                    status_dict["url"] = url
                    status_dict["status_code"] = self.get_status_code(url)
                    status_dict["timestamp"] = datetime.now()
                    status_dict["depth"] = depth + 1
                    all_urls_info.append(status_dict)
        return all_urls_info

    def scrape_text(self, url):
        soup = self.get_soup(url)
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return text