"""Base Web Crawler Class"""

import asyncio
from urllib.parse import urljoin, urlparse
import os

from aiohttp import ClientSession
from bs4 import BeautifulSoup
import structlog

from errors import FetchException, SaveException

logger = structlog.getLogger()


class AsyncWebCrawler:
    """Web Crawler Class."""

    def __init__(
        self,
        base_url: str,
        download_dir: str = "downloads",
        file_extension: str = "g.zip",
    ) -> None:
        """
        Initialize the crawler with a base URL, download directory, and file extension filter.

        :param base_url: The base URL to start crawling from.
        :param download_dir: Directory to save downloaded files.
        :param file_extension: File extension to filter download links (e.g., ".pgn").
        """
        self.base_url = base_url
        self.download_dir = download_dir
        self.file_extension = file_extension

        os.makedirs(download_dir, exist_ok=True)

    async def fetch(self, url, session):
        """
        Fetch the content of a given URL asynchronously.

        :param url: URL to fetch.
        :param session: aiohttp ClientSession instance.
        :return: The text content of the response or None if an error occurs.
        """
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as exc:
            logger.warning(f"Error fetching {url}: {exc}")
            raise FetchException(
                message=f"Failed to fetch content from {url}", requested_url=url
            ) from exc

    async def fetch_and_save(self, url: str, session: ClientSession) -> None:
        """
        Fetch a file and save it to the download directory if it matches the file extension.

        :param url: URL of the file to download.
        :param session: aiohttp ClientSession instance.
        """
        try:
            filename = os.path.basename(urlparse(url).path)
            if not filename.endswith(self.file_extension):
                return

            filepath = os.path.join(self.download_dir, filename)
            if os.path.exists(filepath):
                logger.info(f"File already exists, skipping: {filename}")
                return

            async with session.get(url) as response:
                response.raise_for_status()
                filepath = os.path.join(self.download_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(await response.read())
                logger.info(f"Downloaded: {filename}")
        except Exception as e:
            logger.warning(f"Error downloading {url}: {e}")
            raise SaveException(
                message=f"Failed to save file {filename}",
                requested_url=url,
                desired_path=filepath,
            )

    async def parse_links(self, url: str, session: ClientSession):
        """
        Parse all links from the given URL that match the specified file extension.

        :param url: URL to parse.
        :param session: aiohttp ClientSession instance.
        :return: A list of matched URLs.
        """
        content = await self.fetch(url, session)
        if not content:
            return []

        soup = BeautifulSoup(content, "html.parser")
        links = []
        for anchor in soup.find_all("a", href=True):
            link = urljoin(self.base_url, anchor["href"])
            if link.endswith(self.file_extension):
                links.append(link)
        return links

    async def crawl(self):
        """
        Start crawling the base URL to find and download files.
        """
        async with ClientSession() as session:
            logger.info(f"Crawling {self.base_url}...")
            links = await self.parse_links(self.base_url, session)
            tasks = [self.fetch_and_save(link, session) for link in links]
            await asyncio.gather(*tasks)

    def run(self):
        """
        Run the crawler asynchronously.
        """
        asyncio.run(self.crawl())
