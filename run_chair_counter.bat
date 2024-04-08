@echo off 
echo Enter the name of the floor plan file (or press Enter to use "rooms.txt"): 
set /p FileName= 
if "%FileName%"=="" set FileName=rooms.txt 
python chair_counter.py %FileName%
pause