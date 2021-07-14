import RPi.GPIO as GPIO
import time

pwm_pin_r = 1#set pin to be used as right pwm
pwm_pin_l = 2#set pin to be used as left pwm
freq = 50#set frequency of pwm

def setup():
	global pwm
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pwm_pin, GPIO.OUT)
	GPIO.output(pwm_pin, GPIO.LOW)
	pwm_l = GPIO.PWM(pwm_pin_l, freq)
	pwm_r = GPIO.PWM(pwm_pin_r, freq)
	pwm_l.start(0)
	pwm_r.start(0)



def loop():
	pos_max = 100
	while True:
		if pos_X > pos_Y:
			dc = pos_X/pos_max
			pwm_l.ChangeDutyCycle(dc)
			pwm_r.ChangeDutyCycle(dc)
		elif pos_Y > pos_X:
			dc = pos_Y/pos_max
			if pos_Y < 0:
				pwm_l.ChangeDutyCycle(0)
				pwm_r.ChangeDutyCycle(dc)
			elif pos_Y > 0:
				pwm_l.ChangeDutyCycle(dc)
				pwm_r.ChangeDutyCycle(0)



def stop():
	pwm.stop()
	GPIO.output(pwm_pin, GPIO.LOW)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		stop()

