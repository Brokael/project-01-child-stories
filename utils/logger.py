import logging
from pathlib import Path


def setup_logger():
    logs_folder = Path("logs")
    logs_folder.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("story_agent")