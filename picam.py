#!/usr/bin/python
# see https://www.youtube.com/watch?v=XPCpwcn2Q6w

#  curl http://picam.local:8080/advance/192.168.1.101/5


call the pi REST by going to http://<IP Address of Raspberry Pi>/advance/<IP Address of DigiCamContol Webservice>/<integer for the number of slides in tray to advance>
#remote wires goto top left, and center pin

import web, requests
import RPi.GPIO as GPIO
import time

urls = ('/advance/(.*)/(.*)', 'advance')

app = web.application(urls, globals())


class advance:

    def GET(self, digi_cam_ip, loops):

        for loop in range(0, int(loops)):

            # specify how the pins are referred to
            GPIO.setmode(GPIO.BCM)

            # pin the relay is connected to on the Raspberry Pi
            pin = 2

            # activate the relay for 0.25 seconds, then release
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.25)
            GPIO.output(pin, GPIO.HIGH)

            GPIO.cleanup()

            # wait for the projector to advance the slide
            time.sleep(4)

            # take the picture by calling DigiCam's webservice
            requests.post("http://" + digi_cam_ip + ":5513/?CMD=Capture")

            # wait for the image to transfer from the camera to the computer
            time.sleep(2)

        return "Finished"

if __name__ == "__main__":
    app.run()
