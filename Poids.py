# Takeout
# https://takeout.google.com/


import glob
import logging as log
import logging.handlers
import os.path
import shutil
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

PATH = "G:/My Drive/PoidsPression/"
DL_PATH = "C:/Users/rivoi/Downloads/"
CLOUD_PATH = DL_PATH + "Takeout/Fit/All Data/"
JSON_FILE = "derived_com.google.weight_com.google.android.g.json"
CSV_FILE = "Renpho Health R_PmJP0.csv"
ZIP_FILE = "takeout-*.zip"
WINDOW = 180

log.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
	handlers=[
		logging.handlers.TimedRotatingFileHandler(PATH + "Poids.log", when='midnight', interval=1, backupCount=7, encoding=None, delay=False, utc=False, atTime=None, errors=None),
		logging.StreamHandler()
	]
)


def load_csv():
	if os.path.isfile(PATH + CSV_FILE):
		result = pd.read_csv(PATH + CSV_FILE)
		result = result.rename(columns={'Données de temps': 'date', 'Poids(kg)': 'kg'})
		result = result.drop(['IMC', 'Graisse corporelle(%)', 'Poids hors masse grasse(kg)', 'Gras sous-cutané(%)', 'Graisse viscérale', 'Eau Corporelle Totale(%)', 'Muscle squelettique(%)', 'Masse musculaire(kg)', 'Masse osseuse(kg)', 'Protéines(%)', 'Métabolisme de base(kcal)', 'Âge métabolique', 'Remarques'], axis=1)
		result = result.astype({'date': 'datetime64[ns]'})
		result = result.astype({'kg': 'float'})
		return result.to_dict('records')
	return []


def add_data(file_name):
	data = []
	result = pd.read_json(file_name)
	for dataPoint in result["Data Points"]:
		kg = float(dataPoint["fitValue"][0]["value"]["fpVal"])
		date = pd.to_datetime(
			int(dataPoint["endTimeNanos"]) / 1000000, utc=False, unit="ms"
		)
		if date.year >= 2021:
			data.append({"kg": kg, "date": date})
	return data


def show():
	plt.plot(df["date"], df["kg"], color="g")

	mean = df["kg"].rolling(window=WINDOW).mean()
	plt.plot(df["date"], mean, color='0.5')

	plt.axvline(datetime(2023, 2, 2))

	# median = df["kg"].rolling(window=180).skew()
	# plt.plot(df["date"], median, color='red', label='Running median')

	# plt.legend(loc='best')
	plt.tight_layout()
	plt.grid(which="both")
	plt.grid(which="major", linewidth=1)
	plt.grid(which="minor", linewidth=0.2)
	max_kg = df['kg'].max(numeric_only=True)
	min_kg = df['kg'].min(numeric_only=True)
	plt.title(f"Poids: {df['kg'][len(df['kg']) - 1]}, min: {round(min_kg, 2)}Kg, max: {round(max_kg, 2)}Kg, Δ: {round(max_kg - min_kg, 2)}Kg, x̄: {round(mean[mean.size - 1], 2)}Kg (x̄: {WINDOW} days)")
	max_kg = int(max_kg) + 1
	min_kg = int(min_kg) - 1
	x_min = df['date'][0] - timedelta(days=10)
	x_max = df["date"][df["date"].size - 1] + timedelta(days=10)
	plt.axis((x_min, x_max, min_kg, max_kg))
	yticks = []
	count = min_kg
	while count <= max_kg:
		yticks.append(count)
		count += 1
	plt.yticks(yticks)
	plt.minorticks_on()

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
	# plt.gcf().autofmt_xdate(fontsize='small')  # Rotate and align the tick labels
	plt.xticks(rotation=45, ha='right', fontsize='small')
	plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))

	fig = plt.gcf()
	fig.canvas.manager.set_window_title('Poids')
	DPI = fig.get_dpi()
	fig.set_size_inches(1280.0 / float(DPI), 720.0 / float(DPI))
	plt.savefig(PATH + 'Poids.png')

	plt.show()


if __name__ == "__main__":
	zip_list = glob.glob(DL_PATH + ZIP_FILE)
	if len(zip_list) > 0:
		log.info("Found zipfile from Takeout: " + zip_list[0])
		shutil.unpack_archive(zip_list[0], DL_PATH)
		os.remove(zip_list[0])

	if os.path.isfile(CLOUD_PATH + JSON_FILE):
		shutil.copy2(CLOUD_PATH + JSON_FILE, PATH)
		shutil.rmtree(CLOUD_PATH + '/../..')

	cloud_data = []
	if len(cloud_data) == 0:
		cloud_data = add_data(PATH + JSON_FILE)

	csv_file = PATH + CSV_FILE
	log.info(f"csv_file = {csv_file}")
	csv_root = csv_file[0: (len(csv_file) - 4)]
	log.info(f"csv_root = {csv_root}")

	if os.path.isfile(csv_root):
		log.info("Found csv_root")
		if os.path.isfile(csv_file):
			os.remove(csv_root + ".csv")
		os.rename(csv_root, csv_file)

	if os.path.isfile(DL_PATH + CSV_FILE):
		shutil.copy2(DL_PATH + CSV_FILE, PATH)
		os.remove(DL_PATH + CSV_FILE)
	csv_data = load_csv()

	results = []
	cloud_data.extend(csv_data)
	for myDict in cloud_data:
		if myDict not in results:
			results.append(myDict)
		else:
			log.info(myDict)

	sortedDatas = sorted(results, key=lambda d: d["date"])
	df = pd.DataFrame(sortedDatas)
	df.to_csv(PATH + 'poids.csv', encoding='utf-8', index=False, date_format="%Y-%m-%dT%H:%M:%S")
	log.info('\n' + df.to_string())
	show()
