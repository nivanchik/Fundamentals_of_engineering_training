import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

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

def leds_light(value):
    bin = dec2bin(value)
    GPIO.output(leds, bin)
    return

def adc():
    step = 0
    for value in range(7, -1, -1):
        step += 2**value
        signal = dec2bin(step)
        GPIO.output(dac, signal)
        time.sleep(0.005)
        comp_sig = GPIO.input(comp)
        if comp_sig == 1:
            step -= 2**value    
    return step

try:
    measured_data = []
 
    start = time.time()
    GPIO.output(troyka, 1)
    signal = 0
    while signal < 0.82*maxlevel:
        signal = adc()
        leds_light(signal)
        voltage = maxvoltage*(signal/maxlevel)
        measured_data.append(round(voltage, 2))
        print(round(voltage, 2), "\n")
    
    GPIO.output(troyka, 0)

    while signal > 0.1*maxlevel:
        signal = adc()
        leds_light(signal)
        voltage = maxvoltage*(signal/maxlevel)
        measured_data.append(round(voltage, 2))
        print(round(voltage, 2), "\n")

    finish = time.time()

    absolute_time = finish - start
    number_measures = len(measured_data)

    plt.plot(measured_data)
    plt.show()

    measured_data_str = [str(item) for item in measured_data]

    period = absolute_time/number_measures

    freqence_d = 1/(period)

    step_kvant = max(measured_data)/(2*bits)

    print_settings = [round(freqence_d, 2), round(step_kvant, 2)]
    print_settings_str = [str(item) for item in print_settings]

    print(f" time:  {round(absolute_time, 2)} \n period of measure:  {round(period, 2)} \n middle freqence diskret: {round(freqence_d, 2)} \n step kvant: {round(step_kvant, 2)}")

    with open("data.txt", "w") as outfile:
        outfile.write("\n".join(measured_data_str))
    
    with open("settings.txt", "w") as f:
        f.write("\n".join(print_settings_str))

finally :
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()