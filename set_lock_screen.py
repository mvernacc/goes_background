"""Set the Windows 10 lock screen to a live image of Earth from the GOES satellites.
"""
from pathlib import Path
import subprocess
import logging
from logging.handlers import RotatingFileHandler
from io import BytesIO
from PIL import Image
import requests


GOES_IMG_URL = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/1808x1808.jpg'
GOES_IMG_HEIGHT = 1808
GOES_IMG_WIDTH = 1808


# Set up logging
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
log_file = Path(__file__).parent / 'log.txt'
my_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
logger.addHandler(my_handler)

# Get the SID of the current user.
wmic_result = subprocess.check_output("wmic useraccount where name='%username%' get sid", shell=True)
sid = wmic_result.decode().split('\n')[1].strip()

# Create the path where Windows keeps the lockscreen image file.
lockscreen_image_filepath = (
    Path(r'C:\ProgramData\Microsoft\Windows\SystemData')
    / sid
    / r'ReadOnly\LockScreen_O'  # You might need to change this line.
    / 'LockScreen___3840_2160_notdimmed.jpg')

# Fetch the latest GOES image from NOAA's server.
response = requests.get(GOES_IMG_URL)
goes_image = Image.open(BytesIO(response.content))
logger.info('Image gotten from {:s}'.format(GOES_IMG_URL))

# Paste the GOES image into a black 4k image.
image_4k = Image.new('RGB', (3840, 2160))
image_4k.paste(goes_image, (int((3840 - GOES_IMG_WIDTH) / 2), 2160 - GOES_IMG_HEIGHT))

# Write the image to the lockscreen image location.
image_4k.save(lockscreen_image_filepath)
logger.info('Image written to {:}'.format(lockscreen_image_filepath))
