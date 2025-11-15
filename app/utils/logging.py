import logging,os
from app.settings import settings
from logging.handlers import RotatingFileHandler
os.makedirs(settings.LOG_DIR , exist_ok=True)

logger=logging.getLogger(settings.APP_NAME)
logger.setLevel(settings.LOG_LEVEL)

formatter = logging.Formatter( 
    " [%(levelname)s]  | %(name)s | %(message)s | %(asctime)s" )

file_handler = RotatingFileHandler(
    os.path.join(settings.LOG_DIR,settings.LOG_FILE),
    mode="a",
    maxBytes=5_000_000,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)