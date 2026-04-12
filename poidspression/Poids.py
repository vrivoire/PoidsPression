# Takeout
# https://takeout.google.com/

import os.path
import tkinter
from datetime import datetime, timedelta

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.dates as m_dates
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd
from matplotlib.dates import date2num, num2date
from matplotlib.widgets import Slider, Button

import poidspression
from poidspression import log

LOCAL_PATH = F'{os.getenv('USERPROFILE')}/Documents/PoidsPression/'
POIDS_CSV_FILE = 'poids.csv'
GOOGLE_PATH = f"{os.getenv('USERPROFILE')}/GoogleDrive/Mon disque/PoidsPression/"
GOOGLE_FILE = "Renpho Health-R_PmJP0"

# DL_PATH = F"{os.getenv('USERPROFILE')}/Downloads/"
# CLOUD_PATH = DL_PATH + "Takeout/Fit/All Data/"
# JSON_FILE = "derived_com.google.weight_com.google.android.g.json"
# ZIP_FILE = "takeout-*.zip"

DAYS = 30.437 * 3
LOCATION = f'{os.getenv('USERPROFILE')}\\Documents\\NetBeansProjects\\PycharmProjects\\PoidsPression\\'


def load_csv(file_name: str) -> list:
    log.info(f'Looking for {file_name}')
    if os.path.isfile(file_name):
        log.info(f'{file_name} found')
        result = pd.read_csv(file_name)
        result = result.rename(columns={'La date': 'date', 'Temps': 'time', 'Poids(kg)': 'kg'})
        try:
            result = result.drop(
                ['Temps', 'IMC', 'Graisse corporelle(%)', 'Muscle squelettique(%)', 'Poids hors masse grasse(kg)',
                 'Gras sous-cutané(%)', 'Graisse viscérale', 'Eau Corporelle Totale(%)', 'Masse musculaire(kg)',
                 'Masse osseuse(kg)',
                 'Protéines(%)', 'Métabolisme de base(kcal)', 'Âge métabolique', 'Poids optimal(kg)',
                 'Objectif de poids optimal(kg)', 'Objectif masse grasse optimale(kg)',
                 'Objectif de masse musculaire optimale(kg)', 'Type de corps', 'Remarques'],
                axis=1)
        except KeyError:
            pass

        try:
            result['date'] = pd.to_datetime(result['date'] + ' ' + result['time'], format="%Y.%m.%d %H:%M:%S")
            result = result.drop(['time'], axis=1)
        except KeyError:
            pass

        result = result.astype({'date': 'datetime64[ns]'})
        result = result.astype({'kg': 'float'})
        to_dict: list = result.to_dict('records')
        log.info(f'Found {len(to_dict)} entries in {file_name}')
        return to_dict
    else:
        log.info(f'Not found file {file_name}')
    return []


def add_data(file_name):
    log.info(f'Looking for {file_name}')
    data = []
    result = pd.read_json(file_name)
    for dataPoint in result["Data Points"]:
        kg = float(dataPoint["fitValue"][0]["value"]["fpVal"])
        ndate = pd.to_datetime(
            int(dataPoint["endTimeNanos"]) / 1000000, utc=False, unit="ms"
        )
        if ndate.year >= 2021:
            data.append({"kg": kg, "date": ndate})
    return data


