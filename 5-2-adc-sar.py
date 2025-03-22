import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
bits = len(dac)
maxlevel = 2**bits
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
    step = 0
    for value in range(7, -1, -1):
        step += 2**value
        signal = dec2bin(step)
        GPIO.output(dac, signal)
        sleep(0.01)
        comp_sig = GPIO.input(comp)
        if comp_sig == 1:
            step -= 2**value    
    return step

try:
    while(True):
        value = adc()
        voltage = value / maxlevel * maxvoltage
        print(f"number = {value} -- voltage = {round(voltage, 2)}")


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup(dac)
    print("EOP")  