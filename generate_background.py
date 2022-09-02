from datetime import date
from pathlib import Path
import schedule as schedule
from PIL import Image, ImageDraw, ImageFont, ImageGrab
import os
import ctypes
import time
import logging


def create_image(day: date):
    """
     Calculate the size of the user's primary display using the dimensions of a screenshot and then
     create the new background image using Pillow and store it into the new directory.
    """
    filename = "backgroundimages/" + day.isoformat() + ".png"
    ss = ImageGrab.grab()
    im = Image.new("RGB", ss.size, (19, 19, 19))
    datefont = ImageFont.truetype("corbelb.ttf", 60)
    dayfont = ImageFont.truetype("corbel.ttf", 50)
    d = ImageDraw.Draw(im)

    d.text((ss.size[0]/2, ss.size[1]/2-30),
           date.strftime(day, "%B - %d - %Y"),
           font=datefont, fill=(255, 255, 255, 255),
           anchor="mm")
    d.text((ss.size[0]/2, ss.size[1]/2+30),
           date.strftime(day, "%A"),
           font=dayfont, fill=(200, 200, 200, 255),
           anchor="mm")

    im.save(filename)

    set_wallpaper(os.path.abspath(filename))


def check_date():
    """
     Grab/Store the current date and then subtract one day and store that as "yesterday".
     If the "yesterday" isn't there then it's safe to assume that it's a new day of a new month/year.
    """
    today = date.today()
    yesterday = date(today.year, today.month, today.day)
    try:
        yesterday = date(today.year, today.month, today.day - 1)
    except ValueError:
        logging.error("ValueError: could not subtract 1 from \"yesterday\" day variable")
        pass
    # Check to see if the current day's image isn't there and then create an image if it's not.
    if not Path("backgroundimages/" + today.isoformat() + ".png").exists():
        if yesterday <= today:
            create_image(today)


def set_wallpaper(directory: str):
    """
     This is magic.
    """
    ctypes.windll.user32.SystemParametersInfoW(20, 0, directory, 0)


def delete_previous():
    """
     Once every sunday this function will:
      - Sort the list of files in the directory that start with a number.
      - Delete the file that's the oldest/lowest (first position after sorting)
    """
    allfiles = sorted(Path("backgroundimages/").glob("[0-9]*"))
    if len(allfiles) >= 7:
        try:
            os.remove(allfiles[0])
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    try:
        os.mkdir("backgroundimages")
    except FileExistsError:
        pass
    check_date()
    # Run the program at midnight
    schedule.every().day.at("00:00").do(check_date)
    # Run this program every sunday
    schedule.every().sunday.do(delete_previous)
    # Generate log file at startup
    logging.basicConfig(filename="generate_background_logs.log", level=logging.INFO)
    while True:
        schedule.run_pending()
        time.sleep(30)
