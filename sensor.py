import sys
import time
import RPi.GPIO as GPIO


hallpin = 2
ledpin = 5
start = 0
counter = 0
bounce_time = 30


if len(sys.argv) == 2:
	bounce_time = int(sys.argv[1])


def sensor_setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(hallpin, GPIO.IN)
	GPIO.setup(ledpin, GPIO.OUT)
	GPIO.output(ledpin, False)
	GPIO.add_event_detect(hallpin, GPIO.RISING, callback = calculate, bouncetime = bounce_time)


def calculate(channel):
	global counter
	global start

	counter = counter + 1
	end = time.time()
	rpm = (1.0 / (end - start)) * 60.0
	start = time.time()
	sys.stdout.write(str(int(rpm)) + "\n")
	sys.stdout.flush()


def main():
	sensor_setup()
	while True:
		time.sleep(0.001)


main()
