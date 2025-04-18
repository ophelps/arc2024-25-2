from pymavlink import mavutil

# Start a connection listening to a UDP port
#the_connection = mavutil.mavlink_connection('udpin:localhost:14551')
the_connection = mavutil.mavlink_connection('/dev/serial0', baud=57600)

the_connection.wait_heartbeat()
# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))

while 1:
    msg = the_connection.recv_match(blocking=True)
    print(msg)
