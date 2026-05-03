import json
import logging as log
import logging.handlers
import os.path
import tkinter as tk
import traceback
from pathlib import Path

import pandas
from matplotlib import pyplot as plt
from pandas import DataFrame

DAYS = 30.437 * 3

POIDS_PRESSION_FOLDER = 'PoidsPression'
DOCUMENTS_FOLDER = 'Documents'
BKP_SCRIPTS_FOLDER = 'BkpScripts'
POIDS_PRESSION_PATH = F'{os.getenv('USERPROFILE')}/{DOCUMENTS_FOLDER}/{POIDS_PRESSION_FOLDER}/'
LOG_PATH = f"{os.getenv('USERPROFILE')}/{DOCUMENTS_FOLDER}/NetBeansProjects/PycharmProjects/logs/"
BKP_PATH: str = f"{os.getenv('USERPROFILE')}/{DOCUMENTS_FOLDER}/{BKP_SCRIPTS_FOLDER}/"
LOG_NAME: str = ''


def ppretty(value: object, tab_char: object = '\t', return_char: object = '\n', indent: object = 0) -> str | None:
    try:
        return json.dumps(value, indent=4, sort_keys=True, default=str, check_circular=False)
    except Exception as ex:
        log.error(ex)
        log.error(traceback.format_exc())
    return None


def set_icon(icon_name: str):
    path1: str = f'{Path(__file__).parent.parent.resolve()}/{icon_name}'
    if os.path.isfile(path1):
        plt.get_current_fig_manager().window.iconphoto(False, tk.PhotoImage(file=path1))
    else:
        path2: str = f'{Path(__file__).parent.parent.parent.parent.parent.resolve()}/{icon_name}'
        if os.path.isfile(path2):
            plt.get_current_fig_manager().window.iconphoto(False, tk.PhotoImage(file=path2))
        else:
            log.info(f'Not setting window icon, {path1} & {path2} icon not exists')


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
    log.info(f'>>>> {title} DataFrame: {len(df)} rows\n{df[len(df) - max_rows:]}')
