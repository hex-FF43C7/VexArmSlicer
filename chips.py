#region VEXcode Generated Robot Configuration
from vex import *
from cte import *
import urandom
import math

"""
ALL LOCATIONS ARE FROM THE BOTTOM MOST FACE OF THE OBJECT,
XYZ LIST IS A LIST FORMATED LIKE SO: [X, Y, Z] 
"""

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
            self.arm.move_to(self.chip_grab_point(current_location, z_mod=10))
            self.arm.move_to(*self.chip_grab_point(self.current_location))

            self.arm.set_end_effector_magnet(True)

        self.arm.move_to(*start_p)
        
        self.arm.move_to(*end_high)
        self.arm.move_to(self.chip_grab_point(destination, z_mod=10))
        self.arm.move_to(self.chip_grab_point(destination))

        if not hold:
            self.arm.set_end_effector_magnet(False)

            self.arm.move_to(*end_high)
        
        self.current_location = destination.copy()
    
    def chip_grab_point(origin_to_convert, z_mod=0):
        return origin_to_convert[0], origin_to_convert[1], origin_to_convert[2] + z_mod + self.height_of_chip

    def _set_color(self, destination=None):
        if destination is None:
            first_loc = self.current_location.copy()
        else:
            first_loc = destination.copy()
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

    def get_color(self, force_scan=False):
        if self.color_of_chip is None or force_scan:
            return self._set_color()
        else:
            return self.color_of_chip

