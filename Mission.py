import Scan
import takeoff
import time


scan_altitude_meters = 13
move_altitude_meters = 1
takeoff_tolerance = 5

tag_locations = {}

the_connection = takeoff.takeoff(altitude=scan_altitude_meters)


while Scan.get_height(the_connection) < (scan_altitude_meters - takeoff_tolerance / 100) or len(tag_locations) < 3:
    tag_locations.update(Scan.scan_for_tags(the_connection))
    print(tag_locations)

print("Tags found!")

for id in range(1, 4, 1):
    Scan.go_to_tag(the_connection, tag_locations[id], altitude=1)
    takeoff.land()
    while Scan.get_height(the_connection) > 0:
        print("landing")
        time.sleep(0.5)

    print("Landed")
    time.sleep(0.5)

    takeoff.takeoff(move_altitude_meters)
    while id != 3 and Scan.get_height(the_connection) < (move_altitude_meters - takeoff_tolerance / 100):
        print("taking off")
        time.sleep(0.5)
        
    #print
print("Success!")
print(tag_locations)