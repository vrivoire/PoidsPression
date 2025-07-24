@echo 0ff
cls
cd C:\Users\adele\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------
rem pyinstaller --onefile Poids.py --icon=weight-scale.ico --nowindowed --noconsole
start pyinstaller -y --onedir  Poids.py --icon=poids.ico --nowindowed --noconsole --paths=C:\Users\ADELE\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------
rem pyinstaller --onefile Pression.py --icon=pression.ico --nowindowed --noconsole
start pyinstaller -y --onedir  Pression.py --icon=pression.png --nowindowed --noconsole --paths=C:\Users\ADELE\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------

rem 
