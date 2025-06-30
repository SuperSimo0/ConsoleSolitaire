@echo off
if not "%1" == "max" start /MAX cmd /c %0 max & exit/b

pip install -r requirements.txt
python main.py

pause