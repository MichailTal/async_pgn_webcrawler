"""Module holding the Unzipp Class"""

import os
import zipfile
import shutil
import structlog

from errors import CopyExceptions

logger = structlog.getLogger()


class FileUnzipper:
    """Unzipper Class"""

    def __init__(
        self,
        source_dir: str = "downloads",
        target_dir: str = "unzipped",
        pgn_target_dir: str = "Z:\\Schach\\03_PGN",
    ):
        """
        Initialize the FileUnzipper with source and target directories.

        :param source_dir: Directory containing the zip files.
        :param target_dir: Directory to extract the files into.
        """
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.pgn_target_dir = pgn_target_dir

        os.makedirs(target_dir, exist_ok=True)

    def unzip_files(self):
        """
        Unzip all zip files in the source directory into the target directory.
        Skips files that have already been extracted.
        """
        for filename in os.listdir(self.source_dir):
            if filename.endswith(".zip"):
                zip_path = os.path.join(self.source_dir, filename)
                extract_path = os.path.join(
                    self.target_dir, os.path.splitext(filename)[0]
                )

                if os.path.exists(extract_path):
                    logger.info(f"Already unzipped, skipping: {filename}")
                    continue

                try:
                    with zipfile.ZipFile(zip_path, "r") as zip_ref:
                        zip_ref.extractall(extract_path)
                        logger.info(f"Unzipped: {filename} to {extract_path}")
                except zipfile.BadZipFile:
                    logger.warning(f"Error: Bad zip file {filename}")

    def copy_pgn_files(self):
        """
        Copy all .pgn files from the unzipped directories to the PGN target directory.
        """
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(".pgn"):
                    source_path = os.path.join(root, file)
                    target_path = os.path.join(self.pgn_target_dir, file)

                    if os.path.exists(target_path):
                        logger.info(f"PGN file already exists, skipping: {file}")
                        continue

                    try:
                        shutil.copy2(source_path, target_path)
                        logger.info(f"Copied: {file} to {self.pgn_target_dir}")
                    except Exception as exc:
                        logger.warning(f"Error copying {file}: {exc}")
                        raise CopyExceptions(
                            message=f"Error copying {file}: {exc}", filename=file
                        )
