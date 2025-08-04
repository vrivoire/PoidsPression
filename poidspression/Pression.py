import ctypes
import os
import sys
import time
import tkinter as tk
import traceback
from datetime import datetime, timedelta
from tkinter import Entry, IntVar, Tk, PhotoImage
from typing import Any

import dateutil.relativedelta
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import date2num, num2date
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import Slider, Button

import poidspression
from poidspression import log

VERSION = 3
PATH = f"{os.getenv('USERPROFILE')}/GoogleDrive/PoidsPression/"
LOCATION = f'{os.getenv('USERPROFILE')}\\Documents\\NetBeansProjects\\PycharmProjects\\PoidsPression\\'

DAYS = 30.437 * 2

class Pression:

    def __init__(self):
        log.info('Starting')

    @staticmethod
    def load_csv() -> list[dict]:
        try:
            df: pd.DataFrame = pd.read_csv(f'{PATH}pression.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df.to_dict('records')
        except (FileNotFoundError, pd.errors.EmptyDataError) as ex1:
            log.error(ex1)
            pressure_list: list[dict[str, datetime]] = []
            return pressure_list

    @staticmethod
    def save_csv(pressure_list: list[dict[str, datetime]]) -> None:
        df: pd.DataFrame = pd.DataFrame(pressure_list)
        if os.path.isfile(PATH + 'poids.csv'):
            df.to_csv(f'{PATH}pression.csv', encoding='utf-8', index=False, date_format="%Y/%m/%d %H:%M:%S")
        else:
            log.warn(f'File not found: {PATH}pression.csv')

    @staticmethod
    def display_graph(pressure_list: list[dict[str, datetime]]) -> None:
        fig, ax1 = plt.subplots()
        df: pd.DataFrame = pd.DataFrame(pressure_list)

        mean = df.rolling(window=f'{DAYS}D', on='date')['sys'].mean()
        ax1.plot(df["date"], mean, color='darkgreen')
        mean = df.rolling(window=f'{DAYS}D', on='date')['dia'].mean()
        ax1.plot(df["date"], mean, color='royalblue')
        mean = df.rolling(window=f'{DAYS}D', on='date')['pulse'].mean()
        plt.plot(df["date"], mean, color='gray')

        l0, = ax1.plot(df["date"], df["sys"], "g", label='Sys')
        l1, = ax1.plot(df["date"], df["dia"], "b", label='Dia')
        l2, = ax1.plot(df["date"], df["pulse"], "k", label='Pulse', visible=False)

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

        plt.tight_layout()
        plt.grid(which="both")
        plt.grid(which="major", linewidth=1)
        plt.grid(which="minor", linewidth=0.2)
        plt.minorticks_on()

        ax: plt.axes.Axes = plt.gca()
        ax.set_xlim(
            pressure_list[0]['date'] - timedelta(days=10),
            pressure_list[len(pressure_list) - 1]['date'] + timedelta(days=10)
        )

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

        last_month = datetime.now() - dateutil.relativedelta.relativedelta(days=DAYS)
        mask = df['date'] > last_month
        df2 = df.loc[mask]
        log.info(f"x: {int(DAYS)} days, sys: {int(df2['sys'].mean())}, dia: {int(df2['dia'].mean())}")
        pressure_list[len(pressure_list) - 1]['date'].strftime('%Y/%m/%d %H:%M')
        plt.title(
            f'Pression (x̄: {int(DAYS)} days, sys: {round(df2['sys'].mean(), 2)}, dia: {round(df2['dia'].mean(), 2)}), sys: {df['sys'][len(df['sys']) - 1]}, dia: {df['dia'][len(df['dia']) - 1]}, pulse: {df['pulse'][len(df['pulse']) - 1]}, Date: {df['date'][len(df['date']) - 1].strftime('%Y/%m/%d %H:%M')}')
        plt.savefig(PATH + 'pression.png')

        def callback_on_clicked(label):
            ln = lines_by_label[label]
            ln.set_visible(not ln.get_visible())
            ln.figure.canvas.draw_idle()

        lines_by_label = {l.get_label(): l for l in [l0, l1, l2]}
        line_colors = [l.get_color() for l in lines_by_label.values()]
        check = CheckButtons(
            ax=ax.inset_axes((0.0, 0.0, 0.05, 0.1)),
            labels=list(lines_by_label.keys()),
            actives=[l.get_visible() for l in lines_by_label.values()],
            label_props={'color': line_colors},
            frame_props={'edgecolor': line_colors},
            check_props={'facecolor': line_colors},
        )
        check.on_clicked(callback_on_clicked)

        def callback_update(val):
            slider_position.valtext.set_text(num2date(val).date())
            window = [
                val - DAYS,
                val + 1,
                minimum,
                maximum
            ]
            ax1.axis(window)
            fig.canvas.draw_idle()

        def callback_reset(event):
            slider_position.reset()
            window = [
                date2num(df["date"][0]),
                date2num(df['date'][len(df['date']) - 1]),
                minimum,
                maximum
            ]
            ax1.axis(window)
            fig.canvas.draw_idle()

        slider_position = Slider(
            plt.axes((0.08, 0.01, 0.73, 0.03), facecolor='White'),
            'Date',
            date2num(df["date"][0]),
            date2num(df['date'][len(df['date']) - 1]),
            valstep=1,
            color='w',
            initcolor='none'
        )
        slider_position.valtext.set_text(df["date"][0].date())
        slider_position.on_changed(callback_update)
        button = Button(fig.add_axes((0.9, 0.01, 0.055, 0.03)), 'Reset', hovercolor='0.975')
        button.on_clicked(callback_reset)

        thismanager = matplotlib.pyplot.get_current_fig_manager()
        img = PhotoImage(file=f'{LOCATION}pression.png')
        thismanager.window.tk.call('wm', 'iconphoto', thismanager.window._w, img)

        plt.show()

    @staticmethod
    def add_line(line: dict) -> None:
        pressure_list.append(line)


class Dialog:
    ROOT: Tk = tk.Tk()

    def __init__(self, pression: Pression) -> None:
        Dialog.ROOT.eval('tk::PlaceWindow . center')
        Dialog.ROOT.title(f"Pression {VERSION}")
        Dialog.ROOT.resizable(False, False)

        row = tk.Frame(Dialog.ROOT)
        tk.Label(row, width=20, text=f"Pression v{VERSION}", anchor='center', font=('calibre', 12, 'bold')).pack(
            side=tk.LEFT)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        entries: list[tuple[Any, Entry, IntVar]] = self.make_form()

        Dialog.ROOT.bind('<Return>', lambda event: self.submit(entries))
        tk.Button(text='Show', width=20, command=lambda: self.submit(entries)).pack(padx=5, pady=5)

        entries[0][1].focus()

        photo = tk.PhotoImage(file=f'{LOCATION}pression.png')
        Dialog.ROOT.wm_iconphoto(False, photo)

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
            ent = tk.Entry(row, textvariable=intVar, validate='key',
                           validatecommand=(Dialog.ROOT.register(self.validate), '%S', '%P'),
                           font=('calibre', 12, 'normal'), width=4)
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
    poidspression.set_up(__file__)
    try:
        i = 0
        while not os.path.exists(f'{PATH}pression.csv') and i < 5:
            log.warning(f'The path "{f'{PATH}pression.csv'}" not ready.')
            i += 1
            time.sleep(10)
        if not os.path.exists(f'{PATH}pression.csv'):
            ctypes.windll.user32.MessageBoxW(0, "Mapping not ready.", "Warning!", 16)
            sys.exit()

        pression: Pression = Pression()

        start_time: float = time.time()
        pressure_list: list[dict]
        log.info(f'sys.argv: {sys.argv}')

        pressure_list = pression.load_csv()
        dialog: Dialog = Dialog(pression)

        log.info(f"\n{pd.DataFrame(pressure_list)}")
        pression.save_csv(pressure_list)
        pression.display_graph(pressure_list)
        log.info("--- %s seconds ---" % (time.time() - start_time))
    # c = 5/ 0
    except Exception as ex:
        log.error(ex)
        log.error(traceback.format_exc())
