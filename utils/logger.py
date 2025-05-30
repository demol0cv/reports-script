import logging
from pathlib import Path


def logger_init(verbose: bool = False, logs_dir: str = "logs"):
    Path(logs_dir).mkdir(
        parents=True,
        exist_ok=True,
    )  # Создаем каталог, если он не существует
    log_file = Path(logs_dir) / "app.log"

    # Настройка логгера
    logger = logging.getLogger("root")
    logger.setLevel(logging.DEBUG)

    # Форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if verbose:
        # Обработчик для консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Обработчик для файла
    file_handler = logging.FileHandler(log_file, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
