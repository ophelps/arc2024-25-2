import libiq.takeoff
import libiq.land
import pymavlink
import time

mav_connection = pymavlink.connect_to_sysid('udpin:0.0.0.0:55555', 1)

for i in range(4):
    libiq.takeoff.takeoff(3.33)
    time.sleep(10)
    libiq.land.land()
    time.sleep(10)
