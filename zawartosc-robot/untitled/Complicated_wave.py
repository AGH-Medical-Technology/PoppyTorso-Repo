from pypot.creatures import PoppyTorso
import time
import itertools
import numpy

import pypot.dynamixel
if __name__ == '__main__':
    ports = pypot.dynamixel.get_available_ports()
    print('available ports:', ports)

    if not ports:
        raise IOError('No port available.')

    port = ports[0]
    print('Using the first on the list', port)

    dxl_io = pypot.dynamixel.DxlIO(port)
    print('Connected!')

    found_ids = dxl_io.scan()
    print('Found ids:', found_ids)

    if len(found_ids) < 2:
        raise IOError('You should connect at least two motors on the bus for this test.')

    ids = found_ids[:-1]
    dxl_io.enable_torque(ids)
    speed = dict(zip(ids, itertools.repeat(20)))
    dxl_io.set_moving_speed(speed)
    
    t=0
    while(True):
        time.sleep(0.5)
        dxl_io.set_goal_position({42 : 90})
        dxl_io.set_goal_position({52 : -90})
        time.sleep(0.5)
        dxl_io.set_goal_position({54 : -90})
        dxl_io.set_goal_position({44 : 90})
        time.sleep(0.5)
        dxl_io.set_goal_position({37 : 75})
        time.sleep(0.5)
        dxl_io.set_goal_position({41 : 90})
        dxl_io.set_goal_position({51 : -90})
        time.sleep(0.5)
        while(t<5):
            dxl_io.set_goal_position({54 : -120})
            time.sleep(0.5)
            dxl_io.set_goal_position({54 : 120})
            time.sleep(0.5)
            t+=1
        break