# goes_background

Set the Windows 10 lock screen to a live* image of Earth from the [GOES satellites](https://www.goes-r.gov/).

Thanks to NOAA and NASA for providing us with these amazing images!

WARNING: USE AT YOUR OWN RISK! This code requires some not-so-safe steps (e.g. taking ownership of and modifying a system file with `ReadOnly` in the name). I have not tested this code thoroughly, and I can't promise that you won't bork your system using it.

*It seems the images are 30~40 minutes old by the time they make it from the satellite, though NOAA's servers, to my computer.

## Prerequisites

You must have python 3 installed in Windows 10. You can install python via the Windows Store.

## Setup

### Take ownership of the folder where lockscreen images are stored

Windows 10 stores the lockscreen image for your user account in 
```
C:\ProgramData\Microsoft\Windows\SystemData\${sid}\ReadOnly\LockScreen_${char}\LockScreen___3840_2160_notdimmed.jpg
```

where `${sid}` is the SID for your user account and ${char} is a random(?) character (it's `O` in my case).

First, find your SID by running the following in command line:
```
wmic useraccount where name='%username%' get sid
```

Then, take ownership of your SystemData folder. Open command line as administrator and run:
```
takeown /F C:\ProgramData\Microsoft\Windows\SystemData\${sid} /r /d Y
```
replacing `${sid}` with your SID.

### Check the character in your lockscreen folder

Your lockscreen image might not be in `C:\ProgramData\Microsoft\Windows\SystemData\${sid}\ReadOnly\LockScreen_O\`, but might instead has some other character in the `LockScreen_` folder name. If this is the case, you will need to modify  `set_lock_screen.py` where `lockscreen_image_filepath` is defined.

### Test the python script

Try running the following in PowerShell or command line:
```
python set_lock_screen.py
```

It should run without errors. Lock your computer, you should see an image of Earth on a black background with a NOAA logo at the bottom as your lock screen.

### Schedule the image update task

Run `schedule_task.bat` in PowerShell or command line. It should print a message starting with `SUCCESS:`.
