import logging as log
import logging.handlers
import sys
import time
import tkinter as tk
import traceback
from datetime import datetime, timedelta, date
from tkinter import Entry, IntVar, Tk
from typing import Any
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

VERSION = 3
PATH = "G:/My Drive/PoidsPression/"
DAYS = 60


LOG_PATH = f"{PATH}logs/"
LOG_FILE = f'{LOG_PATH}Pression.log'


def namer(name: str) -> str:
    return name.replace(".log", "") + ".log"


if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
fileHandler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when='midnight', interval=1, backupCount=7, encoding=None, delay=False, utc=False, atTime=None, errors=None)
fileHandler.namer = namer
log.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-8s] [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
    handlers=[
        fileHandler,
        logging.StreamHandler()
    ]
)


class Pression:

    def __init__(self):
        log.info('Starting')

    @staticmethod
    def load_csv() -> list[dict]:
        try:
            df: pd.DataFrame = pd.read_csv(f'{PATH}pression.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df.to_dict('records')
        except (FileNotFoundError, pd.errors.EmptyDataError) as ex:
            log.error(ex)
            pressure_list: list[dict[str, datetime]] = []
            return pressure_list

    @staticmethod
    def save_csv(pressure_list: list[dict[str, datetime]]) -> None:
        df: pd.DataFrame = pd.DataFrame(pressure_list)
        df.to_csv(f'{PATH}pression.csv', encoding='utf-8', index=False, date_format="%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def display(pressure_list: list[dict[str, datetime]]) -> None:
        df: pd.DataFrame = pd.DataFrame(pressure_list)

        mean = df.rolling(window=f'{DAYS}D', on='date')['sys'].mean()
        plt.plot(df["date"], mean, color='darkgreen')
        mean = df.rolling(window=f'{DAYS}D', on='date')['dia'].mean()
        plt.plot(df["date"], mean, color='darkblue')
        # mean = df["pulse"].rolling(window=WINDOW).mean()
        # plt.plot(df["date"], mean, color='darkred')

        plt.plot(df["date"], df["sys"], "g", label=f'Sys')
        plt.plot(df["date"], df["dia"], "b", label=f'Dia')

        max_sys: int = int(df['sys'].max(numeric_only=True)) + 1
        min_sys: int = int(df['sys'].min(numeric_only=True)) - 1
        log.info(f"max_sys: {max_sys}, min_sys: {min_sys}")
        max_dia: int = int(df['dia'].max(numeric_only=True)) + 1
        min_dia: int = int(df['dia'].min(numeric_only=True)) - 1
        log.info(f"max_dia: {max_dia}, min_dia: {min_dia}")

        maximum: int = max_sys if max_sys > max_dia else max_dia
        minimum: int = min_sys if min_sys < min_dia else min_dia

        plt.axis((df["date"][0], df["date"][df["date"].size - 1], minimum, maximum))

        yticks: list[int] = []
        count: int = minimum
        while count <= maximum:
            yticks.append(count)
            count += 5
        plt.yticks(yticks)
        plt.minorticks_on()

        if df['sys'].max() >= 160:
            plt.axhspan(160, 165, color='xkcd:pastel orange', linestyle='-')
        plt.axhspan(140, 160, color='xkcd:light orange', linestyle='-')
        plt.axhspan(120, 140, color='xkcd:apricot', linestyle='-')

        plt.axhspan(100, 110, color='xkcd:pastel orange', linestyle='-')
        plt.axhspan(90, 100, color='xkcd:light orange', linestyle='-')
        plt.axhspan(80, 90, color='xkcd:apricot', linestyle='-')

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=7))
        plt.xticks(rotation=45, ha='right', fontsize='small')

        plt.legend()
        plt.tight_layout()
        plt.grid(which="both")
        plt.grid(which="major", linewidth=1)
        plt.grid(which="minor", linewidth=0.2)
        plt.minorticks_on()

        ax: plt.axes.Axes = plt.gca()
        x_min: datetime = pressure_list[0]['date'] - timedelta(days=10)
        x_max: datetime = pressure_list[len(pressure_list) - 1]['date'] + timedelta(days=10)
        ax.set_xlim(x_min, x_max)

        fig: plt.axes.Figure = plt.gcf()
        fig.subplots_adjust(
            left=0.055,
            bottom=0.105,
            right=0.952,
            top=0.948,
            wspace=0.198,
            hspace=0.202
        )
        fig.canvas.manager.set_window_title(f'Pression {VERSION}')
        DPI: float = fig.get_dpi()
        fig.set_size_inches(1280.0 / float(DPI), 720.0 / float(DPI))
        print()
        plt.title(f'Pression {VERSION} (x̄: {DAYS} days), Sys: {df['sys'][len(df['sys']) - 1]}, Dia: {df['dia'][len(df['dia']) - 1]}, Pulse: {df['pulse'][len(df['pulse']) - 1]}, Date: {df['date'][len(df['date']) - 1]}')
        plt.savefig(PATH + 'pression.png')
        plt.show()

    @staticmethod
    def add_line(line: dict) -> None:
        pressure_list.append(line)
        log.info(line)


