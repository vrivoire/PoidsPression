import os
import tkinter
import traceback
from pathlib import Path

import matplotlib
from pandas import DataFrame

matplotlib.use('TkAgg')
import matplotlib.dates as m_dates
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd
from matplotlib.dates import date2num, num2date
from matplotlib.widgets import Slider, Button
import poidspression
from poidspression import log, POIDS_PRESSION_PATH, DAYS

FILE_EXTENSION: str = '.csv'
BKP_FILE: str = 'forfait_Ultime'
BKP_FULL_PATH = POIDS_PRESSION_PATH + BKP_FILE + FILE_EXTENSION

DL_PATH: str = f"{os.getenv('USERPROFILE')}/Downloads/"
DL_FILE_PATTERN: str = f"{BKP_FILE}*{FILE_EXTENSION}"

COLS: dict[str, str] = {
    'Date': 'datetime64[ns]',
    'Description': 'str',
    'Sous-description': 'str',
    'Type d’opération': 'str',
    'Montant': 'Float64',
    'Solde': 'Float64'
}


class Solde:
    def __init__(self):
        df: DataFrame = self.prepare_data()
        self.display_graph(df)

        # df_in.to_json(SENSORS_OUTPUT_JSON_FILE, orient='records', indent=4, date_format='iso',
        #               compression={
        #                   'method': 'zip',
        #                   'compression': zipfile.ZIP_LZMA,
        #                   'compresslevel': 9
        #               })

        # https://pypi.org/project/tabulate/
        # >>> print(tabulate([[0.12345, 0.12345, 0.12345]], floatfmt=(".1f", ".3f")))
        # ---  -----  -------
        # 0.1  0.123  0.12345
        # print(df.to_markdown())
        # print('------------------------------------')

        # print('------------------------------------')
        # print(df.describe(include='all'))
        # print('------------------------------------')
        # print(df.shape)
        # print('------------------------------------')
        # df.info()
        # print('------------------------------------')
        # print(poidspression.ppretty(os.environ.copy()))

    def display_graph(self, df: DataFrame):
        try:
            fig, ax1 = plt.subplots()

            dollars_graph, = ax1.plot(df["Date"], df["Solde"], color="g", label='$')
            mean_dollars = df.rolling(window=f'{int(DAYS)}D', on='Date')['Solde'].mean()
            mean_dollars_graph, = ax1.plot(df["Date"], df.rolling(center=True, window=f'{DAYS}D', on='Date')['Solde'].mean(), color='0.5', label='Mean $')

            mplcursors.cursor(dollars_graph, hover=2).connect("add", lambda sel: sel.annotation.set_text(
                f'{m_dates.num2date(sel.target[0]).strftime('%d/%m/%Y')}:  {round(float(sel[1][1]), 2)} {sel[0].get_label()}'
            ))
            mplcursors.cursor(mean_dollars_graph, hover=2).connect("add", lambda sel: sel.annotation.set_text(
                f'{m_dates.num2date(sel.target[0]).strftime('%d/%m/%Y')}:  {round(float(sel[1][1]), 2)} {sel[0].get_label()}'
            ))

            plt.tight_layout()
            plt.grid(which="both")
            plt.grid(which="major", linewidth=1)
            plt.grid(which="minor", linewidth=0.2)

            title = plt.title(
                f"Date: {df["Date"].tail(1).item().strftime('%d/%m/%Y')}, ${df["Solde"].tail(1).item():,.2f}, min: ${df['Solde'].min(numeric_only=True):.2f}, max: ${df['Solde'].max(numeric_only=True):,.2f}, x̄: ${mean_dollars.tail(1).item():,.2f}, rolling: {int(DAYS)} days)"
            )

            yticks: list[int] = []
            count: int = df['Solde'].min(numeric_only=True)
            while count <= df['Solde'].max(numeric_only=True):
                yticks.append(count)
                count += 10000

            plt.minorticks_on()

            plt.gca().xaxis.set_major_formatter(m_dates.DateFormatter('%m/%Y'))
            plt.gca().xaxis.set_major_locator(m_dates.MonthLocator(interval=1))
            plt.xticks(rotation=45, ha='right', fontsize='small')

            plt.gcf()
            fig.subplots_adjust(
                left=0.055,
                bottom=0.133,
                right=0.952,
                top=0.948,
                wspace=0.198,
                hspace=0.102
            )
            fig.canvas.manager.set_window_title('Solde')

            def callback_update(val):
                slider_position.valtext.set_text(num2date(val).date())
                df2 = df[df['Date'].dt.date.between(num2date(val - DAYS).date(), num2date(val).date())]
                ax1.axis((
                    val - DAYS,
                    val + 1,
                    df2['Solde'].min(numeric_only=True) - 500,
                    df2['Solde'].max(numeric_only=True) + 500
                ))
                mean_dollars = df2.rolling(window=f'{int(DAYS)}D', on='Date')['Solde'].mean()
                title.set_text(
                    f"Date: {df2["Date"].tail(1).item().strftime('%d/%m/%Y')}, ${df2["Solde"].tail(1).item():,.2f}, min: ${df2['Solde'].min(numeric_only=True):,.2f}, max: ${df2['Solde'].max(numeric_only=True):,.2f}, x̄: ${mean_dollars.tail(1).item():,.2f}, rolling: {int(DAYS)} days)"
                )
                fig.canvas.draw_idle()

            def callback_reset(event):
                slider_position.reset()
                ax1.axis((
                    date2num(df["Date"][0]),
                    date2num(df['Date'][len(df['Date']) - 1]),
                    df['Solde'].min(numeric_only=True) - 500,
                    df['Solde'].max(numeric_only=True) + 500
                ))
                mean_dollars = df.rolling(window=f'{int(DAYS)}D', on='Date')['Solde'].mean()
                title.set_text(
                    f"Date: {df["Date"].tail(1).item().strftime('%d/%m/%Y')}, ${df["Solde"].tail(1).item():,.2f}, min: ${df['Solde'].min(numeric_only=True):,.2f}, max: ${df['Solde'].max(numeric_only=True):,.2f}, x̄: ${mean_dollars.tail(1).item():,.2f}, rolling: {int(DAYS)} days)"
                )
                fig.canvas.draw_idle()

            slider_position = Slider(
                plt.axes((0.08, 0.01, 0.73, 0.03), facecolor='White'),
                'Date',
                date2num(df["Date"].head(1).item()),
                date2num(df['Date'].tail(1).item()),
                valstep=1,
                color='w',
                initcolor='none'
            )
            slider_position.valtext.set_text(df["Date"][0].date())
            slider_position.on_changed(callback_update)

            button = Button(fig.add_axes((0.9, 0.01, 0.055, 0.03)), 'Reset', hovercolor='0.975')
            button.on_clicked(callback_reset)

            slider_position.set_val(date2num(df['Date'][len(df['Date']) - 1]))

            mng = plt.get_current_fig_manager()
            mng.window.state('zoomed')

            dpi: float = fig.get_dpi()
            root = tkinter.Tk()
            SCREEN_WIDTH: int = root.winfo_screenwidth()
            SCREEN_HEIGHT: int = root.winfo_screenheight()
            root.destroy()
            fig.set_size_inches(SCREEN_WIDTH / float(dpi), SCREEN_HEIGHT / float(dpi))
            plt.savefig(POIDS_PRESSION_PATH + 'Poids.png')

            poidspression.set_icon('dollar_coin.png')

            plt.show()
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())

    def setup_columns(self, df: DataFrame) -> DataFrame:
        df = df.astype(COLS)
        df = df.astype({'Date': 'datetime64[ns]'})
        # df = df.sort_values(by=['Date'], ascending=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df.reset_index(drop=True, inplace=True)
        return df

    def get_df_from_dl(self) -> dict[str, DataFrame]:
        try:
            dicto: dict[str, DataFrame] = {}
            for path in Path(DL_PATH).glob(DL_FILE_PATTERN):
                df_dict: DataFrame | None = poidspression.load_csv(path.__str__(), list(COLS.keys()))
                if df_dict is not None:
                    dicto[path.__str__()] = df_dict
                else:
                    log.warning(f'Could not load file: {path.__str__()}')
            return dicto
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex

    def drop_duplicates(self, df):
        try:
            len1: int = len(df)
            df.drop_duplicates(subset=list(COLS.keys()), keep='first', inplace=True)
            log.info(f'Initial df size: {len1}, removed: {len1 - len(df)} rows, now: {len(df)}')
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex

    def prepare_data(self) -> DataFrame:
        try:
            df: DataFrame = poidspression.load_csv(BKP_FULL_PATH, list(COLS.keys()))
            if df is not None:
                df_dict: dict[str, DataFrame] = self.get_df_from_dl()
                for path, df_tmp in df_dict.items():
                    df = pd.concat([df_tmp, df], axis=0, ignore_index=True, join='outer')
                    df = self.setup_columns(df)
                    log.info(f'Concated: {path}, now {len(df)} rows')

                self.drop_duplicates(df)
                df = self.setup_columns(df)
                df = df.sort_values(by=['Date'], ascending=True)
                df.reset_index(drop=True, inplace=True)
                poidspression.show_df(df, title='Result:', max_rows=10)

                poidspression.save_csv(df, BKP_FULL_PATH)

                for path in df_dict.keys():
                    log.info(f'File {path} deleted')
                    Path(path).unlink(missing_ok=True)
            else:
                log.error('df is None')

            return df
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex


if __name__ == "__main__":
    try:
        poidspression.set_up(__file__)
        solde: Solde = Solde()

    except Exception as ex:
        log.error(ex)
        log.error(traceback.format_exc())
