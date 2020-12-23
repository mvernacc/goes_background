"""
First, take ownership of the SystemData folder by opening command prompt as administrator and running:
```
takeown /F C:\ProgramData\Microsoft\Windows\SystemData\ /r /d Y
```
Reference: https://superuser.com/a/1210076, comments
"""
from pathlib import Path
import subprocess
from io import BytesIO
from PIL import Image
import requests


GOES_IMG_URL = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/1808x1808.jpg'
GOES_IMG_HEIGHT = 1808
GOES_IMG_WIDTH = 1808

# Get the SID of the current user.
wmic_result = subprocess.check_output("wmic useraccount where name='%username%' get sid", shell=True)
sid = wmic_result.decode().split('\n')[1].strip()

# Create the path where Windows keeps the lockscreen image file.
lockscreen_image_filepath = (
    Path(r'C:\ProgramData\Microsoft\Windows\SystemData')
    / sid / r'ReadOnly\LockScreen_O\LockScreen___3840_2160_notdimmed.jpg')
print(lockscreen_image_filepath)

# Fetch the latest GOES image from NOAA's server.
response = requests.get(GOES_IMG_URL)
goes_image = Image.open(BytesIO(response.content))
# goes_image.save('goes_1808x1808.jpg')

# Paste the GOES image into a black 4k image.
image_4k = Image.new('RGB', (3840, 2160))
image_4k.paste(goes_image, (int((3840 - GOES_IMG_WIDTH) / 2), 2160 - GOES_IMG_HEIGHT))

# Write the image to the lockscreen image location.
image_4k.save(lockscreen_image_filepath)
print('Image written to {:s}'.format(lockscreen_image_filepath))
