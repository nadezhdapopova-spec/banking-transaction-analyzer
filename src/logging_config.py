import logging
import os.path
from pathlib import Path

from config import ROOT_DIR

Path(os.path.join(ROOT_DIR, "logs")).mkdir(parents=True, exist_ok=True)

read_xlsx_logger = logging.getLogger("read_xlsx_logger")
read_xlsx_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "read_xlsx.log"),
                                        "w", encoding="utf-8")
read_xlsx_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                                        datefmt="%Y-%m-%d %H:%M:%S")
read_xlsx_handler.setFormatter(read_xlsx_formatter)
read_xlsx_logger.addHandler(read_xlsx_handler)
read_xlsx_logger.setLevel(logging.DEBUG)


external_api_logger = logging.getLogger("external_api_logger")
external_api_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "external_api.log"),
                                           "w", encoding="utf-8")
external_api_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                                           datefmt="%Y-%m-%d %H:%M:%S")
external_api_handler.setFormatter(external_api_formatter)
external_api_logger.addHandler(external_api_handler)
external_api_logger.setLevel(logging.DEBUG)


src_utils_logger = logging.getLogger("src_utils_logger")
src_utils_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "src_utils.log"),
                                        "w", encoding="utf-8")
src_utils_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                                        datefmt="%Y-%m-%d %H:%M:%S")
src_utils_handler.setFormatter(src_utils_formatter)
src_utils_logger.addHandler(src_utils_handler)
src_utils_logger.setLevel(logging.DEBUG)


services_logger = logging.getLogger("services_logger")
services_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "services.log"),
                                       "w", encoding="utf-8")
services_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S")
services_handler.setFormatter(services_formatter)
services_logger.addHandler(services_handler)
services_logger.setLevel(logging.DEBUG)


reports_logger = logging.getLogger("reports_logger")
reports_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "reports.log"),
                                      "w", encoding="utf-8")
reports_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S")
reports_handler.setFormatter(reports_formatter)
reports_logger.addHandler(reports_handler)
reports_logger.setLevel(logging.DEBUG)
