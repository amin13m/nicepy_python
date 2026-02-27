import logging
from functools import wraps


logger = logging.getLogger("nicepy")

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "(%(filename)s-%(lineno)d)[%(levelname)s] %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.setLevel(30)



from functools import wraps
from nicepy.logger import logger


def log_operation(func):
    @wraps(func)
    def wrapper(self ):
        logger.debug(f"{func.__name__} started -> {self._path}")
        try:
            result = func(self)   
            logger.info(f"{func.__name__} success -> {self._path}")
            return result
        except Exception as e:
            logger.exception(
                f"{func.__name__} failed -> {self._path} | Reason: {e}"
            )
            raise
    return wrapper


from nicepy.logger import logger

def log_start(instance, func_name):
    path_info = getattr(instance, "_path", "unknown")
    logger.debug(f"{func_name} started -> {path_info}")

def log_end(instance, func_name):
    path_info = getattr(instance, "_path", "unknown")
    logger.info(f"{func_name} finished -> {path_info}")

def log_error(instance, func_name, e):
    path_info = getattr(instance, "_path", "unknown")
    logger.exception(f"{func_name} failed -> {path_info} | Reason: {e}")