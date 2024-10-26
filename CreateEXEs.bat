@echo 0ff
cls
cd C:\Users\rivoi\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------
pyinstaller --onefile Poids.py --icon=weight-scale.ico --nowindowed --noconsole
@echo -------------------------------------------------
pyinstaller --onefile Pression.py --icon=pression.ico --nowindowed --noconsole
@echo -------------------------------------------------

cd C:\Users\rivoi\Documents\NetBeansProjects\PycharmProjects\Thermopro
pyinstaller --onefile Thermopro.py --icon=Thermopro.jpg --nowindowed --noconsole

pause
