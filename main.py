import argparse
import logging

from reports import Payout, Report, TestReport
from utils.logger import logger_init


logger = logging.getLogger(__name__)


def setup_parser(reports: dict[str, Report]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Скрипт подсчёта зарплаты сотрудников")
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Расширенное логирование с выводом в консоль",
    )
    reports_group = parser.add_argument_group("Отчёты")
    reports_group.add_argument(
        "files",
        nargs="*",
        type=str,
        help="Список входных файлов",
    )
    reports_group.add_argument(
        "--report",
        "-r",
        type=str,
        help="Тип отчёта [" + ", ".join([r for r, v in reports.items()]) + "]",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Укажите файл для вывода данных",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="При сохранении отчёта перезаписывает файл если он уже существует",
    )
    return parser


def command_process(args: argparse.Namespace, reports: dict[str, Report]):

    if isinstance(args.files, list) and len(args.files) > 0:
        logger.debug(", ".join(args.files))
        if args.report:
            rpt = reports.get(args.report)
            if rpt:
                rpt.execute(files=args.files)
            if args.output:
                rpt.save_to_file(args.files, args.output, args.force)
            else:
                raise ValueError(f"Отчёт {args.report} не доступен для формирования.")


def main():
    payout = Payout()
    test = TestReport()

    reports = {
        payout.report_name: payout,
        test.report_name: test,
    }

    parser = setup_parser(reports)
    args = parser.parse_args()
    logger_init(verbose=args.verbose)

    try:
        command_process(args, reports)
    except Exception as e:
        parser.error(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()
