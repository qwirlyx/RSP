import logging

logger = logging.getLogger("service")

def do_work():
    logger.debug("DEBUG: запуск обработки")
    logger.info("INFO: сервис начал выполнение")

    try:
        x = 10 / 0 
        return "ok"
    except Exception as e:
        logger.warning("WARNING: произошла подозрительная ситуация", exc_info=True)
        logger.error("ERROR: критическая ошибка", exc_info=True)
        return "error"