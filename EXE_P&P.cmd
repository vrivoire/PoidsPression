@echo 0ff
cls
cd C:\Users\adele\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------
start pyinstaller -y --onedir  poidspression\Poids.py --icon=poids.ico --nowindowed --noconsole --paths=C:\Users\ADELE\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------
start pyinstaller -y --onedir  poidspression\Pression.py --icon=pression.png --nowindowed --noconsole --paths=C:\Users\ADELE\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------
start pyinstaller -y --onedir  poidspression\Cigs.py --icon=cig.png --nowindowed --noconsole --paths=C:\Users\ADELE\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------

rem 
