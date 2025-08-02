from datetime import datetime, timedelta
import subprocess


def get_date_diff(start: str, end: str) -> (str, timedelta):
    d1 = datetime.strptime(start, '%d/%m/%Y %H:%M')
    d2 = datetime.strptime(end, '%d/%m/%Y %H:%M')
    return f'{start} - {end} = {abs(d1 - d2)}', (d2 - d1).total_seconds()

def get_j_cig(seconds:int) -> float:
    return round(200.0 / (seconds  / 86400),1)


cig_file_name = 'C:/Users/ADELE/Documents/NetBeansProjects/PycharmProjects/PoidsPression/Cigs.py'
last_line: str = ''
i: int = 0
while len(last_line) == 0:
    i -= 1
    with open(cig_file_name, 'r') as file:
        last_line = file.readlines()[i].strip()

last_timestamp = last_line[last_line.index('-') + 1:last_line.index('=')].strip()

line: (str, int)

# line = get_date_diff('25/07/2025 08:00','27/07/2025 11:49')
# print(line, get_j_cig(line[1]))
# line = get_date_diff('27/07/2025 11:49','29/07/2025 15:26')
# print(line, get_j_cig(line[1]))
# line = get_date_diff('29/07/2025 15:26','01/08/2025 12:00')
# print(line, get_j_cig(line[1]))
# line = get_date_diff(last_timestamp, datetime.now().strftime('%d/%m/%Y %H:%M'))
# print(line, get_j_cig(line[1]))

line = get_date_diff(last_timestamp, datetime.now().strftime('%d/%m/%Y %H:%M'))
string = f'{line[0]}\t{get_j_cig(line[1])} cig/j\t{round(get_j_cig(line[1])/25,1)} pkg/j'
print(string)

if not cig_file_name == __file__.replace('\\', '/'):
    with open(cig_file_name, "a") as file:
        file.write(f'# {string}\n')

    try:
        completed_process = subprocess.run(
            f'"C:/Program Files/Notepad++/notepad++.exe" "{cig_file_name}"',
            capture_output=True,
            timeout=5,
            encoding="utf-8",
            check=False,
            shell=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")

# History
# 25/07/2025 08:00 - 27/07/2025 11:49 = 2 days, 3:49:00		92.6 cig/j  3.7 pkg/j
# 27/07/2025 11:49 - 29/07/2025 15:26 = 2 days, 3:37:00		93.0 cig/j  3.7 pkg/j
# 29/07/2025 15:26 - 01/08/2025 12:00 = 2 days, 22:58:00	70.0 cig/j  2.8 pkg/j
