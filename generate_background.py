"""
TODO
Make the images appear in a new folder inside the cwd
Add comments
"""
from datetime import date
from pathlib import Path
import schedule as schedule
from PIL import Image, ImageDraw, ImageFont
import os
import ctypes
import time
import logging


def create_image(day: date):
    filename = day.isoformat() + ".png"
    im = Image.new("RGB", (2560, 1440), (19, 19, 19))
    datefont = ImageFont.truetype("corbelb.ttf", 60)
    dayfont = ImageFont.truetype("corbel.ttf", 50)
    d = ImageDraw.Draw(im)

    d.text((1280, 1440/2-30), date.strftime(day, "%B - %d - %Y"), font=datefont, fill=(255, 255, 255, 255), anchor="mm")
    d.text((1280, 1440/2+30), date.strftime(day, "%A"), font=dayfont, fill=(200, 200, 200, 255), anchor="mm")

    im.save(filename)

    set_wallpaper(os.path.abspath(filename))


def check_date():
    today = date.today()
    yesterday = date(today.year, today.month, today.day)
    try:
        yesterday = date(today.year, today.month, today.day - 1)
    except ValueError:
        logging.error("ValueError: could not subtract 1 from \"yesterday\" day variable")
        pass

    if not Path(today.isoformat() + ".png").exists():
        if yesterday <= today:
            create_image(today)


def set_wallpaper(directory: str):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, directory, 0)


def delete_previous():
    allfiles = sorted(Path(".").glob("[0-9]*.py"))
    if len(allfiles) >= 7:
        try:
            os.remove(allfiles[0])
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    check_date()
    schedule.every().day.at("00:00").do(check_date)
    schedule.every().sunday.do(delete_previous)
    logging.basicConfig(filename="generate_background_logs.log", level=logging.INFO)
    while True:
        schedule.run_pending()
        time.sleep(30)
