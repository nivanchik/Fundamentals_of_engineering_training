import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
bits = len(dac)
levels = 2**bits
maxvoltage = 3.3
troyka = 13
comp = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for value in range(256):
        signal = dec2bin(value)
        GPIO.output(dac, signal)
        comp_sig = GPIO.input(comp)
        sleep(0.007)
        if comp_sig:
            return value

try:
    while(True):
        value = adc()
        voltage = value / levels * maxvoltage
        print(f"number = {value} -- voltage = {round(voltage, 2)}")


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup(dac)
    print("EOP")   