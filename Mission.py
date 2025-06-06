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
print("Heartbeat from system (system %u component %u)" % 
        (the_connection.target_system, the_connection.target_component))


current_mode = ""

while "auto" not in current_mode.lower():
    msg = the_connection.recv_match(type = 'HEARTBEAT', blocking = False)
    if msg:
        current_mode = mavutil.mode_string_v10(msg)
        print(current_mode)


scan_altitude_meters = 5
#scan_altitude_meters = 1.5
move_altitude_meters = 1
takeoff_tolerance = 100

tag_locations = {}

print("about to loiter")
print("GOT TO TAKEOFF")
#takeoff.takeoff(the_connection, altitude=scan_altitude_meters)
print("Takeoff complete")

#while Scan.get_height(the_connection) < (scan_altitude_meters - takeoff_tolerance / 100) or len(tag_locations) < 3:
while len(tag_locations) < 3:
    print("Scanning for tags...")
    try:
        tag_locations.update(Scan.scan_for_tags(the_connection))
    except:
        takeoff.land(the_connection)
        exit()

    print(tag_locations)

print("Tags found!")

for id in range(1, 4, 1):
    print("Moving to tag #" + str(id))
    Scan.go_to_tag(the_connection, tag_locations[id], altitude=1, tolerance=40)
    print("Movement complete, landing")
    takeoff.land(the_connection)
    while Scan.get_height(the_connection) > 0.2:
        print("Still landing")
        time.sleep(0.5)
    

    print("Landed")
    time.sleep(4)

    takeoff.takeoff(the_connection, move_altitude_meters)
    while id != 3 and Scan.get_height(the_connection) < (move_altitude_meters - takeoff_tolerance / 100):
        print("taking off")
        time.sleep(0.5)
        
    #print
print("Success!")
print(tag_locations)
