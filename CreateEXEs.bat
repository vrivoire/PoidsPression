@echo 0ff
cls
cd C:\Users\rivoi\Documents\NetBeansProjects\PycharmProjects\PoidsPression
@echo -------------------------------------------------
pyinstaller --onefile Poids.py --icon=weight-scale.ico --nowindowed --noconsole
@echo -------------------------------------------------
pyinstaller --onefile Pression.py --icon=pression.ico --nowindowed --noconsole
@echo -------------------------------------------------

pause
