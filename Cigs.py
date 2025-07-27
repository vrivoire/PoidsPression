from datetime import datetime


def get_date_diff(start: str, end: str) -> str:
    d1 = datetime.strptime(start, "%d/%m/%Y %H:%M")
    d2 = datetime.strptime(end, "%d/%m/%Y %H:%M")
    return f'{start} - {end} = {abs(d1 - d2)}'


line: str = get_date_diff('25/07/2025 08:00', datetime.now().strftime("%d/%m/%Y %H:%M"))
print(line)

with open(__file__, "a", newline='') as file:
    file.write('# '+ line + "\n")


# History
