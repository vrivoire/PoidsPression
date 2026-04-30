import logging as log
import logging.handlers
import os.path
import tkinter as tk
from pathlib import Path

import pandas
from matplotlib import pyplot as plt
from pandas import DataFrame

HOME_PATH = f"{os.getenv('USERPROFILE')}/"
LOG_PATH = f"{HOME_PATH}Documents/NetBeansProjects/PycharmProjects/logs/"
LOG_NAME: str = ''


def ppretty(value, tab_char='\t', return_char='\n', indent=0):
    string: str = return_char + tab_char * (indent + 1)
    if type(value) is dict:
        items = [
            string + repr(key) + ': ' + ppretty(value[key], tab_char, return_char, indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + return_char + tab_char * indent)
    elif type(value) is list:
        items = [
            string + ppretty(item, tab_char, return_char, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + return_char + tab_char * indent)
    elif type(value) is tuple:
        items = [
            string + ppretty(item, tab_char, return_char, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + return_char + tab_char * indent)
    else:
        return repr(value)


def set_icon(icon_name: str):
    path = f'{Path(__file__).parent.parent.resolve()}\\{icon_name}'
    if os.path.isfile(path):
        log.info(f'>>>> {path} icon exists')
        plt.get_current_fig_manager().window.iconphoto(False, tk.PhotoImage(file=path))
    else:
        log.error(f'>>>> {path} icon not exists')

    path = f'{Path(__file__).parent.parent.parent.parent.parent.resolve()}\\{icon_name}'
    if os.path.isfile(path):
        log.info(f'>>>> {path} icon exists')
        plt.get_current_fig_manager().window.iconphoto(False, tk.PhotoImage(file=path))
    else:
        log.error(f'>>>> {path} icon not exists')


def set_up(log_name: str):
    global LOG_NAME
    LOG_NAME = f'{LOG_PATH}{log_name[log_name.rfind('\\') + 1:len(log_name) - 3]}.log'

    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)

    file_handler = logging.handlers.TimedRotatingFileHandler(LOG_NAME, when='midnight', interval=1,
                                                             backupCount=7, encoding=None, delay=True,
                                                             utc=False, atTime=None, errors=None)
    file_handler.namer = lambda name: name.replace(".log", "") + ".log"
    log.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-8s] [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
        handlers=[
            file_handler,
            logging.StreamHandler()
        ]
    )


def show_df(df: DataFrame, title='', max_columns=None, width=1000, max_rows=50) -> None:
    pandas.set_option('display.max_columns', max_columns)
    pandas.set_option('display.width', width)
    pandas.set_option('display.max_rows', max_rows)
    log.info(f'>>>> {title} DataFrame len: {len(df)}\n{df[len(df) - max_rows:]}')
