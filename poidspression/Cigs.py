import csv
import os.path
import subprocess
from datetime import datetime

import poidspression
from poidspression import log

PATH = f"{os.getenv('USERPROFILE')}/GoogleDrive/PoidsPression/"
LOG_PATH = f"{os.getenv('USERPROFILE')}/Documents/NetBeansProjects/PycharmProjects/logs/"
LOG_FILE = f'{LOG_PATH}Cigs.log'
CIG_FILE_NAME = f'{os.getenv('USERPROFILE')}/Documents/NetBeansProjects/PycharmProjects/PoidsPression/poidspression/Cigs.py'


def save_csv(fields):
    log.info(fields)
    with open(PATH + 'Cigs.csv', 'a', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


def load_csv() -> datetime:
    with open(PATH + 'Cigs.csv', 'r', newline='\n', encoding='utf-8') as f:
        reader = csv.reader(f)
        _last_date = ''
        for row in reader:
            if len(row) > 0:
                log.info(row)
                _last_date = row[1]
        _last_date = datetime.strptime(_last_date, '%d/%m/%Y %H:%M')
        return _last_date


def get_date_diff(_start: datetime, _end: datetime) -> tuple[datetime, datetime, str, float]:
    return _start, _end, f'{abs(_start - _end)}', (_end - _start).total_seconds()


def get_j_pkg_cig(secs: float) -> tuple[float, float]:
    if secs == 0:
        secs = 1
    _j_cig: float = round(200.0 / (secs / 86400), 1)
    _pkg_cig: float = round(_j_cig / 25, 1)
    return _j_cig, _pkg_cig


if __name__ == "__main__":
    poidspression.set_up(__file__)

    last_date: datetime = load_csv()
    start, end, diff, seconds = get_date_diff(last_date, datetime.now().replace(second=0, microsecond=0))
    j_cig, pkg_cig = get_j_pkg_cig(seconds)
    save_csv([
        start.strftime('%d/%m/%Y %H:%M'),
        end.strftime('%d/%m/%Y %H:%M'),
        diff,
        j_cig,
        pkg_cig
    ])

    if CIG_FILE_NAME != __file__.replace('\\', '/'):
        try:
            completed_process = subprocess.Popen(["C:/Program Files/Notepad++/notepad++.exe", PATH + 'Cigs.csv'])
        except subprocess.CalledProcessError as e:
            log.info(f"Error executing command: {e}")
            log.info(f"Stderr: {e.stderr}")
