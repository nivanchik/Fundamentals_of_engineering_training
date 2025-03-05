import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

point = GPIO.PWM(23, 1000)
point.start(0)

try:
    while True:
        duty_cycle = int(input("duty cycle:"))
        point.ChangeDutyCycle(duty_cycle)
        print(3.3*duty_cycle/100)

finally:
    point.stop()
    GPIO.output(23,0)
    GPIO.cleanup()
