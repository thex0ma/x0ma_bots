import logging
from inspect import iscoroutinefunction
from functools import wraps

logger = logging.getLogger(__name__)


def logs(func):
    if iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger.debug("Calling function: %s", func.__name__)

            try:
                return await func(*args, **kwargs)
            except Exception:
                logger.exception("Error in function: %s", func.__name__)
                raise

        return async_wrapper

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        logger.debug("Calling function: %s", func.__name__)

        try:
            return func(*args, **kwargs)
        except Exception:
            logger.exception("Error in function: %s", func.__name__)
            raise

    return sync_wrapper
