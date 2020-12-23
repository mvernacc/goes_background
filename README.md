# goes_background

Set the Windows 10 lock screen to a live* image of Earth from the [GOES satellites](https://www.goes-r.gov/).

Thanks to NOAA and NASA for providing us with these amazing images!

WARNING: USE AT YOUR OWN RISK! I have not tested this code thoroughly, and I can't promise that you won't bork your system using it. In particular, this code uses `PIL` to open a (untrusted) image from the web; `PIL` has had many security vulnerabilities in the past ([examples](https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=python+image+library&search_type=all)).

*It seems the images are 30~40 minutes old by the time they make it from the satellite, though NOAA's servers, to my computer.

![Image of Earth from a GOES satellite](https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/1808x1808.jpg)

## Prerequisites

You must have python 3 installed in Windows 10. You can install python via the Windows Store.

This code is meant to work with a 4k display; the lock screen image is saved with a size of 3840x2160 pixels. It has not been tested with other display resolutions. 

## Setup

### Install requirements

Run in PowerShell or command line, from the repo's top directory:
```
pip install -r requirements.txt
```

### Test the python script

Try running the following in PowerShell or command line:
```
python set_lock_screen.py
```

It should run without errors. Lock your computer, you should see an image of Earth on a black background with a NOAA logo at the bottom as your lock screen.

### Schedule the image update task

Run `schedule_task.bat` in PowerShell or command line. It should print a message starting with `SUCCESS:`.
