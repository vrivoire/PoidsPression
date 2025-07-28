from datetime import datetime
import subprocess


def get_date_diff(start: str, end: str) -> (str, int):
    d1 = datetime.strptime(start, '%d/%m/%Y %H:%M')
    d2 = datetime.strptime(end, '%d/%m/%Y %H:%M')
    return f'{start} - {end} = {abs(d1 - d2)}', int(abs(d1 - d2).seconds)


cig_file_name = 'C:/Users/ADELE/Documents/NetBeansProjects/PycharmProjects/PoidsPression/Cigs.py'
last_line: str = ''
i: int = 0
while len(last_line) == 0:
    i -= 1
    with open(cig_file_name, 'r') as file:
        last_line = file.readlines()[i].strip()

last_timestamp = last_line[last_line.index('-') + 1:last_line.index('=')].strip()

line: (str, int) = get_date_diff(last_timestamp, datetime.now().strftime('%d/%m/%Y %H:%M'))

string = f'{line[0]}\t{int((200.0 / (line[1] / 60 / 24)))} cig/j'
print(string)

if not cig_file_name == __file__.replace('\\', '/'):
    with open(cig_file_name, "a") as file:
        file.write(f'# {string}\n')

    completed_process = subprocess.run(
        f'"C:/Program Files/Notepad++/notepad++.exe" "{cig_file_name}"',
        capture_output=True,
        timeout=70,
        encoding="utf-8",
        check=False,
        shell=True
    )

# History
# 25/07/2025 08:00 - 27/07/2025 11:49 = 2 days, 3:49:00

