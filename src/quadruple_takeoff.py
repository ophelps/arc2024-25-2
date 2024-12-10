import libiq.takeoff
import libiq.land
import pymavlink
import time

mav_connection = pymavlink.connect_to_sysid('udpin:0.0.0.0:55555', 1)

for i in range(4):
<<<<<<< HEAD
    libiq.takeoff.takeoff(mav_connection, 3.33)
    time.sleep(10)
    libiq.land.land(mav_connection)
=======
    libiq.takeoff.takeoff(3.33)
    time.sleep(10)
    libiq.land.land()
>>>>>>> f130b5e1546df7dbcf0cf069a658044af613f0fd
    time.sleep(10)
