@echo off
echo Checking that required modules are installed...
C:\Python27\python.exe get-pip.py
C:\Python27\python.exe -m pip install -r requirements.txt
cls
C:\Python27\python.exe main.py
pause