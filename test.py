import sys, os
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(basedir)
from drivers import epd2in13_V4
from PIL import Image, ImageDraw, ImageFont
from time import sleep

epd = epd2in13_V4.EPD()
epd.init_fast()
epd.Clear(0xFF)
epd.sleep()

font = ImageFont.truetype(basedir + '/assets/fonts/dejavu_sans_mono.ttf', 40)

def draw_text(text, y_position):
    image = Image.new('1', (250, 122), 255)
    draw = ImageDraw.Draw(image)
    draw.text((10, y_position), text, font=font, fill=0)
    epd.display_fast(epd.getbuffer(image.rotate(180)))

number = 1

while number <= 10:
    epd.init_fast()
    draw_text(str(number), 50)
    number += 1
    epd.sleep()