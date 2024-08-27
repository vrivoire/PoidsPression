import logging as log
import logging.handlers
import logging.handlers
import sys
import time
import tkinter as tk
import traceback
from datetime import datetime, timedelta
from tkinter import Entry, IntVar, Tk
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

VERSION = 3
PATH = "G:/My Drive/PoidsPression/"

log.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.handlers.TimedRotatingFileHandler(f'{PATH}Pression.log', when='midnight', interval=1, backupCount=7, encoding=None, delay=False, utc=False, atTime=None, errors=None),
        logging.StreamHandler()
    ]
)


class Pression:

    def __init__(self):
        log.info('Starting')

    def load_csv(self) -> list[dict]:
        try:
            df: pd.DataFrame = pd.read_csv(f'{PATH}pression.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df.to_dict('records')
        except (FileNotFoundError, pd.errors.EmptyDataError) as ex:
            log.error(ex)
            pressure_list: list[dict[str, datetime]] = []
            return pressure_list

    def save_csv(self, pressure_list: list[dict[str, datetime]]) -> None:
        df: pd.DataFrame = pd.DataFrame(pressure_list)
        df.to_csv(f'{PATH}pression.csv', encoding='utf-8', index=False, date_format="%Y-%m-%dT%H:%M:%S")

    def display(self, pressure_list: list[dict[str, datetime]]) -> None:
        df: pd.DataFrame = pd.DataFrame(pressure_list)

        plt.plot(df["date"], df["sys"], "g", label='Sys')
        plt.plot(df["date"], df["dia"], "b", label='Dia')
        plt.plot(df["date"], df["pulse"], "r", label='Pulse')

        max_sys: int = int(df['sys'].max(numeric_only=True)) + 1
        min_sys: int = int(df['sys'].min(numeric_only=True)) - 1
        log.info(f"max_sys: {max_sys}, min_sys: {min_sys}")
        max_dia: int = int(df['dia'].max(numeric_only=True)) + 1
        min_dia: int = int(df['dia'].min(numeric_only=True)) - 1
        log.info(f"max_dia: {max_dia}, min_dia: {min_dia}")
        max_pulse: int = int(df['pulse'].max(numeric_only=True)) + 1
        min_pulse: int = int(df['pulse'].min(numeric_only=True)) - 1
        log.info(f"max_pulse: {max_pulse}, min_pulse: {min_pulse}")

        maximum: int = max_sys if max_sys > max_dia else max_dia
        maximum = (maximum if maximum > max_pulse else max_pulse) + 1

        minimum: int = min_sys if min_sys < min_dia else min_dia
        minimum = int(round(((minimum if minimum < min_pulse else min_pulse) - 1) / 10, 0) * 10)

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
        fig.canvas.manager.set_window_title(f'Pression {VERSION}')
        DPI: float = fig.get_dpi()
        fig.set_size_inches(1280.0 / float(DPI), 720.0 / float(DPI))
        plt.title(f'Pression {VERSION}')
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

    def validate(self, character: Any, entry_value: str) -> object:
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

    def submit(self, entries: list[tuple[Any, Entry, IntVar]]) -> None:
        error: bool = False
        line: dict = {}
        for entry in entries:
            field = entry[0]
            value: int
            try:
                value = entry[2].get()
                line[field.lower()] = value
            except tk.TclError as ex:
                error = True
                log.error(f'{field}: {ex}')
        if not error:
            line['date'] = datetime.now()
            pression.add_line(line)
            Dialog.ROOT.destroy()


if __name__ == "__main__":
    try:
        start_time: float = time.time()
        pression: Pression = Pression()

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
