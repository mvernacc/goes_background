schtasks /create /tn "Lockscreen GOES Images" /tr "python %~dp0set_lock_screen.py" /sc minute /mo 10
