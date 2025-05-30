from ._utils import Record
from .base import Report


class Payout(Report):
    headers_line = " " * 16 + "name" + " " * 11 + "hours\trate\tpayout"

    @property
    def report_name(self):
        return "payout"

    @property
    def doc(self):
        return """Отчёт по зарплате"""

    @staticmethod
    def formatter(r: Record) -> str:
        return (
            "-" * 15
            + f" {r.name}"
            + " " * (15 - len(r.name))
            + f"{r.hours_worked}\t{r.hourly_rate}\t{int(r.hourly_rate)*int(r.hours_worked)}"
        )