class Dialog:
    ROOT: Tk = tk.Tk()

    def __init__(self, pression: Pression) -> None:
        Dialog.ROOT.eval('tk::PlaceWindow . center')
        Dialog.ROOT.title(f"Pression {VERSION}")
        Dialog.ROOT.resizable(False, False)

        row = tk.Frame(Dialog.ROOT)
        tk.Label(row, width=20, text=f"Pression v{VERSION}", anchor='center', font=('calibre', 12, 'bold')).pack(side=tk.LEFT)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        entries: list[tuple[Any, Entry, IntVar]] = self.make_form()

        Dialog.ROOT.bind('<Return>', lambda event: self.submit(entries))
        tk.Button(text='Show', width=20, command=lambda: self.submit(entries)).pack(padx=5, pady=5)

        entries[0][1].focus()
        Dialog.ROOT.mainloop()

    @staticmethod
    def validate(character: Any, entry_value: str) -> object:
        return True if (character in '0123456789 ' and len(entry_value) < 4) else False

    def make_form(self) -> list[tuple[Any, Entry, IntVar]]:
        entries: list[tuple[Any, Entry, IntVar]] = []
        for field in 'Sys', 'Dia', 'Pulse':
            row = tk.Frame(Dialog.ROOT)
            tk.Label(row, width=6, text=field, anchor='w', font=('calibre', 12, 'bold')).pack(side=tk.LEFT)
            intVar = tk.IntVar(value='')
            ent = tk.Entry(row, textvariable=intVar, validate='key', validatecommand=(Dialog.ROOT.register(self.validate), '%S', '%P'), font=('calibre', 12, 'normal'), width=4)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, ent, intVar))
        return entries

    @staticmethod
    def submit(entries: list[tuple[Any, Entry, IntVar]]) -> None:
        error: bool = False
        line: dict = {}
        for entry in entries:
            field = entry[0]
            value: int
            try:
                value = entry[2].get()
                line[field.lower()] = value
            except tk.TclError as ex1:
                error = True
                log.error(f'{field}: {ex1}')
        if not error:
            line['date'] = datetime.now()
            pression.add_line(line)
            Dialog.ROOT.destroy()
        elif entries[0][1].get() == '' and entries[1][1].get() == '' and entries[2][1].get() == '':
            Dialog.ROOT.destroy()


if __name__ == "__main__":
    try:
        pression: Pression = Pression()

        start_time: float = time.time()
        pressure_list: list[dict]
        log.info(f'sys.argv: {sys.argv}')

        pressure_list = pression.load_csv()
        dialog: Dialog = Dialog(pression)

        log.info(f"\n{pd.DataFrame(pressure_list).to_string()}")
        pression.save_csv(pressure_list)
        pression.display(pressure_list)
        log.info("--- %s seconds ---" % (time.time() - start_time))
    # c = 5/ 0
    except Exception as ex:
        log.error(ex)
        log.error(traceback.format_exc())
