import time
from gpiozero import Button, LED

switch = Button(24)
counter = 0
prev_status = switch.is_pressed
led = LED(23)

while True:
    current_status = switch.is_pressed
    if prev_status and not current_status:
        counter += 1
        print(counter)
    if not current_status:
        led.on()
    else:
        led.off()
        
    prev_status = current_status
    time.sleep(0.001)
    