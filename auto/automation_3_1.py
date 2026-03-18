#region VEXcode Generated Robot Configuration
from vex import *
from cte import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
arm10 = Arm(Ports.PORT10)
signal_tower_6 = SignalTower(Ports.PORT6)
motor_4 = Motor(Ports.PORT4, True)
motor_2 = Motor(Ports.PORT2, False)
motor_1 = Motor(Ports.PORT1, True)
object_sensor_a = ObjectDetector(brain.three_wire_port.a)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

# Initialize the 6-Axis Arm
arm10.initialize_arm()

# Reset the Signal Tower lights
signal_tower_6.set_color(SignalTower.ALL, SignalTower.OFF)
signal_tower_6.set_color(SignalTower.GREEN, SignalTower.ON)

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode EXP Python Project
# 
# ------------------------------------------

# Library imports
from vex import *
# import asyncio
try:
    import utime
except ImportError:
    class utime:
        def ticks_diff(self, *args):
            raise Exception('import of utime failed')

        def ticks_ms(self):
            raise Exception('import of utime failed')
# Begin project code

CHIP_HEIGHT = 10

BLOCK_HEIGHT = 20

def reprint(msg):
    brain.screen.set_cursor(1, 1)
    brain.screen.clear_row(1)
    brain.screen.print(msg)

class RetTimer:
    def __init__(self, wait_ms):
        self.delay = wait_ms
        self.last_start_time = None

        self.elapsed = 0

        self._enabled_flag = False
    
    def enable(self):
        if self._enabled_flag == False:
            self.last_start_time = utime.ticks_ms()
            self._enabled_flag = True
        else:
            self.update()
    

    def disable(self):
        self._enabled_flag = False
    
    def update(self):
        now = utime.ticks_ms()
        self.elapsed += utime.ticks_diff(self.last_start_time, now)
        self.last_start_time = now

    @property
    def dn(self):
        if not self._enabled_flag: #update the timer if its runing
            self.update()

        if self.elapsed >= self.delay:
            return True
        else:
            return False

    def reset(self):
        self.elapsed = 0


class set_rules:
    def __init__(self):
        pass

    def run(self):
        rule_list = []
        for attribute_name in dir(self):
            attribute_value = getattr(self, attribute_name)
            if callable(attribute_value) and not attribute_name.startswith('__') and not attribute_name in ['run', 'update_inputs', 'update_outputs']:
                rule_list.append(attribute_name)
        
        # raise Exception(rule_list)

        i = 0
        while True:
            self.update_inputs()
            for rule in rule_list:
                rule_func = getattr(self, rule)
                rule_result = rule_func()
                if rule_result != 0:
                    raise Exception('error in {nam} code: {res}'.format(nam=rule, res=rule_result))
            self.update_outputs()
            i += 1
    
    def update_inputs(self):
        pass
    
    def update_outputs(self):
        pass

class rules(set_rules):
    def __init__(self):
        self.start_coil = 0
        self.stop_coil = 1
        self.stop_sensor_coil = 0
        self.run_coil = 0
        self.track_coil = 0

    def update_inputs(self):
        self.start_coil = bool(brain.buttonLeft.pressing())
        self.stop_coil = bool(brain.buttonRight.pressing())
        self.stop_sensor_coil = bool(object_sensor_a.is_object_detected())


    def update_outputs(self):
        if self.track_coil:
            motor_1.spin(FORWARD)
            motor_2.spin(FORWARD)
            motor_4.spin(FORWARD)
        else:
            motor_1.stop()
            motor_2.stop()
            motor_4.stop()


    def rung_1(self):
        # reprint('hello world')
        # reprint(f"((not {self.stop_coil}) and (not {self.stop_sensor_coil}) and ({self.start_coil} or {self.run_coil}))")
        if ((not self.stop_coil) and (not self.stop_sensor_coil) and (self.start_coil or self.run_coil)):
            self.run_coil = 1
        else:
            self.run_coil = 0

        return 0

    def rung_2(self):
        self.track_coil = bool(self.run_coil)

        return 0



if __name__ == '__main__':
    daemon = rules()
    daemon.run()

    # t = RetTimer(5000)
    # reprint('started')
    # while not t.dn:
    #     t.enable()
    
    # reprint('end')
