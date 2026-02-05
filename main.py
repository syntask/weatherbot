from PIL import Image, ImageDraw, ImageFont
import time, datetime
from time import sleep
import sys, os, platform
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(basedir)
import threading
import queue
import requests

def is_sim_mode() -> bool:
    if sys.platform.startswith("linux") and platform.machine().startswith(("arm", "aarch")):
        return False
    return True

sim_mode = is_sim_mode()

if sim_mode:
    import tkinter as tk
    from PIL import ImageTk
else: 
    from drivers import epd2in13_V4

# Queue for image updates
image_queue = queue.Queue()

latitude = 44.9833
longitude = -93.2667
wind_unit = "mph" # kmh, ms, mph, kn
temp_unit = "fahrenheit" # celsius, fahrenheit

temp_str = "°C" if temp_unit == "celsius" else "°F"
wind_str = {"kmh": "KM/H", "ms": "M/S", "mph": "MPH", "kn": "knots"}[wind_unit]

#key for WMO weather interpretation codes to weather thumbnail names
weather_thumbnails = {
    0: "clear-day",
    1: "partly-cloudy-day",
    2: "partly-cloudy-day",
    3: "overcast",
    45: "fog",
    48: "fog",
    51: "rain",
    53: "rain",
    55: "rain",
    56: "rain-snow-mix",
    57: "rain-snow-mix",
    61: "rain",
    63: "rain",
    65: "rain",
    66: "rain-snow-mix",
    67: "rain-snow-mix",
    71: "snow",
    73: "snow",
    75: "snow",
    77: "snow",
    80: "rain",
    81: "rain",
    82: "rain",
    85: "snow",
    86: "snow",
    95: "thunderstorm",
    96: "thunderstorm",
    99: "thunderstorm",
}

weather_data = {}

fnt_dejavu_12 = ImageFont.truetype(basedir + '/assets/fonts/dejavu_sans_mono.ttf', 12)

fnt_dejavu_22= ImageFont.truetype(basedir + '/assets/fonts/dejavu_sans_mono.ttf', 22)

def draw_text(image, text, x, y, halign, valign, font):
    draw = ImageDraw.Draw(image)
    # Use textbbox to get text dimensions (fallback to textsize if not available)
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)

    if halign == "center":
        x_offset = -text_width // 2
    elif halign == "right":
        x_offset = -text_width
    else:
        x_offset = 0

    if valign == "middle":
        y_offset = -text_height // 2
    elif valign == "bottom":
        y_offset = -text_height
    else:
        y_offset = 0

    draw.text((x + x_offset, y + y_offset), text, fill="black", font=font)
    return image

def draw():
    image = Image.new("RGB", (250, 122), "white")
    global weather_data
    
    if "error" in weather_data:
        draw_text(image, "Error fetching weather data:", 125, 30, "center", "top", fnt_dejavu_12)
        draw_text(image, weather_data["error"], 125, 60, "center", "top", fnt_dejavu_12)
    else:
        weather_thumbnail = weather_thumbnails.get(weather_data.get("weather_code", 0), "clear-day")
        image.paste(Image.open(f"{basedir}/assets/weather_thumbnails/{weather_thumbnail}.bmp"), (20, 20))
        weather_str = f"{weather_data.get('temperature_2m', 'N/A')}{temp_str}\n{weather_data.get('windspeed_10m', 'N/A')} {wind_str}\n{weather_data.get('winddirection_10m', 'N/A')}°"
        draw_text(image, weather_str, 112, 51, "left", "middle", fnt_dejavu_22)
        
        draw_text(image, f"Updated at {datetime.datetime.now().strftime('%m/%d %H:%M')}", 125, 120, "center", "bottom", fnt_dejavu_12)
    return image

def tick():
    # Fetch weather data
    
    global weather_data
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": 44.9833,
            "longitude": -93.2667,
            "current": "weather_code,temperature_2m,apparent_temperature,relative_humidity_2m,windspeed_10m,wind_gusts_10m,winddirection_10m",
            "wind_speed_unit": wind_unit,
            "temperature_unit": temp_unit
        })

        data = response.json()
        weather_data = data.get("current", {})
    except Exception as e:
        weather_data = {"error": str(e)}
    
    buffer = draw()
    display_image(buffer)

def main():
    tick()
    # Fire the tick() function at the start of each hour (system time)
    while True:
        now = time.time()
        sleep_time = 900 - (now % 900)
        time.sleep(sleep_time)
        tick()

def display_image(image):
    if sim_mode:
        # Put the image in the queue for the UI thread
        image_queue.put(image)
    else:
        epd.init_fast()
        epd.display(epd.getbuffer(image.rotate(180)))
        epd.sleep()

if __name__ == "__main__":
    if sim_mode:
        def main_thread():
            main()

        # Start main/tick in a background thread
        t = threading.Thread(target=main_thread, daemon=True)
        t.start()

        # Tkinter UI runs on main thread
        root = tk.Tk()
        root.title("Waveshare EPD Simulator")
        img = draw()
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=photo)
        label.pack()

        def poll_queue():
            try:
                while True:
                    new_img = image_queue.get_nowait()
                    photo2 = ImageTk.PhotoImage(new_img)
                    label.config(image=photo2)
                    label.image = photo2
            except queue.Empty:
                pass
            root.after(100, poll_queue)

        root.after(100, poll_queue)
        root.mainloop()
    else:
        epd = epd2in13_V4.EPD()
        main()