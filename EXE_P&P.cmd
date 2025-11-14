@echo 0ff
cls
cd C:\Users\adele\Documents\NetBeansProjects\PycharmProjects\PoidsPression
call .venv\Scripts\activate.bat
pip freeze > requirements.txt

@echo -------------------------------------------------
start pyinstaller -y --onedir  poidspression\Poids.py --icon=poids.ico --nowindowed --noconsole --paths=C:\Users\ADELE\Documents\NetBeansProjects\PycharmProjects\PoidsPression;C:\Users\ADELE\Documents\NetBeansProjects\PycharmProjects\PoidsPression\.venv\Lib\site-packages
@echo -------------------------------------------------
start pyinstaller -y --onedir  poidspression\Pression.py --icon=pression.png --nowindowed --noconsole --paths=C:\Users\ADELE\Documents\NetBeansProjects\PycharmProjects\PoidsPression;C:\Users\ADELE\Documents\NetBeansProjects\PycharmProjects\PoidsPression\.venv\Lib\site-packages
@echo -------------------------------------------------

rem 
