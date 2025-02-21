from pymavlink import mavutil
import change_mode 

# Start a connection listening on a UDP port
# 14551 is connection stream
the_connection = mavutil.mavlink_connection('udpout:192.168.10.10:14550')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % 
        (the_connection.target_system, the_connection.target_component))

def takeoff(altitude=1):
        change_mode.change_mode(the_connection, "GUIDED")
        # arm/disarm
        # second num param is arm/disarm (1 arm, 0 disarm)
        the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
        msg = the_connection.recv_match(type='COMMAND_ACK',blocking=True)
        print(msg)

        # takeoff
        # last value is altitude
        # FIX THIS
        the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0, 0, altitude)
        msg = the_connection.recv_match(type='COMMAND_ACK',blocking=True)
        print(msg)

        return the_connection

def land():
        change_mode.change_mode(the_connection, "LAND")
