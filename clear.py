import sys, os
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(basedir)
from drivers import epd2in13_V4

epd = epd2in13_V4.EPD()
epd.init()
epd.Clear(0xFF)
epd.sleep()

print("Display cleared successfully.")