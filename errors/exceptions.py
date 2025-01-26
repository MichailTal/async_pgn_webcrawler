"""Module holding custom exceptions."""


class WebCrawlerException(Exception):
    """Base exception for web crawler errors."""


class FetchException(WebCrawlerException):
    """
    Raised when fetching a PGN from the source fails.

    Attributes:
        message (str): The error message.
        requested_url (str): The URL that caused the error.
    """

    def __init__(self, message: str, requested_url: str) -> None:
        super().__init__(message)
        self.requested_url = requested_url

    def __str__(self) -> str:
        return f"FetchException: {self.args[0]} (URL: {self.requested_url})"


class SaveException(FetchException):
    """
    Raised when a fetched file could not be written to the given directory.

    Attributes:
        desired_path (str): The file path where saving failed.
    """

    def __init__(self, message: str, requested_url: str, desired_path: str) -> None:
        super().__init__(message, requested_url)
        self.desired_path = desired_path

    def __str__(self) -> str:
        return (
            f"SaveException: {self.args[0]} (URL: {self.requested_url}, "
            f"Path: {self.desired_path})"
        )


class CopyExceptions(WebCrawlerException):
    """Exception raised when moving decompressed file failed"""

    def __init__(self, message: str, filename: str):
        super().__init__(message)

        self.filename = filename

    def __str__(self) -> str:
        return f"FetchException: {self.args[0]} (Bad Filename: {self.filename})"
