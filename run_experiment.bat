@echo off
REM Ensure the Z: drive is mapped
if not exist Z:\ (
      net use Z: "\\vu.local\home\FA_FEWEB-RESEARCH002\Files"
)

REM Navigate to the correct working directory
cd /d "Z:\Comparative-judgement"

REM Run the PsychoPy standalone Python with main.py script (so, running the experiment)
"C:\Users\FA_FEWEB-RESEARCH002\AppData\Local\Programs\PsychoPy\python.exe" run.py

REM Pause to keep the window open in case of errors
pause