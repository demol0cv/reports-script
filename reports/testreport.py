from ._utils import Record
from .base import Report


class TestReport(Report):

    headers_line = " " * 30 + "Имя" + " " * 14 + "Часов  В час\tЗарплата"

    def formatter(self, r: Record) -> str:
        return (
            "\u2796" * 14
            + f" 🙍 {r.name}"
            + " " * (15 - len(r.name))
            + f"{r.hours_worked}🕒\t{r.hourly_rate}💲\t{int(r.hourly_rate)*int(r.hours_worked)}💲"
        )

    @property
    def report_name(self):
        return "testreport"

    @property
    def doc(self):
        return """Тестовый отчёт."""
