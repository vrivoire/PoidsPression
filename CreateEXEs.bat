@echo 0ff
cls
cd C:\Users\rivoi\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------
rem pyinstaller --onefile Poids.py --icon=weight-scale.ico --nowindowed --noconsole
pyinstaller --onedir  Poids.py --icon=weight-scale.ico --nowindowed --noconsole
@echo -------------------------------------------------
rem pyinstaller --onefile Pression.py --icon=pression.ico --nowindowed --noconsole
pyinstaller --onedir  Pression.py --icon=pression.ico --nowindowed --noconsole
@echo -------------------------------------------------

pause
