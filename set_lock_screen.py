"""Set the Windows 10 lock screen to a live image of Earth from the GOES satellites.
"""
import asyncio
from datetime import datetime
from io import BytesIO
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from winrt.windows.system.userprofile import UserProfilePersonalizationSettings
from winrt.windows.storage import StorageFile, ApplicationData
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


async def async_main():
    # Fetch the latest GOES image from NOAA's server.
    response = requests.get(GOES_IMG_URL)
    goes_image = Image.open(BytesIO(response.content))
    logger.info(f'Image gotten from {GOES_IMG_URL:s}')

    # Paste the GOES image into a black 4k image.
    image_4k = Image.new('RGB', (3840, 2160))
    image_4k.paste(goes_image, (int((3840 - GOES_IMG_WIDTH) / 2), 2160 - GOES_IMG_HEIGHT))

    # Save the image to a temporary folder, then copy it to the ApplicationData Local Folder.
    now = datetime.now()
    temp_img_filepath = Path(__file__).parent / 'temp' / now.strftime('img_%Y-%m-%dT%H%M%S.jpg')
    image_4k.save(temp_img_filepath)

    img_file = await StorageFile.get_file_from_path_async(os.fspath(
        temp_img_filepath))
    img_file_copy = await img_file.copy_async(
        ApplicationData.get_current().local_folder
    )

    # Set the Lock Screen image.
    # Note - this will fail unless the image file provided to `try_set_lock_screen_image_async`
    # is in the ApplicationData Local Folder.
    settings = UserProfilePersonalizationSettings.get_current()
    success = await settings.try_set_lock_screen_image_async(img_file_copy)
    logger.info(f'Set lock screen success flag: {success}')

    # Clean up.
    img_file.delete_async()
    img_file_copy.delete_async()

asyncio.run(async_main())
