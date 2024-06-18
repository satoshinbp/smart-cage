import time
import threading
import board
import adafruit_dht
import gpiozero
from flask import Flask, jsonify, render_template

app = Flask(__name__)

temperature = None
humidity = None

LED_PIN = 23
led = gpiozero.DigitalOutputDevice(LED_PIN)

dht_device = adafruit_dht.DHT11(board.D21)

TEMP_WARNING = (18, 25)
TEMP_ALERT = (15, 28)
HUM_WARNING = (40, 60)
HUM_ALERT = (30, 70)

alert_mode = False


def update_alert_mode(temp, hum):
    global alert_mode
    if (
        TEMP_WARNING[0] <= temp <= TEMP_WARNING[1]
        and HUM_WARNING[0] <= hum <= HUM_WARNING[1]
    ):
        led.off()
        alert_mode = False
    elif TEMP_ALERT[0] <= temp <= TEMP_ALERT[1] and HUM_ALERT[0] <= hum <= HUM_ALERT[1]:
        led.on()
        alert_mode = False
    else:
        alert_mode = True


def blink_led():
    while True:
        if alert_mode:
            led.on()
            time.sleep(1)
            led.off()
            time.sleep(1)
        else:
            time.sleep(0.1)


def read_sensor():
    global temperature, humidity
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            update_alert_mode(temperature, humidity)
        except RuntimeError as error:
            print(f"RuntimeError: {error.args[0]}")
        finally:
            time.sleep(2.0)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    return jsonify(temperature=temperature, humidity=humidity)


if __name__ == "__main__":
    sensor_thread = threading.Thread(target=read_sensor)
    sensor_thread.start()
    blink_thread = threading.Thread(target=blink_led)
    blink_thread.start()
    app.run(host="0.0.0.0", port=5000)
