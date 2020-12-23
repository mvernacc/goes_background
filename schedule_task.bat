:: Get the absolute path to the python executable.
:: Use `pythonw` so it runs without a shell GUI appearing.
FOR /F "tokens=* USEBACKQ" %%F IN (`where pythonw`) DO (
SET python_exe=%%F
)
:: Schedule a task to periodically run the set_lock_screen.py script.
schtasks /create /tn "Lockscreen GOES Images" /tr "%python_exe% %~dp0set_lock_screen.py" /sc minute /mo 10
