import logging
from os import PathLike
from pathlib import Path


logger = logging.getLogger(__name__)


class CsvLoader:
    def __init__(self, filename: PathLike):
        if not isinstance(filename, PathLike):
            raise TypeError("filename должен быть PathLike")

        self.filename = (
            Path(filename).absolute()
            if isinstance(filename, str)
            else filename.absolute()
        )
        logger.debug(filename)
