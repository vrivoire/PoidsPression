@echo off
echo --------------------------------- PoidsPression ---------------------------------

cd %USERPROFILE%\Documents\NetBeansProjects\PycharmProjects\PoidsPression
echo .
call .venv\Scripts\activate.bat
echo .
pip list -v
rem echo .
rem pip-review
echo .
pip-review --interactive
echo .
pip list
echo .
pip freeze > requirements.txt
echo .
pause