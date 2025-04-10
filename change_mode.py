from pymavlink import mavutil


def change_mode(master, mode, autopilot='ardupilot', sub_mode='NONE'):

    # Check if mode is available
    if mode not in master.mode_mapping():
        print(f'Unknown mode : {mode}')
        print(f"available modes: {list(master.mode_mapping().keys())}")
        raise Exception('Unknown mode')
    
    # Get mode ID
    mode_id = master.mode_mapping()[mode]
    sub_mode = 0

    master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_DO_SET_MODE,
                                0, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode_id, sub_mode, 0, 0, 0, 0)
    ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    print(ack_msg)
    return ack_msg.result