def display_graph():
    fig, ax1 = plt.subplots()

    kg, = ax1.plot(df["date"], df["kg"], color="g", label='Kg')
    mean = df.rolling(window=f'{DAYS}D', on='date')['kg'].mean()
    mean_kg, = ax1.plot(df["date"], df.rolling(window=f'{DAYS}D', on='date')['kg'].mean(), color='0.5', label='Mean kg')

    mplcursors.cursor(kg, hover=2).connect("add", lambda sel: sel.annotation.set_text(
        f'{m_dates.num2date(sel.target[0]).strftime('%Y/%m/%d %H:00')}:  {round(float(sel[1][1]), 2)} {sel[0].get_label()}'
    ))
    mplcursors.cursor(mean_kg, hover=2).connect("add", lambda sel: sel.annotation.set_text(
        f'{m_dates.num2date(sel.target[0]).strftime('%Y/%m/%d %H:00')}:  {round(float(sel[1][1]), 2)} {sel[0].get_label()}'
    ))

    plt.axvline(datetime(2023, 2, 2))

    plt.tight_layout()
    plt.grid(which="both")
    plt.grid(which="major", linewidth=1)
    plt.grid(which="minor", linewidth=0.2)
    max_kg = df['kg'].max(numeric_only=True)
    min_kg = df['kg'].min(numeric_only=True)
    plt.title(
        f"Date: {df["date"].tail(1).item().strftime('%Y/%m/%d %H:%M')}, Poids: {df["kg"].tail(1).item()}, min: {round(min_kg, 2)}Kg, max: {round(max_kg, 2)}Kg, "
        f"Δ: {round(max_kg - min_kg, 2)}Kg, x̄: {round(mean.tail(1).item(), 2)}Kg (rolling x̄: {int(DAYS)} days)")
    max_kg = int(max_kg) + 0.5
    min_kg = int(min_kg) - 0.5
    plt.axis((
        df['date'][0] - timedelta(days=10),
        df["date"].tail(1).item() + timedelta(days=10),
        min_kg,
        max_kg
    ))
    yticks = []
    count = min_kg
    while count <= max_kg:
        yticks.append(count)
        count += 1
    plt.yticks(yticks)
    plt.minorticks_on()

    plt.gca().xaxis.set_major_formatter(m_dates.DateFormatter('%Y/%m'))
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
    fig.canvas.manager.set_window_title('Poids')

    def callback_update(val):
        slider_position.valtext.set_text(num2date(val).date())
        df['date'] = pd.to_datetime(df['date'])
        df2 = df[df['date'].dt.date.between(num2date(val - DAYS).date(), num2date(val).date())]
        min2 = df2['kg'].min(numeric_only=True) - 0.5
        if np.isnan(min2):
            min2 = df['kg'].min(numeric_only=True) - 0.5
        max2 = df2['kg'].max(numeric_only=True) + 0.5
        if np.isnan(max2):
            max2 = df['kg'].max(numeric_only=True) + 0.5
        window = [
            val - DAYS,
            val + 1,
            min2,
            max2
        ]
        ax1.axis(window)
        fig.canvas.draw_idle()

    def callback_reset(event):
        slider_position.reset()
        window = [
            date2num(df["date"][0]),
            date2num(df['date'][len(df['date']) - 1]),
            df['kg'].min(numeric_only=True) - 0.5,
            df['kg'].max(numeric_only=True) + 0.5
        ]
        ax1.axis(window)
        fig.canvas.draw_idle()

    slider_position = Slider(
        plt.axes((0.08, 0.01, 0.73, 0.03), facecolor='White'),
        'Date',
        date2num(df["date"][0]),
        date2num(df['date'].tail(1).item()),
        valstep=1,
        color='w',
        initcolor='none'
    )
    slider_position.valtext.set_text(df["date"][0].date())
    slider_position.on_changed(callback_update)
    button = Button(fig.add_axes((0.9, 0.01, 0.055, 0.03)), 'Reset', hovercolor='0.975')
    button.on_clicked(callback_reset)

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    dpi: float = fig.get_dpi()
    root = tkinter.Tk()
    SCREEN_WIDTH: int = root.winfo_screenwidth()
    SCREEN_HEIGHT: int = root.winfo_screenheight()
    root.destroy()
    fig.set_size_inches(SCREEN_WIDTH / float(dpi), SCREEN_HEIGHT / float(dpi))
    plt.savefig(LOCAL_PATH + 'Poids.png')

    plt.show()


def get_from_export():
    pass
    # zip_list = glob.glob(DL_PATH + ZIP_FILE)
    # if len(zip_list) > 0:
    #     log.info("Found zipfile from Takeout: " + zip_list[0])
    #     shutil.unpack_archive(zip_list[0], DL_PATH)
    #     os.remove(zip_list[0])

    # if os.path.isfile(CLOUD_PATH + JSON_FILE):
    #     shutil.copy2(CLOUD_PATH + JSON_FILE, GOOGLE_PATH)
    #     shutil.rmtree(CLOUD_PATH + '/../..')
    # cloud_data = []
    # if os.path.isfile(GOOGLE_PATH + JSON_FILE):
    #     cloud_data = add_data(GOOGLE_PATH + JSON_FILE)
    #     os.remove(GOOGLE_PATH + JSON_FILE)


if __name__ == "__main__":
    poidspression.set_up(__file__)

    get_from_export()

    google_file = GOOGLE_PATH + GOOGLE_FILE
    log.info(f"google_file = {google_file}")

    # if os.path.isfile(DL_PATH + CSV_FILE):
    #     shutil.copy2(DL_PATH + CSV_FILE, GOOGLE_PATH)
    #     os.remove(DL_PATH + CSV_FILE)

    csv_data1 = load_csv(google_file)
    if os.path.isfile(google_file):
        os.remove(google_file)

    csv_data2 = load_csv(LOCAL_PATH + POIDS_CSV_FILE)

    results = []
    results.extend(csv_data1)
    results.extend(csv_data2)

    # cloud_data.extend(csv_data1)
    # for myDict in cloud_data:
    #     if myDict not in results:
    #         results.append(myDict)

    sortedDatas = sorted(results, key=lambda d: d["date"])
    df = pd.DataFrame(sortedDatas)
    df = df.filter(['kg', 'date'])
    df['kg'] = df['kg'].apply(lambda x: round(x, 2))

    df = df.drop(df[(df['date'].dt.hour == 0) & (df['date'].dt.minute == 0) & (df['date'].dt.second == 0)].index)
    df = df.drop_duplicates(subset=['kg', 'date'], keep='first')

    df.to_csv(LOCAL_PATH + POIDS_CSV_FILE, encoding='utf-8', index=False, float_format='%.2f',
              date_format="%Y/%m/%d %H:%M:%S")

    log.info('\n')
    log.info(f'\n{df}')
    display_graph()
