import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec2bin(x):
    return [(x >> 1) & 1 for i in range (7, -1, -1)]

try:
    period = float(input("Type a period for sygnal: "))
    while True:
        x = 0
        while(x <= 255):
            GPIO.output(dac, dec2bin(x))
            x = x + 1
            sleep(period/512)
        x = x - 1
        while(x >= 0):
            GPIO.output(dac, dec2bin(x))
            x = x - 1
            sleep(period/512)

except Exception:
    print("Enter an number!")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("EOP")