import logging
import logging.handlers
import os

os.makedirs("logs", exist_ok=True)

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

file_handler = logging.handlers.RotatingFileHandler(
    "logs/app.log",
    maxBytes=5 * 1024 * 1024, 
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler]
)

logging.getLogger("service").setLevel(logging.DEBUG)   
logging.getLogger("controller").setLevel(logging.INFO)  