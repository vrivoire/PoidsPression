@echo 0ff
cls
cd C:\Users\adele\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------
rem pyinstaller --onefile Poids.py --icon=weight-scale.ico --nowindowed --noconsole
start pyinstaller --onedir  Poids.py --icon=weight-scale.ico --nowindowed --noconsole
@echo -------------------------------------------------
rem pyinstaller --onefile Pression.py --icon=pression.ico --nowindowed --noconsole
start pyinstaller --onedir  Pression.py --icon=pression.ico --nowindowed --noconsole
@echo -------------------------------------------------

rem 
