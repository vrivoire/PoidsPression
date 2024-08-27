@echo 0ff
cls

set PoidsPression=%HOMEDRIVE%%HOMEPATH%\Documents\NetBeansProjects\PycharmProjects\PoidsPression
rem cd %PoidsPression%

@echo -------------------------------------------------
pyinstaller --onefile Poids.py --icon=%PoidsPression%\weight-scale.ico --nowindowed --noconsole
@echo -------------------------------------------------
pyinstaller --onefile Pression3.py --icon=%PoidsPression%\pression.ico --nowindowed --noconsole
@echo -------------------------------------------------

pause
