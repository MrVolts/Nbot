import requests
from bs4 import BeautifulSoup
from datetime import datetime


class WebScraper:

    def __init__(self, base_url):
        self.visited_urls = set()
        self.base_url = base_url

    def clean_text(self, text):
        soup = BeautifulSoup(text, "lxml")
        text = soup.get_text(separator=' ', strip=True)
        return text

    def get_soup(self, link):
        request_object = requests.get(link, auth=('user', 'pass'))
        soup = BeautifulSoup(request_object.content, 'html.parser')
        return soup

    def find_internal_urls(self, soup):
        internal_urls = set()
        a_tags = soup.findAll("a", href=True)

        for a_tag in a_tags:
            if a_tag["href"].startswith(('#', 'mailto')):
                continue
            elif a_tag["href"].startswith('/') and not a_tag["href"].startswith('//'):
                internal_url = self.base_url + a_tag["href"]
            elif a_tag["href"].startswith("http") or a_tag["href"].startswith("https"):
                internal_url = a_tag["href"]
            else:
                continue

            internal_urls.add(internal_url)

        return internal_urls

    def scrape_text(self, url, websitescraper_data, depth=0, max_depth=3):
        if depth > max_depth or url in self.visited_urls:
            return

        self.visited_urls.add(url)

        soup = self.get_soup(url)
        print(f"Scraping {url}")

        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        cleaned_text = self.clean_text(text)
        if cleaned_text:
            websitescraper_data.append({"text": cleaned_text, "channel": "website_scraper"})

        internal_urls = self.find_internal_urls(soup)

        for internal_url in internal_urls:
            self.scrape_text(internal_url, websitescraper_data, depth + 1, max_depth)

        if depth == 0:
            print(f"\nFinished scraping. Total links scraped: {len(self.visited_urls)}")


