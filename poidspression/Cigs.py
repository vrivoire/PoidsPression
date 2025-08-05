import csv
import os.path
import subprocess
from datetime import datetime, timedelta

import poidspression
from poidspression import log

PATH = f"{os.getenv('USERPROFILE')}/GoogleDrive/PoidsPression/"
LOG_PATH = f"{os.getenv('USERPROFILE')}/Documents/NetBeansProjects/PycharmProjects/logs/"
LOG_FILE = f'{LOG_PATH}Cigs.log'
CIG_FILE_NAME = 'C:/Users/ADELE/Documents/NetBeansProjects/PycharmProjects/PoidsPression/poidspression/Cigs.py'


def save_csv(fields):
    log.info(fields)
    with open(PATH + 'Cigs.csv', 'a', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


def load_csv() -> datetime:
    with open(PATH + 'Cigs.csv', 'r', newline='\n', encoding='utf-8') as f:
        reader = csv.reader(f)
        last_date = None
        for row in reader:
            if len(row) > 0:
                log.info(row)
                last_date = row[1]
        last_date = datetime.strptime(last_date, '%d/%m/%Y %H:%M')
        return last_date


def get_date_diff(start: datetime, end: datetime) -> (datetime, datetime, str, timedelta):
    return start, end, f'{abs(start - end)}', (end - start).total_seconds()


def get_j_cig(seconds: int) -> float:
    if seconds == 0:
        seconds = 1
    return round(200.0 / (seconds / 86400), 1)


if __name__ == "__main__":
    poidspression.set_up(__file__)

    last_date: datetime = load_csv()
    line: (datetime, datetime, str, timedelta) = get_date_diff(last_date, datetime.now().replace(second=0, microsecond=0))
    get_j_cig = get_j_cig(line[3])
    save_csv([
        line[0].strftime('%d/%m/%Y %H:%M'),
        line[1].strftime('%d/%m/%Y %H:%M'),
        line[2],
        get_j_cig,
        round(get_j_cig / 25, 1)
    ])

    if CIG_FILE_NAME != __file__.replace('\\', '/'):
        try:
            completed_process = subprocess.Popen(["C:/Program Files/Notepad++/notepad++.exe", PATH + 'Cigs.csv'])
        except subprocess.CalledProcessError as e:
            log.info(f"Error executing command: {e}")
            log.info(f"Stderr: {e.stderr}")
