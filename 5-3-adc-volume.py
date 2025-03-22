import RPi.GPIO as GPIO
import time

leds = [2, 3, 4, 17, 27, 22, 10, 9]
n_leds = len(leds)
volume_mode = [0] * n_leds
dac = [8, 11, 7, 1, 0, 5, 12, 6]
bits = len(dac)
maxlevel = 2**bits - 1
maxvoltage = 3.3
troyka = 13
comp = 14

GPIO.setmode(GPIO.BCM)

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    step = 0
    for value in range(7, -1, -1):
        step += 2**value
        signal = dec2bin(step)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        comp_sig = GPIO.input(comp)
        if comp_sig == 1:
            step -= 2**value    
    return step

try:
    while(True):
        signal = adc()
        volume = round(signal/maxlevel*8)

        for i in range(0, volume):
            volume_mode[i] = 1

        GPIO.output(leds, volume_mode)
        voltage = signal * maxvoltage / maxlevel

        for i in range(0, volume):
            volume_mode[i] = 0

        print(f"number = {signal} -- voltage = {round(voltage, 2)}")

finally :
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()