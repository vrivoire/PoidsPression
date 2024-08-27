@echo 0ff
cls

@echo -------------------------------------------------
pyinstaller --onefile Poids.py --icon=weight-scale.ico --nowindowed --noconsole
@echo -------------------------------------------------
pyinstaller --onefile Pression3.py --icon=pression.ico --nowindowed --noconsole
@echo -------------------------------------------------

pause