class Stack:
    def __init__(self, arm, sensor, chip_height, origin_chip, amount_stacked, sensor_location=SENSOR, travel_height=TRAVEL_HEIGHT):
        self.arm = arm
        self.sensor = sensor
        self.current_location = origin_chip #track location by origin, bottom face of lowest chip
        self.chip_height = chip_height
        
        self.chips = [] #bottom chip is first, and top chip is last
        for mod in range(amount_stacked):
            self.chips.append(Chip(
                arm=self.arm,
                sensor=self.sensor, 
                height_of_chip=self.chip_height,
                location_of_chip=[origin_chip[0], origin_chip[1], origin_chip[2]+(self.chip_height*mod)]
                sensor_location=sensor_location,
                travel_height=travel_height,
            ))
    
    @classmethod
    def StackBuilderObjects(cls, arm, sensor, chip_height, chip_objects: list, destination, move=True, sensor_location=SENSOR, travel_height=TRAVEL_HEIGHT):
        """
        a factory style class method to build a stack based on a list of chip objects

        Args:
            arm (cte.arm): the arm in charge of moving the chips
            sensor (cte.sensor): the sensor used to log chip color when requested
            chip_height (int): height of chip in mm (because chips are kept track of based on bottom most face, but moved based on top most face, to height must be accounted for)
            chip objects: (list): list of chip objects
            destination (list): where the stack is located after chips are gathered
            sensor_location (list): location of sensor, sensor faces up and the locaiton is the top most face of the sensor, this is the only instance of an origin being based on the top face
            travel_height (int): how high the arm moves when moving latteraly
            move (bool): if true, it will move the chips into the new stack after creation, otherwise its asumed that they are already in stack formation
        
        returns:
            a new stack object with the chips in order and ready
        """
        
        ans = cls(
            arm=arm,
            sensor=sensor,
            chip_height=chip_height,
            origin_chip=[0, 0, 0],
            amount_stacked=0,
            sensor_location=sensor_location,
            travel_height=travel_height
        )
        i = 0
        for chp in chip_objects:
            ans.chips.append(chp)
            if move:
                chp.move_to(
                    [destination[0], destination[1], destination[2]+chip_height*i]
                )
            else:
                chp.current_location = [destination[0], destination[1], destination[2]+chip_height*i]
            i += 1
        
        ans.current_location=[
            destination[0],
            destination[1],
            destination[2]+(chip_height*len(chip_objects)),
        ]

        return ans
    
    @classmethod
    def StackBuilderCords(cls, arm, sensor, chip_height, chip_cords: list, destination, sensor_location=SENSOR, travel_height=TRAVEL_HEIGHT, move=True):
        """
        a factory style class method to build a stack based on the locaiton of other chips

        Args:
            arm (cte.arm): the arm in charge of moving the chips
            sensor (cte.sensor): the sensor used to log chip color when requested
            chip_height (int): height of chip in mm (because chips are kept track of based on bottom most face, but moved based on top most face, to height must be accounted for)
            chip_cords: (list): list of xyz lists to grab the chips from
            destination (list): where the stack is located after chips are gathered
            sensor_location (list): location of sensor, sensor faces up and the locaiton is the top most face of the sensor, this is the only instance of an origin being based on the top face
            travel_height (int): how high the arm moves when moving latteraly
            move (bool): if true, it will move the chips into the new stack after creation, otherwise its asumed that they are already in stack formation
        
        returns:
            a new stack object with the chips in order and ready
        """
        chip_objects = []
        for cord in chip_cords:
            chip_objects.append(Chip(
                arm=arm,
                sensor=sensor, 
                height_of_chip=chip_height,
                location_of_chip=cord,
                sensor_location=sensor_location,
                travel_height=travel_height,
            ))

        return cls.StackBuilderObjects(
            arm=arm,
            sensor=sensor,
            chip_height=chip_height,
            chip_objects=chip_objects,
            destination=destination,
        )

    def unstack(self, locations_to_place: list):
        """
        Unstacks the chips and places them in a series of locations while removing them from the stack

        Args:
            locations_to_place (list): a list of locations for the chips to be placed, top to bottom

        Returns:
            a list of chip objects that where unstacked
        """
            
        ans = []
        for lz, chp in zip(locations_to_place, self.chips_from_top_to_bottom):
            ans.append(chp)
            chp.move_to(lz)
        
        for unstacked_chp in ans:
            self.chips.remove(unstacked_chp)
        
        # self.current_location[2] = self.current_location[2] - (self.chip_height*len(ans))

        return ans
            
        
        
    def move_to(self, destination):
        """
        moves the stack to a new location, but also inverts the order of the stack

        args:
            destinaiton (list): an xyz list for the destinaiton of the stack
        """
        # mod = len(self.chips)
        mod = 1
        for chp in self.chips_from_top_to_bottom:
            chp.move_to([destination[0], destination[1], destination[2]+self.chip_height*mod])
            mod += 1

        self.chips = self.chips[::-1]
        self.current_location = destination.copy()

    def sort(self, key):
        """
        sorts the chips into other stacks depending on the key
        args:
            key:
            [
                [lambda chip_object: chip_object.get_color() == Color.RED, [xyz]],
                [lambda chip_object: chip_object.get_color() == Color.GREEN, [xyz]],
                [lambda chip_object: True, [xyz]] #<-else line
            ]
        """

        # sorted_piles = {tuple(locaiton), self.StackBuilderObjects() for _, locaiton in key}
        sorted_piles = dict()
        for _, locaiton in key:
            sorted_piles[tuple(locaiton)] = self.StackBuilderObjects(
                arm=self.arm,
                sensor=self.sensor,
                chip_height=self.chip_height,
                chip_objects=[],
                destination=list(locaiton),
                move=False,
            )


        for chp in self.chips_from_top_to_bottom:
            chip_sorted_flag = False
            for test, location in key:
                if test(chp):
                    chip_sorted_flag = True
                    sorted_piles[tuple(location)].chips = [chp] + sorted_piles[tuple(location)].chips
                    sorted_piles[tuple(locaiton)].current_location = [
                        sorted_piles[tuple(locaiton)].current_location[0],
                        sorted_piles[tuple(locaiton)].current_location[1],
                        sorted_piles[tuple(locaiton)].current_location[2]+self.chip_height
                    ]
                    chp.move_to([location[0], locaiton[1], locaiton[2]])
                    break
            if not chip_sorted_flag:
                raise Exception('chip couldnt be sorted, please add an else line')

        return sorted_piles
    
    def update_colors(self, destination):
        """
        moves the stack to a new loation same as the move comand, but updates the colors as it does so
        
        Args:
            destination (list): an xyz list on where the chips end up after being scanned
        """
        # mod = len(self.chips)
        mod = 1
        for chp in self.chips_from_top_to_bottom:
            chp.get_color(destination=[destination[0], destination[1], destination[2]+self.chip_height*mod])
            mod += 1

        self.chips = self.chips[::-1]
        self.current_location = destination.copy()
    
    @property
    def chips_from_top_to_bottom(self):
        """
        to make loops more ledgeble, this function renames an arbatrary [::-1] to somthing easyer to understand
        please note that the chips are returned in top to bottom because if using the move command on a chip, you can only really move the top most one at a time.
        """
        return self.chips[::-1]


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

    first_stack = Stack(
        arm_1,
        optical_3,
        10,
        [59, 208, 23],
        2,
    )

    sorted_stacks = first_stack.sort(key=[
        [lambda chp: chp.get_color(force_scan=True) == Color.GREEN, [156, 157, 20]],
        [lambda chp: chp.get_color(force_scan=True) == Color.RED, [156, 30, 20]],
        [lambda chp: True, [156, -30, 40]],
    ])
    print(sorted_stacks)

    # first_stack.move_to([156, 157, 20])
    # chip_list = first_stack.unstack([
    #     [59, 208, 23],
    #     [100, 208, 23]
    # ])
    # reprint(brain, chip_list[0].current_location)

    # second_stack = Stack.StackBuilderObjects(
    #     arm=arm_1,
    #     sensor=optical_3,
    #     chip_height=10,
    #     chip_objects=chip_list[::-1],
    #     destination=[100, 208, 13],
    # )


    # reprint(brain, first_chip.get_color())