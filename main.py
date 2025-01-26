"""Main Module."""

from src.asyncwebcrawler import AsyncWebCrawler
from src.decompress_files import FileUnzipper


if __name__ == "__main__":
    # Example usage
    crawler = AsyncWebCrawler(
        base_url="https://www.pgnmentor.com/files.html", file_extension=".pgn"
    )
    crawler.run()
    # unzipper = FileUnzipper()
    # unzipper.unzip_files()
    # unzipper.copy_pgn_files()
