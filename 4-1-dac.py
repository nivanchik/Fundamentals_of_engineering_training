import RPi.GPIO as GPIO

GPIO.setwarnings(False)

dac = [26, 19, 13, 6, 5, 11, 9, 10]

def dec2bin(num):
    return [(num >> 1) & 1 for i in range (7, -1, -1)]


GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

try:
    while True:
        num = input("Type a number from 0 to 255:")
        try:
            num = float(num)
            if num % 1.0 != 0:
                print("Enter an integer!")
            elif 0 <= num <= 255:
                GPIO.output(dac, dec2bin(int(num)))
                voltage = num / 256.0 * 3.3
                print(f"Output voltage is about {voltage:.4} volt")
            else:
                if num < 0:
                    print("Number have to be >=0! Try again...")
                elif num > 255:
                    print("Number is out of range [0, 255]! Try again...")
        except Exception:
            if num == "q": break
            print("You have to type a number, not string! Try again...")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("EOP")