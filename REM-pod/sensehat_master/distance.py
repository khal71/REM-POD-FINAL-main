import RPi.GPIO as GPIO
import time
import socket

server_address = ('192.168.104.114', 5000)  # Replace with the IP of your Sense HAT Raspberry Pi

# board numbering system to use
GPIO.setmode(GPIO.BCM)

# variable to delay time
delayTime = 2

# setup of trigger and echo pins
trigPin = 23
echoPin = 24
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # start sensor to send ping. set it low for 2 micros
        GPIO.output(trigPin, 0)
        time.sleep(2E-6)
        # set it high for 10 micros
        GPIO.output(trigPin, 1)
        time.sleep(10E-6)
        # back to zero communication to complete the ping
        GPIO.output(trigPin, 0)
        # when echo pin goes high the timer starts. means the ping is sent
        while GPIO.input(echoPin) == 0:
            pass
        # start the time with system time
        echoStartTime = time.time()
        # wait for echo pin to go down to zero
        while GPIO.input(echoPin) == 1:
            pass
        echoStopTime = time.time()
        # calculate ping travel time
        pingTravelTime = echoStopTime - echoStartTime
        # use time to calculate distance to target
        # found at celsius 22.2 the speed of sound is 344.42 m/s
        # used the site weather.gov/epz/wxcalc_speedofsound.
        # also for equations
        # we divide in 2 since sound is out and back
        dist_cm = (pingTravelTime * 34442) / 2

        data = str(round(dist_cm, 1))
        client_socket.sendto(data.encode(), server_address)

        print('Distance = %s cm' % round(dist_cm, 1))
        # make if for data under 30 cm should register in data text
        

        # sleep to slow things down
        time.sleep(delayTime)

except KeyboardInterrupt:
    GPIO.cleanup()
