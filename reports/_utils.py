import logging
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class Record:
    id: int
    email: str
    name: str
    department: str
    hours_worked: int
    hourly_rate: int
