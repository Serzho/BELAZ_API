import logging
from datetime import datetime

import sys
sys.path.append("../../core")

def base_logger(msg: str, module_name: str) -> None:
    time = datetime.now().time()
    logging.info(f" {time.strftime('%H:%M:%S')} {module_name}: {msg}")

def create_logger(filename: str) -> None:
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.info("\n" * 3 + "/" * 50)