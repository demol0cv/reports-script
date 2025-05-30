import json
import logging
from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Any

from ._utils import Record


logger = logging.getLogger(__name__)


class Report(ABC):
    """Интерфейс."""

    headers_line = " " * 16 + "name" + " " * 11 + "hours\trate\tpayout"

    def formatter(self, r: Record) -> str:
        return (
            "-" * 14
            + f"{r.name}"
            + " " * (15 - len(r.name))
            + f"{r.hours_worked}\t{r.hourly_rate}\t{int(r.hourly_rate)*int(r.hours_worked)}"
        )

    @property
    @abstractmethod
    def report_name(self) -> str:
        """Представляет имя отчёта."""

    @property
    @abstractmethod
    def doc(self) -> str:
        """Представляет строку документации отчёта для --help."""

    def execute(self, files: list[PathLike]) -> None:
        """Печатает отчёт по зарплате.

        :param files: Список файлов для обработки
        :type files: list[PathLike]
        :raises FileNotFoundError: возникает, если файл не найден
        """
        print(self.doc)
        for f in files:
            if not Path(f).exists():
                raise FileNotFoundError(f"Файл {f} не найден")
        print(f"Execute {self.report_name} report")
        records = self.load_csvs(files)
        self.print_report(
            records,
            self.headers_line,
        )

    def save_to_file(
        self,
        input_files: list[PathLike],
        filename: PathLike,
        force: bool,
    ):
        logger.info("Сохранение данных в json файл")
        data: list[Record] = self.load_csvs(input_files)
        if not Path(filename).exists() or force:
            with Path(filename).open(mode="w") as f:
                json.dump(
                    data,
                    f,
                    default=lambda o: o.__dict__ if isinstance(o, Record) else o,
                )
        else:
            print(
                f"Файл {filename} уже существует. Укажите пожалуйста другое имя файла или используйте аргумент --force"
            )

    def load_csvs(self, files: list[PathLike]) -> list[Record]:
        """Парсит CSV-файлы с данными о сотрудниках и возвращает список записей.

        :param files: список путей к файлам
        :type files: list[PathLike]
        :return: Список записей о сотрудниках
        :rtype: list[Record]
        """
        records: list[Record] = []
        for file in files:
            with Path(file).open() as f:
                raw_data = f.readlines()
                data = [line.strip() for line in raw_data if line.strip()]
                logger.debug(f"Загружен файл {file} с {len(data)} строками.")
                if not data:
                    logger.warning(f"Файл {file} пустой или не содержит данных.")
                    raise ValueError(f"Файл {file} пустой или не содержит данных.")
                if len(data) < 2:
                    logger.warning(f"Файл {file} содержит только заголовок.")
                    raise ValueError(f"Файл {file} содержит только заголовок.")
                if (l := len(data[0].split(","))) != 6:
                    logger.warning(
                        "Файл %s содержит некорректное количество заголовков: %s",
                        file,
                        l,
                    )
                    raise ValueError(
                        f"Файл {file} содержит некорректное количество заголовков."
                    )
                record_dict: dict[str, Any] = {
                    "id": "",
                    "email": "",
                    "name": "",
                    "department": "",
                    "hours_worked": 0,
                    "hourly_rate": 0,
                }
                for d in data[1:]:
                    line = d.strip().split(",")
                    if len(line) != 6:
                        logger.warning(
                            f"Некорректная строка в файле {file}: {d.strip()}. Ожидалось 6 полей."
                        )
                        raise ValueError(
                            f"Некорректная строка в файле {file}: {d.strip()}. Ожидалось 6 полей."
                        )
                    for i, header in enumerate(data[0].strip().split(",")):
                        if header == "hours_worked":
                            record_dict[header] = int(line[i])
                        elif header in record_dict:
                            record_dict[header] = line[i]
                        else:
                            record_dict["hourly_rate"] = int(line[i])
                    record: Record = Record(**record_dict)
                    records.append(record)
        logger.debug("Из CSV Загружены записи:")
        [logger.debug(r) for r in records]
        return records

    def print_report(
        self,
        data: list[Record],
        headers_line: str = " " * 14 + "name" + " " * 11 + "hours\trate\tpayout",
    ) -> None:
        r"""Печатает отчёт. Можно передать formatter и headers_line, для форматирования заголовков и строк отчёта.

        :param data: Список с информацией о сотрудниках
        :type data: list[Record]
        :param headers_line: формат заголовка отчёта, defaults to " "*14+"name"+" "*11+"hours\trate\tpayout"
        :type headers_line: str, optional
        :param formatter: _description_, defaults to default_formatter
        :type formatter: Callable[[Record], str], optional
        """
        departments: set[str] = set()
        [departments.add(r.department) for r in data]
        logger.debug("Департаменты: %s", ", ".join(departments))
        print(headers_line)
        for d in departments:
            print(d)
            for r in data:
                if r.department == d:
                    print(self.formatter(r))
