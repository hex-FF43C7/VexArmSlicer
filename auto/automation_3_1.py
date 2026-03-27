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
pneumatic_9 = Pneumatic(Ports.PORT9)
optical_7 = Optical(Ports.PORT7)


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


# Color to String Helper
def convert_color_to_string(col):
    if col == Color.RED:
        return "red"
    if col == Color.GREEN:
        return "green"
    if col == Color.BLUE:
        return "blue"
    if col == Color.WHITE:
        return "white"
    if col == Color.YELLOW:
        return "yellow"
    if col == Color.ORANGE:
        return "orange"
    if col == Color.PURPLE:
        return "purple"
    if col == Color.CYAN:
        return "cyan"
    if col == Color.BLACK:
        return "black"
    if col == Color.TRANSPARENT:
        return "transparent"
    return ""
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
            # self.update()
            pass
        
    

    def disable(self):
        self._enabled_flag = False
    
    def update(self):
        if self._enabled_flag:
            now = utime.ticks_ms()

            if self.last_start_time is None:
                self.last_Start_time = now

            else:
                dif = utime.ticks_diff(now, self.last_start_time)
                
                if not now == self.last_start_time:
                    self.elapsed += dif
                    self.last_start_time = now
        
    @property
    def dn(self):
        if self._enabled_flag: #update the timer if its runing
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

        self.run_pump = 0
        self.pump_on_timer = RetTimer(4_500)
        self.pump_off_timer = RetTimer(10_000)

        self.chip_cylynder_active = False
        self.chip_cylynder_extend = RetTimer(2000)
        self.chip_cylynder_retract = RetTimer(3000)

        self.color_queue = [] #[[timer, state],  ...  ] go through and if the most recent timer is done, change gate state to the state and pop the old pair
        self.gate_state = 0 # 0=gate_one 1=gate_two 2=excess
        self.chip_added_coil = 0

        self.manifest = [
            {
                "STATE": 0,
                "RED": 3,
                "GREEN": 1,
            },
            {
                "STATE": 1,
                "RED": 1,
                "GREEN": 3,
            },
        ]

        optical_7.set_light(LedStateType.ON)
        self.color_sensor_background = []
        self.color_sensor_background.append(optical_7.color())


    def update_inputs(self):
        self.start_coil = bool(brain.buttonLeft.pressing())
        self.stop_coil = bool(brain.buttonRight.pressing())
        self.stop_sensor_coil = bool(object_sensor_a.is_object_detected())
        self.color_detected = optical_7.color()
        self.color_object_detected_coil = not optical_7.color() in self.color_sensor_background


    def update_outputs(self):
        if self.run_pump:
            pneumatic_9.pump_on()
        else:
            pneumatic_9.pump_off()

        if self.track_coil:
            motor_1.spin(FORWARD)
            motor_2.spin(FORWARD)
            motor_4.spin(FORWARD)
        else:
            motor_1.stop()
            motor_2.stop()
            motor_4.stop()

        if self.chip_cylynder_active:
            pneumatic_9.extend(CYLINDER4)
        else:
            pneumatic_9.retract(CYLINDER4)
        
        if self.gate_state == 0:
            pneumatic_9.extend(CYLINDER2)
            pneumatic_9.retract(CYLINDER3)

        elif self.gate_state == 1:
            pneumatic_9.retract(CYLINDER2)
            pneumatic_9.extend(CYLINDER3)

        elif self.gate_state == 2:
            pneumatic_9.retract(CYLINDER2)
            pneumatic_9.retract(CYLINDER3)
            

    def rung_1(self):
        # reprint('hello world')
        # reprint(f"((not {self.stop_coil}) and (not {self.stop_sensor_coil}) and ({self.start_coil} or {self.run_coil}))")
        if ((not self.stop_coil) and (self.start_coil or self.run_coil)):
            self.run_coil = 1
        else:
            self.run_coil = 0

        return 0

    def rung_2(self):
        self.track_coil = bool(self.run_coil)

        return 0

    def rung_3(self):
        if (not self.pump_on_timer.dn) and (self.run_pump or self.pump_off_timer.dn):
            self.run_pump = True
        else:
            self.run_pump = False
        
        return 0
            
    
    def rung_4(self):
        if self.run_pump:
            self.pump_on_timer.enable()

            self.pump_off_timer.disable()
            self.pump_off_timer.reset()
        else:
            self.pump_off_timer.enable()

            self.pump_on_timer.disable()
            self.pump_on_timer.reset()

        return 0 
        
    def rung_5(self):
        if (self.run_coil) and (not self.chip_cylynder_extend.dn) and (self.chip_cylynder_active or self.chip_cylynder_retract.dn):
            self.chip_cylynder_active = True
        else:
            self.chip_cylynder_active = False
        
        return 0
            
    
    def rung_6(self):
        if self.chip_cylynder_active:
            self.chip_cylynder_extend.enable()

            self.chip_cylynder_retract.disable()
            self.chip_cylynder_retract.reset()
        else:
            self.chip_cylynder_retract.enable()

            self.chip_cylynder_extend.disable()
            self.chip_cylynder_extend.reset()

        return 0 

    def rung_7(self):
        #add to queue
        if self.color_object_detected_coil and not self.chip_added_coil:

            self.chip_added_coil = True
            # print(self.color_detected)
            if self.color_detected == Color.RED:
                for warehouse in self.manifest:
                    if warehouse['RED'] > 0:
                        warehouse['RED'] -= 1
                        self.color_queue.append([RetTimer(5000), warehouse["STATE"]])
                        self.color_queue[-1][0].enable()
                        break
                    #add red and update manifest

            elif self.color_detected == Color.GREEN:
                for warehouse in self.manifest:
                    if warehouse['GREEN'] > 0:
                        warehouse['GREEN'] -= 1
                        self.color_queue.append([RetTimer(6000), warehouse["STATE"]])
                        self.color_queue[-1][0].enable()
                        break
            else:
                self.color_sensor_background.append(self.color_detected)
                print(self.color_sensor_background)
                
                # return "UNKNOWN COLOR: {}, {}".format(self.color_detected, self.color_object_detected_coil)

        elif not self.color_object_detected_coil and self.chip_added_coil:
            self.chip_added_coil = False

        return 0 
        
    
    def rung_8(self):
        if self.color_queue:
            if self.color_queue[0][0].dn:
                self.gate_state = self.color_queue.pop(0)[-1]
                # print(self.gate_state)
        
        return 0



if __name__ == '__main__':
    daemon = rules()
    daemon.run()

    # t = RetTimer(5000)
    # reprint('started')
    # while not t.dn:
    #     t.enable()
    
    # reprint('end')
