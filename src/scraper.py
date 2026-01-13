import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class BookScraper(Scraper):

    def scrape(self) -> list[dict]:
        results = []

        for page in range(1, 51):
            url = f"{self.base_url}catalogue/page-{page}.html"
            soup = BeautifulSoup(requests.get(url).text, "lxml")

            book_links = self.extract_book_links(soup)

            for link in book_links:
                results.append(self.get_product_info(link))

        return results

    def extract_book_links(self, soup) -> list[str]:
        links = []
        for a in soup.select("article.product_pod h3 a"):
            links.append(urljoin(self.base_url, a["href"]))
        return links

    def get_product_info(self, url: str) -> dict:
        soup = BeautifulSoup(requests.get(url).text, "lxml")

        data = {}
        table = soup.select_one("table.table-striped")

        for row in table.select("tr"):
            key = row.th.text.strip()
            value = row.td.text.strip()
            data[key] = value

        data["Description"] = (
            soup.select_one("#product_description ~ p").text.strip()
            if soup.select_one("#product_description ~ p")
            else ""
        )

        data["Rating"] = soup.select_one("p.star-rating")["class"][1]
        data["Title"] = soup.h1.text.strip()

        return data