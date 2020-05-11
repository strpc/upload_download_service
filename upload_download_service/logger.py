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

DIR_LOG_PATH = os.path.abspath(os.path.join(os.getcwd(), '..', DIR_NAME_LOG))

if not os.path.exists(DIR_LOG_PATH):
    try:
        os.mkdir(DIR_LOG_PATH)
    except Exception as e:
        logging.error('Ошибка при создании папок для логов; {0}'.format(e))


formatter = logging.Formatter(LOG_FORMAT, datefmt=FORMAT_DATE_TIME)
handler = handlers.RotatingFileHandler(
    os.path.join(DIR_LOG_PATH, FILE_NAME_LOG),
    maxBytes=FILESIZE_LOG*1024*1024,
    backupCount=COUNT_BACKUP_LOG,
    encoding='utf-8'
    )
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO) # or ERROR
logger.addHandler(handler)


def do_msg(*args):
    msg = ''
    for i in args:
        if i != args[-1]:
            msg += str(i) + ' '
        else:
            msg += str(i)
    if inspect.stack()[1].function != '<module>':
        msg += "; Method " + inspect.stack()[2].function + '()'
    return msg


def do_write_info(*args):
    logger.info(do_msg(*args))

def do_write_debug(*args):
    logger.debug(do_msg(*args))

def do_write_error(*args):
    logger.error(do_msg(*args))

def do_write_warning(*args):
    logger.warning(do_msg(*args))

def do_write_critical(*args):
    logger.critical(do_msg(*args))