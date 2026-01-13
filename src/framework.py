from src.scraper import BookScraper
from src.transformer import BookTransformer

def flow() -> None:
    """
    Run scraper first, then transformer
    """
    scraper = BookScraper(base_url="http://books.toscrape.com/")
    scraper.run()

    transformer = BookTransformer()
    transformer.run()