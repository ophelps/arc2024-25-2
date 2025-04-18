
print("Started mission")
print("Importing modules...")
import Scan
import takeoff
import time
from pymavlink import mavutil
print("Imports complete!")

print("Waiting for hardware connection")
the_connection = mavutil.mavlink_connection('/dev/serial0', baud=57600)
the_connection.wait_heartbeat()
print("Heartbeat from system")

print(Scan.scan_for_tags(the_connection))
