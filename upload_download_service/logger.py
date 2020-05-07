# -*- coding: utf-8 -*-
import inspect
import os
import logging
import logging.handlers as handlers

from config import (
    DIR_NAME_LOG,
    FILE_NAME_LOG,
    FILESIZE_LOG,
    COUNT_BACKUP_LOG,
    LOG_FORMAT,
    FORMAT_DATE_TIME,
)


if not os.path.exists(os.path.join(os.getcwd(), DIR_NAME_LOG)):
    try:
        os.mkdir(os.path.join(os.getcwd(), DIR_NAME_LOG))
    except Exception as e:
        logging.error('Ошибка при создании папок для логов; {0}'.format(e))


formatter = logging.Formatter(LOG_FORMAT, datefmt=FORMAT_DATE_TIME)
handler = handlers.RotatingFileHandler(os.path.join(DIR_NAME_LOG, FILE_NAME_LOG),
                                       maxBytes=FILESIZE_LOG*1024*1024,
                                       backupCount=COUNT_BACKUP_LOG,
                                       encoding='utf-8'
                                       )
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO) # or ERROR
logger.addHandler(handler)


def do_write_log(log_type, *args):
    msg = ''
    for i in args:
        if i != args[-1]:
            msg += str(i) + ' '
        else:
            msg += str(i)

    if inspect.stack()[1].function != '<module>':
        msg += "; Method " + inspect.stack()[1].function + '()'

    if log_type == 'LOG_TYPE_INFO':
        logger.info(msg)
    if log_type == 'LOG_TYPE_DEBUG':
        logger.debug(msg)
    if log_type == 'LOG_TYPE_WARNING':
        logger.warning(msg)
    if log_type == 'LOG_TYPE_ERROR':
        logger.error(msg)
    if log_type == 'LOG_TYPE_CRITICAL':
        logger.critical(msg)
