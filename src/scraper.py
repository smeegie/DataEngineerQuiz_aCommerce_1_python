
import json
import os
import time
from urllib.parse import urljoin
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from src.config import config


class Scraper:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def run(self) -> None:
        data = self.scrape()
        self.save(data)

    def scrape(self) -> list[dict]:
        raise NotImplementedError

    def save(self, data: list[dict]) -> None:
        os.makedirs(config["RAW_DIRECTORY"], exist_ok=True)
        out_path = os.path.join(config["RAW_DIRECTORY"], "data.json")
        with open(out_path, "w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)


class BookScraper(Scraper):
    def __init__(self, base_url: str) -> None:
        super().__init__(base_url)
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.timeout = 15

    def _get_html(self, url: str) -> str:
        """
        Fetch HTML with retries + timeout to avoid hanging.
        """
        last_err = None
        for attempt in range(1, 3):  # 3 tries
            try:
                r = self.session.get(url, headers=self.headers, timeout=self.timeout)
                r.raise_for_status()
                # Help reduce weird encoding artifacts
                if not r.encoding:
                    r.encoding = "utf-8"
                else:
                    r.encoding = "utf-8"
                return r.text
            except Exception as e:
                last_err = e
                time.sleep(1.5 * attempt)
        raise last_err  # type: ignore[misc]

    def scrape(self) -> list[dict]:
        results: list[dict] = []
        failed_logs = [] 

        # Listing pages are under /catalogue/page-#.html
        for page in range(1, 2):
            listing_url = urljoin(self.base_url, f"catalogue/page-{page}.html")
            print(f"[LIST] page {page}/50: {listing_url}")

            listing_html = self._get_html(listing_url)
            listing_soup = BeautifulSoup(listing_html, "lxml")

            book_urls = self.extract_book_links(listing_soup)

            for i, book_url in enumerate(book_urls, start=1):
                print(f"  [BOOK] page {page} book {i}/{len(book_urls)}")
                # print(book_url) # ahcomment
                try: 
                    results.append(self.get_product_info(book_url))

                    log_entry = {
                        "run_datetime": str(datetime.utcnow().isoformat()),
                        "status": "Success",
                        "url": book_url
                    }
                    log_path = os.path.join(config["RAW_DIRECTORY"], "failed_log.json")
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(log_entry) + "\n")

                except:
                    print(f"  [BOOK] page {page} book {i}/{len(book_urls)} failed")
                    
                    log_entry = {
                        "run_datetime": str(datetime.utcnow().isoformat()),
                        "status": "failed",
                        "url": book_url
                    }
                    log_path = os.path.join(config["RAW_DIRECTORY"], "failed_log.json")
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(log_entry) + "\n")

        return results

    def extract_book_links(self, soup: BeautifulSoup) -> list[str]:
        """
        Extract all book detail page URLs from one listing page.
        The href is relative, so we must urljoin it properly.
        """
        catalogue_base = urljoin(self.base_url, "catalogue/")
        links: list[str] = []
        for a in soup.select("article.product_pod h3 a"):
            href = a.get("href", "")
            links.append(urljoin(catalogue_base, href))
        return links

    def get_product_info(self, url: str) -> dict:
        """
        Visit a book detail page and extract ALL required fields.
        """
        html = self._get_html(url)
        soup = BeautifulSoup(html, "lxml")

        data: dict = {}

        # --- Table fields ---
        table = soup.select_one("table.table-striped")
        if table is None:
            raise ValueError(f"Could not find product table on: {url}")

        for row in table.select("tr"):
            key = row.th.get_text(strip=True)
            val = row.td.get_text(strip=True)

            # normalize weird pound sign sequences
            val = val.replace("Â£", "£")
            data[key] = val

        # --- Title ---
        title_tag = soup.select_one("div.product_main h1")
        data["Title"] = title_tag.get_text(strip=True) if title_tag else ""

        # --- Rating (One/Two/Three/Four/Five) ---
        rating_tag = soup.select_one("p.star-rating")
        if rating_tag and rating_tag.has_attr("class") and len(rating_tag["class"]) > 1:
            data["Rating"] = rating_tag["class"][1]
        else:
            data["Rating"] = ""

        # --- Description ---
        desc_tag = soup.select_one("#product_description + p")
        data["Description"] = desc_tag.get_text(strip=True) if desc_tag else ""

        # Final keys now include:
        # UPC, Product Type, Price (excl. tax), Price (incl. tax), Tax,
        # Availability, Number of reviews, Description, Rating, Title
        return data
