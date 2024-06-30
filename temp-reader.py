import time
import threading
from display import clearDisplay, hc595_shift, pickDigit, number_with_dot, number_without_dot, destroy
from w1thermsensor import W1ThermSensor

temperature = 0.0

def update_temperature():
    """ Update the temperature every second. """
    global temperature
    sensor = W1ThermSensor()
    while True:
        temperature = sensor.get_temperature()
        time.sleep(1)

try:
    threading.Thread(target=update_temperature, daemon=True).start()
    while True:
        for i in range(4):
            clearDisplay()
            digit = (int(temperature * 100) // (10 ** i)) % 10
            pickDigit(i)
            if i == 2:
                hc595_shift(number_with_dot[digit])
            else:
                hc595_shift(number_without_dot[digit])
            time.sleep(0.001)

except KeyboardInterrupt:
    destroy()