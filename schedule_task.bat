schtasks /create /tn "Lockscreen GOES Images" /tr %~dp0set_lock_screen.bat /sc minute /mo 10
