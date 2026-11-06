import itertools
import numpy
import time

import pypot.dynamixel

AMP = 50
FREQ = 0.5
head_z = 36
head_y = 37
l_shoulder_y = 41
l_shoulder_x = 42
l_elbow_y = 54
r_shoulder_y = 51
r_shoulder_x = 52
r_elbow_y = 44
starting_pos = {head_z: 0,
                    head_y: -60,
                    l_shoulder_y: 0,
                    l_shoulder_x: 90,
                    l_elbow_y: 90,
                    r_shoulder_y: 0,
                    r_shoulder_x: -45,
                    r_elbow_y: -90}

def callib():
    for motor, id in starting_pos.items():
        dxl_io.set_goal_position({motor: id})
        time.sleep(0.1)
    time.sleep(2)

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

    ids = found_ids[:1]

    dxl_io.enable_torque(ids)

    speed = dict(zip(ids, itertools.repeat(100)))
    dxl_io.set_moving_speed(speed)
    pos = dict(zip(ids, itertools.repeat(0)))
    dxl_io.set_goal_position(pos)

    callib()
    t0 = time.time()
    while True:
        t = time.time()
        if (t - t0) > 10:
            break

        pos = AMP * numpy.sin(2 * numpy.pi * FREQ * t)
        dxl_io.set_goal_position(dict(zip(ids, itertools.repeat(pos))))
        print(pos)
        time.sleep(0.02)
    callib()