import logging
from service import do_work

logger = logging.getLogger("controller")

def handle_request():
    logger.info("INFO: получен запрос от пользователя")
    logger.debug("DEBUG: это сообщение не будет видно (уровень выше)")
    
    result = do_work()
    logger.info(f"INFO: ответ сервиса = {result}")