#region VEXcode Generated Robot Configuration
from vex import *
from cte import *
import urandom
import math

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

# Begin project code

TRAVEL_HEIGHT = 200
SENSOR = [50, 140, 28]


class Chip:
    def __init__(self, arm, sensor, height_of_chip, location_of_chip, sensor_location=SENSOR, travel_height=TRAVEL_HEIGHT, color_of_chip=None):
        self.arm = arm
        self.sensor = sensor
        self.height_of_chip = height_of_chip
        self.current_location = location_of_chip
        self.color_of_chip = color_of_chip
        self.travel_h = travel_height
        self.sensor_location = [sensor_location[0], sensor_location[1], sensor_location[2]+self.height_of_chip]
    
    def move_to(self, destination, grab=True, hold=False):
        end_high = [destination[0], destination[1], self.travel_h]
        start_p = [self.current_location[0], self.current_location[1], self.travel_h]

        if grab:
            self.arm.set_end_effector_magnet(False)

            self.arm.move_to(*start_p)
            self.arm.move_to(self.current_location[0], self.current_location[1], self.current_location[2]+10)
            self.arm.move_to(*self.current_location)

            self.arm.set_end_effector_magnet(True)

        self.arm.move_to(*start_p)
        
        self.arm.move_to(*end_high)
        self.arm.move_to(destination[0], destination[1], destination[2]+10)
        self.arm.move_to(*destination)

        if not hold:
            self.arm.set_end_effector_magnet(False)

            self.arm.move_to(*end_high)
        
        self.current_location = destination.copy()

    def _set_color(self):
        first_loc = self.current_location.copy()
        self.move_to(self.sensor_location, hold=True)

        self.sensor.set_light(LedStateType.ON)
        self.sensor.set_light_power(50, PERCENT)
        wait(1, SECONDS)

        if self.sensor.is_near_object():
            self.color_of_chip = self.sensor.color()
        else:
            raise Exception('Not near object')

        wait(1, SECONDS)
        self.sensor.set_light(LedStateType.OFF)

        self.move_to(first_loc, grab=False)
        
        return self.color_of_chip

    def get_color(self):
        if self.color_of_chip is None:
            return self._set_color()
        else:
            return self.color_of_chip

class Stack:
    def __init__(self, arm, sensor, chip_height, top_chip, amount_stacked):
        self.arm = arm
        self.sensor = sensor
        self.current_location = top_chip #track location by top most chip
        self.chip_height = chip_height
        
        self.chips = []
        for mod in range(amount_stacked):
            self.chips.append(Chip(
                arm=self.arm,
                sensor=self.sensor, 
                height_of_chip=self.chip_height,
                location_of_chip=[top_chip[0], top_chip[1], top_chip[2]-(self.chip_height*mod)]
            ))
    
    @staticmethod
    def StackBuilderObjects(arm, sensor, chip_height, chip_objects: list, destination):
        ans = Stack(
            arm=arm,
            sensor=sensor,
            chip_height=chip_height,
            top_chip=[0, 0, 0],
            amount_stacked=0
        )
        for i, chp in enumerate(chip_objects):
            chp.chips.append(chp)
            chp.move_to([destination[0], destination[1], destination[2]+chip_height*i])
        
        ans.current_location=[
            destination[0],
            destination[1],
            destination[2]+(chip_height*len(chip_objects)),
        ]

        return ans
    
    @staticmethod
    def StackBuilderCords(arm, sensor, chip_height, chip_cords: list, destination):
        chip_objects = []
        for cord in chip_cords:
            chips_objects.append(Chip(
                arm=arm,
                sensor=sensor, 
                height_of_chip=chip_height,
                location_of_chip=cord,
            ))

        return Stack.StackBuilderObjects(
            arm=arm,
            sensor=sensor,
            chip_height=chip_height,
            chips_objects=chip_objects,
            destination=destination,
        )

    def unstack(self, locations_to_place: list):
        ans = []
        for lz, chp in zip(locations_to_place, self.chips):
            ans.append(chp)
            chp.move_to(lz)

        return ans
            
        
        

        

    
    def move_to(self, destination):
        # mod = len(self.chips)
        mod = 1
        for chp in self.chips:
            chp.move_to([destination[0], destination[1], destination[2]+self.chip_height*mod])
            mod += 1

        self.chips = self.chips[::-1]
        self.current_location = destination.copy()


def reprint(brain, msg):
    brain.screen.set_cursor(1, 1)
    brain.screen.clear_row(1)
    brain.screen.print(msg)


if __name__ == '__main__':
    # Brain should be defined by default
    brain = Brain()

    # Robot configuration code
    brain_inertial = Inertial()
    arm_1 = Arm(Ports.PORT1)
    signal_tower_2 = SignalTower(Ports.PORT2)
    optical_3 = Optical(Ports.PORT3)


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
    arm_1.initialize_arm()

    # Reset the Signal Tower lights
    signal_tower_2.set_color(SignalTower.ALL, SignalTower.OFF)
    signal_tower_2.set_color(SignalTower.GREEN, SignalTower.ON)


    # first_chip = Chip(
    #     arm_1,
    #     optical_3,
    #     10,
    #     [59, 208, 13],
    # )

    first_stack = Stack(
        arm_1,
        optical_3,
        10,
        [59, 208, 23],
        2,
    )

    first_stack.move_to([156, 157, 20])
    # reprint(brain, first_chip.get_color())